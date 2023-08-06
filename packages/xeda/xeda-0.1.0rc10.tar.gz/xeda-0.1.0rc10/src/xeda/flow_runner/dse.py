import logging
import os
import random
import shutil
import traceback
from concurrent.futures import CancelledError, TimeoutError
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Type, Union

from attr import define
from pebble.common import ProcessExpired
from pebble.pool.process import ProcessPool

from ..dataclass import XedaBaseModel, validator
from ..design import Design
from ..flows.flow import Flow, FlowFatalError, FlowSettingsError
from ..tool import NonZeroExitCode
from ..utils import Timer, dump_json, unique
from . import (
    FlowLauncher,
    add_file_logger,
    get_flow_class,
    print_results,
    semantic_hash,
    settings_to_dict,
)

log = logging.getLogger(__name__)


@define(slots=False)
class FlowOutcome:
    settings: Flow.Settings
    results: Flow.Results
    timestamp: Optional[str]
    run_path: Optional[Path]


class Optimizer:
    class Settings(XedaBaseModel):
        max_workers: int = 8  # >= 2
        timeout: int = 3600  # in seconds

    def __init__(self, settings: Optional[Settings] = None, **kwargs) -> None:
        self.base_settings: Flow.Settings = Flow.Settings()
        self.flow_class: Optional[Type[Flow]] = None
        self.variations: Dict[str, List[str]] = {}

        self.settings = settings if settings else self.Settings(**kwargs)
        self.improved_idx: Optional[int] = None

        self.best: Optional[FlowOutcome] = None

    def next_batch(self) -> Union[None, List[Flow.Settings], List[Dict[str, Any]]]:
        ...

    def process_outcome(self, outcome: FlowOutcome, idx: int) -> bool:
        ...


ONE_THOUSAND = 1000.0


def linspace(a: float, b: float, n: int) -> Tuple[List[float], float]:
    if n < 2:
        return [b], 0
    step = (b - a) / (n - 1)
    return [step * i + a for i in range(n)], step


flow_settings_variations: Dict[str, Dict[str, List[str]]] = {
    "vivado_synth": {
        "synth.steps.synth_design.args.flatten_hierarchy": ["full"],
        "synth.strategy": [
            "Flow_AlternateRoutability",
            "Flow_PerfThresholdCarry",
            "Flow_PerfOptimized_high",
            "Flow_RuntimeOptimized",
        ],
        "impl.strategy": [
            "Flow_RunPostRoutePhysOpt",  # fast
            "Performance_ExtraTimingOpt",
            "Flow_RunPhysOpt",  # fast
            "Performance_NetDelay_low",
            "Performance_Explore",
            "Performance_NetDelay_high",  # slow
            "Performance_ExplorePostRoutePhysOpt",  # slow
            # "Flow_RuntimeOptimized", # fast
            "Performance_Retiming",
            "Performance_RefinePlacement",
        ],
    },
    "vivado_alt_synth": {
        "synth.strategy": [
            "ExtraTimingCongestion",
            "ExtraTimingAltRouting",
            "ExtraTiming",
            # "Timing",
        ],
    },
}


class FmaxOptimizer(Optimizer):
    class Settings(Optimizer.Settings):
        init_freq_low: float
        init_freq_high: float
        max_luts: Optional[int] = None
        max_finder_retries = 10

        max_failed_iters = 6
        max_failed_iters_with_best = 3

        delta: float = 0.001
        resolution: float = 0.2
        min_freq_step: float = 0.02

        # min improvement before increasing variations
        variation_min_improv = 1.0

        @validator("init_freq_high")
        def validate_init_freq(cls, value, values):
            assert (
                value > values["init_freq_low"]
            ), "init_freq_high should be more than init_freq_low"
            return value

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.no_improvements: int = 0
        self.prev_frequencies = []
        self.freq_step: float = 0.0
        self.num_variations = 1
        self.last_improvement: float = 0.0

        # can be different due to rounding errors, TODO only keep track of periods?
        self.previously_tried_periods = set()
        assert isinstance(self.settings, self.Settings)
        self.hi_freq = self.settings.init_freq_high
        self.lo_freq = self.settings.init_freq_low
        self.num_iterations: int = 0

    @property
    def best_freq(self) -> Optional[float]:
        return self.best.results.get("Fmax") if self.best else None

    def update_bounds(self) -> bool:
        """
        update low and high bounds based on previous results
        It's called _before_ calculation of each iteration batch
        return False -> stop iteration
        """
        assert isinstance(self.settings, self.Settings)

        if self.num_iterations == 0:  # first time
            return True
        resolution = self.settings.resolution
        max_workers = self.settings.max_workers
        best_freq = self.best_freq

        if self.hi_freq - self.lo_freq < resolution:
            if self.no_improvements > 1:
                log.info(
                    "Stopping as span (=%0.2f) < %0.2f and %d iterations without improvement",
                    self.hi_freq - self.lo_freq,
                    resolution,
                    self.no_improvements,
                )
                return False

        # if we have a best_freq and little or no improvements on this iteration, increment num_variations
        if best_freq:
            if (
                self.improved_idx is None
                or self.last_improvement < self.settings.variation_min_improv
            ):
                if self.num_variations < max_workers:
                    self.num_variations = self.num_variations + 1
                    log.info(
                        "Increased number of variations to %d", self.num_variations
                    )
        if best_freq:
            # we have a best_freq, but no improvements this time
            # increment lo_freq by a small positive random value
            epsilon = random.uniform(
                self.settings.delta,
                max(self.settings.delta, resolution / (self.num_variations + 2)),
            )
            self.lo_freq = best_freq + epsilon

        if self.improved_idx is None:
            self.no_improvements += 1
            if self.no_improvements > self.settings.max_failed_iters:
                log.info(
                    "Stopping after %d unsuccessfull iterations (max_failed_iters=%d)",
                    self.no_improvements,
                    self.settings.max_failed_iters,
                )
                return False
            if best_freq:
                if self.no_improvements > self.settings.max_failed_iters_with_best:
                    log.info(
                        f"no_improvements={self.no_improvements} > max_failed_iters_with_best({self.settings.max_failed_iters_with_best})"
                    )
                    return False

                if best_freq < self.hi_freq:
                    if self.num_variations > 1 and self.no_improvements < 3:
                        self.hi_freq = max(
                            best_freq + resolution, self.hi_freq - self.settings.delta
                        )
                    else:
                        # no variations or too many failures, just binary search
                        self.hi_freq = (self.hi_freq + best_freq) + 2
                        log.info(
                            "No Improvements. Lowering hi_freq to %0.2f", self.hi_freq
                        )
                else:
                    self.hi_freq = best_freq + self.num_variations * resolution
                    log.warning(
                        "No Improvements, but still incrementing hi_freq to %0.2f (%d variations)",
                        self.hi_freq,
                        self.num_variations,
                    )
            else:
                self.hi_freq = self.lo_freq - resolution
                if self.hi_freq <= resolution:
                    log.warning("hi_freq < resolution")
                    return False
                self.lo_freq = self.hi_freq / (0.7 + self.no_improvements)
                log.info(
                    "Lowering bounds to [%0.2f, %0.2f]", self.lo_freq, self.hi_freq
                )
        else:
            # sanity check, best_freq was set before in case of a successful run
            assert (
                best_freq
            ), f"best_freq was None, while improved_idx={self.improved_idx}"

            # reset no_improvements
            self.no_improvements = 0

            # if best freq
            if best_freq >= self.hi_freq:
                self.hi_freq = best_freq + self.freq_step * max_workers
                log.debug("incrementing hi_freq to %0.2f", self.hi_freq)
            else:
                self.hi_freq = (
                    self.hi_freq + best_freq
                ) / 2 + self.num_variations * resolution
                log.debug("decrementing hi_freq to %0.2f", self.hi_freq)

        if best_freq:
            # sanity check
            assert (
                self.lo_freq > best_freq
            ), f"BUG! self.lo_freq ({self.lo_freq}) <= best_freq({best_freq})"
            assert (
                self.hi_freq > best_freq
            ), f"BUG! self.hi_freq ({self.hi_freq}) <= best_freq({best_freq})"

        log.debug("Bound set to [%0.2f, %0.2f]", self.lo_freq, self.hi_freq)
        return True

    def next_batch(self) -> Union[None, List[Flow.Settings], List[Dict[str, Any]]]:
        assert isinstance(self.settings, self.Settings)

        if not self.update_bounds():
            return None

        batch_settings = []
        finder_retries = 0

        n = self.settings.max_workers
        if self.num_variations > 1:
            log.info("Generating %d variations", self.num_variations)
            n = n // self.num_variations
        while True:
            if self.hi_freq <= 0 or self.lo_freq < 0:
                log.warning(
                    "hi_freq(%0.2f) or lo_freq(%0.2f) were not positive!",
                    self.hi_freq,
                    self.lo_freq,
                )
                return None
            freq_candidates, freq_step = linspace(
                self.lo_freq,
                self.hi_freq,
                n,
            )
            self.freq_step = freq_step
            log.debug(
                "[try %d] lo_freq=%0.2f, hi_freq=%0.2f, freq_step=%0.2f",
                finder_retries,
                self.lo_freq,
                self.hi_freq,
                freq_step,
            )

            if self.best and self.freq_step < self.settings.min_freq_step:
                log.warning(
                    "Stopping: freq_step=%0.2f is below the limit (%0.2f)",
                    freq_step,
                    self.settings.min_freq_step,
                )
                return None

            clock_periods_to_try = []
            frequencies = []
            for freq in freq_candidates:
                clock_period = round(ONE_THOUSAND / freq, 3)
                if clock_period not in self.previously_tried_periods:
                    clock_periods_to_try.append(clock_period)
                    frequencies.append(freq)

            clock_periods_to_try = unique(clock_periods_to_try)

            if len(clock_periods_to_try) >= max(1, n - 1):
                break

            if finder_retries > self.settings.max_finder_retries:
                log.error("finder failed after %d retries!", finder_retries)
                return None

            finder_retries += 1
            if self.best_freq:
                self.hi_freq += self.settings.delta + (
                    random.random() * self.settings.resolution
                )
                log.debug("finder increased hi_freq to %0.2f", self.hi_freq)
            else:
                delta = finder_retries * random.random() + self.settings.delta
                self.hi_freq -= delta
                self.lo_freq = max(0, self.lo_freq - delta)
                log.warning(
                    "finder updated range to [%0.2f, %0.2f]", self.lo_freq, self.hi_freq
                )

        self.previously_tried_periods.update(clock_periods_to_try)

        log.info(
            f"Trying following frequencies (MHz): {[f'{freq:.2f}' for freq in frequencies]}"
        )

        if self.flow_class:
            assert isinstance(self.base_settings, self.flow_class.Settings)

        def rand_choice(lst, mx):
            mx = min(len(lst), mx)
            return random.choice(lst[:mx])

        base_settings = dict(self.base_settings)
        for i in range(self.num_variations):
            for clock_period in clock_periods_to_try:
                vv = settings_to_dict(
                    {
                        k: rand_choice(v, i + 1 + self.no_improvements)
                        for k, v in self.variations.items()
                    },
                    expand_dict_keys=True,
                )
                settings = {**base_settings, "clock_period": clock_period, **vv}
                batch_settings.append(settings)

        self.improved_idx = None
        if batch_settings:
            self.num_iterations += 1
        return batch_settings

    def process_outcome(self, outcome: FlowOutcome, idx: int) -> bool:
        """returns True if this was the best result so far"""
        assert isinstance(self.settings, self.Settings)

        if not outcome.results.success:
            return False

        freq_str = outcome.results.get("Fmax")
        if freq_str is None:
            log.warning("No valid in the results! run_path=%s", outcome.run_path)
            return False
        freq = float(freq_str)

        if self.settings.max_luts:
            lut = outcome.results.get("lut")
            if lut and int(lut) > self.settings.max_luts:
                log.warning(
                    "Used LUTs %s larger than maximum allowed %s. Fmax: %s",
                    lut,
                    self.settings.max_luts,
                    freq,
                )
                outcome.results["exceeds_max_luts"] = True
                return False

        best_freq = self.best_freq
        if best_freq and freq > best_freq:
            self.last_improvement = freq - best_freq
            log.info(
                "New best frequency: %0.2f MHz  Improvement:%0.2f MHz",
                freq,
                self.last_improvement,
            )

        if best_freq is None or freq > best_freq:
            self.best = outcome
            self.base_settings = outcome.settings
            self.improved_idx = idx
            if self.num_variations > 1 and idx > self.settings.max_workers // 2:
                self.num_variations -= 1
            return True
        else:
            log.debug("Lower Fmax: %0.2f than the current best: %0.2f", freq, best_freq)
            return False


class Executioner:
    def __init__(self, launcher: "Dse", design: Design, flow_class):
        self.launcher = launcher
        self.design = design
        self.flow_class = flow_class

    def __call__(
        self, args: Tuple[int, Dict[str, Any]]
    ) -> Tuple[Optional[FlowOutcome], int]:
        idx, flow_settings = args
        try:
            flow = self.launcher.launch_flow(
                self.flow_class, self.design, flow_settings
            )
            return (
                FlowOutcome(
                    settings=deepcopy(flow.settings),
                    results=flow.results,
                    timestamp=flow.timestamp,
                    run_path=flow.run_path,
                ),
                idx,
            )
        except FlowFatalError as e:
            log.warning(f"[Run Thread] Fatal exception during flow: {e}")
            traceback.print_exc()
            log.warning("[Run Thread] Continuing")
        except KeyboardInterrupt as e:
            log.exception("[Run Thread] KeyboardInterrupt received during flow")
            raise e
        except NonZeroExitCode as e:
            log.warning(f"[Run Thread] {e}")
        except Exception as e:
            log.exception(f"Exception: {e}")
        return None, idx


class Dse(FlowLauncher):
    def __init__(
        self,
        optimizer_class: Union[str, Type[Optimizer]],
        optimizer_settings: Union[Dict[str, Any], Optimizer.Settings] = {},
        xeda_run_dir: Union[str, os.PathLike] = "xeda_run_dse",
        cleanup: bool = True,
        keep_optimal_run_dirs: bool = True,
        **kwargs,
    ) -> None:
        super().__init__(
            xeda_run_dir,
            debug=False,
            dump_settings_json=True,
            display_results=False,
            dump_results_json=True,
            cached_dependencies=True,
            run_in_existing_dir=False,
            cleanup=cleanup and not keep_optimal_run_dirs,
            **kwargs,
        )
        if isinstance(optimizer_class, str):
            if optimizer_class == "fmax":
                optimizer_class = FmaxOptimizer
            else:
                raise Exception(f"Unknown optimizer: {optimizer_class}")
        if not isinstance(optimizer_settings, Optimizer.Settings):
            optimizer_settings = optimizer_class.Settings(**optimizer_settings)
        self.optimizer: Optimizer = optimizer_class(settings=optimizer_settings)
        self.keep_optimal_run_dirs = keep_optimal_run_dirs

    def run_flow(
        self,
        flow_class: Union[str, Type[Flow]],
        design: Design,
        flow_settings: Union[None, Dict[str, Any], Flow.Settings] = None,
    ):
        timer = Timer()

        cleanup_nonoptimal_runs = self.cleanup and self.keep_optimal_run_dirs

        optimizer = self.optimizer

        unsuccessfull_iters = 0
        num_iterations = 0
        future = None
        pool = None

        results_sub = [
            "Fmax",
            "lut",
            "ff",
            "slice",
            "latch",
            "bram_tile",
            "dsp",
        ]

        successful_results: List[Dict[str, Any]] = []
        executioner = Executioner(self, design, flow_class)

        if isinstance(flow_class, str):
            flow_class = get_flow_class(flow_class)

        if flow_settings is None:
            flow_settings = {}

        if isinstance(flow_settings, Flow.Settings):
            flow_settings = dict(flow_settings)

        optimizer.variations = flow_settings_variations[flow_class.name]

        base_variation = settings_to_dict(
            {k: v[0] for k, v in optimizer.variations.items() if v},
            expand_dict_keys=True,
        )
        flow_settings = {**flow_settings, **base_variation}

        try:
            base_settings = flow_class.Settings(**flow_settings)
        except FlowSettingsError as e:
            log.error("%s", e)
            exit(1)

        base_settings.redirect_stdout = True

        optimizer.flow_class = flow_class
        optimizer.base_settings = base_settings

        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S%f")[:-3]
        add_file_logger(Path.cwd(), timestamp)
        best_json_path = (
            Path.cwd() / f"fmax_{design.name}_{flow_class.name}_{timestamp}.json"
        )
        log.info("Best results are saved to %s", best_json_path)
        max_workers = optimizer.settings.max_workers
        log.debug("max_workers=%d", max_workers)

        flow_setting_hashes: Set[str] = set()

        iterate = True
        try:
            with ProcessPool(max_workers=max_workers) as pool:
                while iterate:
                    batch_settings = optimizer.next_batch()
                    if not batch_settings:
                        break

                    this_batch = []
                    for s in batch_settings:
                        hash = semantic_hash(s)
                        if hash not in flow_setting_hashes:
                            this_batch.append(s)
                            flow_setting_hashes.add(hash)

                    future = pool.map(
                        executioner,
                        enumerate(this_batch),
                        timeout=optimizer.settings.timeout,
                    )

                    have_success = False
                    improved = False
                    try:
                        iterator = future.result()
                        if not iterator:
                            log.error("Process result iterator is None!")
                            break
                        while True:
                            try:
                                idx: int
                                outcome: FlowOutcome
                                outcome, idx = next(iterator)
                                if outcome is None:
                                    log.error("Flow outcome is None!")
                                    iterate = False
                                    continue
                                improved = optimizer.process_outcome(outcome, idx)
                                if improved:
                                    log.info(
                                        "Writing improved result to %s", best_json_path
                                    )
                                    dump_json(
                                        dict(
                                            best=optimizer.best,
                                            successful_results=successful_results,
                                            total_time=timer.timedelta,
                                            optimizer_settings=optimizer.settings,
                                            num_iterations=num_iterations,
                                            unsuccessfull_iters=unsuccessfull_iters,
                                        ),
                                        best_json_path,
                                        backup_previous=False,
                                    )
                                if outcome.results.success:
                                    have_success = True
                                    r = {k: outcome.results.get(k) for k in results_sub}
                                    successful_results.append(r)
                                if (
                                    cleanup_nonoptimal_runs
                                    and not improved
                                    and (have_success or num_iterations > 0)
                                ):
                                    p = outcome.run_path
                                    if p and p.exists():
                                        log.debug(
                                            "Deleting non-improved run directory: %s",
                                            p,
                                        )
                                        shutil.rmtree(p, ignore_errors=True)
                                        outcome.run_path = None
                            except StopIteration:
                                break  # next(iterator) finished
                            except TimeoutError as e:
                                log.critical(
                                    f"Flow run took longer than {e.args[1]} seconds. Cancelling remaining tasks."
                                )
                                future.cancel()
                            except ProcessExpired as e:
                                log.critical(f"{e}. Exit code: {e.exitcode}")
                    except CancelledError:
                        log.warning("CancelledError")
                    except KeyboardInterrupt as e:
                        pool.stop()
                        pool.join()
                        raise e from None

                    if not have_success:
                        unsuccessfull_iters += 1

                    num_iterations += 1
                    log.info(
                        f"End of iteration #{num_iterations}. Execution time: {timer.timedelta}"
                    )
                    if optimizer.best:
                        print_results(
                            results=optimizer.best.results,
                            title="Best so far",
                            subset=results_sub,
                            skip_if_false=True,
                        )
                    else:
                        log.info("No results to report.")

        except KeyboardInterrupt:
            log.exception("Received Keyboard Interrupt")
            log.critical("future: %s pool: %s", future, pool)
            if pool:
                pool.join()
            if future and not future.cancelled():
                future.cancel()
            if pool:
                pool.close()
                pool.join()
        except Exception as e:
            log.exception(f"Received exception: {e}")
            traceback.print_exc()
        finally:
            if future and not future.cancelled():
                log.warning("Canecelling future")
                future.cancel()
            if pool:
                log.warning("Process pool still active.")
                pool.close()
                pool.join()
            if optimizer.best:
                print_results(
                    results=optimizer.best.results,
                    title="Best Results",
                    subset=results_sub,
                )
                log.info("Best result were written to %s", best_json_path)
            else:
                log.error("No successful runs!")
            log.info(
                "Total execution time: %s  Number of iterations: %d",
                timer.timedelta,
                num_iterations,
            )
        return optimizer.best
