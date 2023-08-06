import logging
from typing import Any, Dict, List, Optional

from ...dataclass import validator
from ..flow import FpgaSynthFlow
from .vivado_synth import RunOptions, VivadoSynth

log = logging.getLogger(__name__)

# curated options based on experiments and Vivado documentations
# and https://www.xilinx.com/support/documentation/sw_manuals/xilinx2022_1/ug901-vivado-synthesis.pdf
strategies: Dict[str, Dict[str, Optional[Dict[str, Any]]]] = {
    "synth": {
        "Debug": {
            "synth": {
                "-assert": None,
                "-debug_log": None,
                "-flatten_hierarchy": "none",
                "-keep_equivalent_registers": None,
                "-no_lc": None,
                "-fsm_extraction": "off",
                "-directive": "RuntimeOptimized",
            },
            "opt": {"-directive": "RuntimeOptimized"},
        },
        "Runtime": {
            "synth": {"-directive": "RuntimeOptimized"},
            "opt": {"-directive": "RuntimeOptimized"},
        },
        "Default": {
            "synth": {"-flatten_hierarchy": "rebuilt", "-directive": "Default"},
            "opt": {"-directive": "ExploreWithRemap"},
        },
        "Timing": {
            "synth": {
                "-flatten_hierarchy": "rebuilt",
                # "-retiming": None,
                "-directive": "PerformanceOptimized",
                "-fsm_extraction": "one_hot",
                "-shreg_min_size": "5",
            },
            "opt": {"-directive": "ExploreWithRemap"},
        },
        "ExtraTiming": {
            "synth": {
                "-flatten_hierarchy": "full",
                "-retiming": None,
                "-directive": "PerformanceOptimized",
                "-fsm_extraction": "one_hot",
                "-resource_sharing": "off",
                "-shreg_min_size": "10",
                "-keep_equivalent_registers": None,
            },
            "opt": {"-directive": "ExploreWithRemap"},
        },
        "ExtraTimingAlt": {
            "synth": {
                "-flatten_hierarchy": "full",
                "-retiming": None,
                "-directive": "PerformanceOptimized",
                "-fsm_extraction": "one_hot",
                "-resource_sharing": "off",
                "-shreg_min_size": "5",
                "-no_lc": None,  # turns off LUT combining
                "-keep_equivalent_registers": None,
            },
            "opt": {"-directive": "ExploreWithRemap"},
        },
        "Area": {
            # AreaOptimized_medium or _high prints error messages in Vivado 2020.1: "unexpected non-zero reference counts", but succeeeds and post-impl sim is OK too
            "synth": {
                "-flatten_hierarchy": "full",
                "-control_set_opt_threshold": "1",
                "-shreg_min_size": "3",
                "-resource_sharing": "auto",
                "-directive": "AreaOptimized_medium",
            },
            "opt": {"-directive": "ExploreArea"},
        },
        "AreaHigh": {
            # AreaOptimized_medium or _high prints error messages in Vivado 2020.1: "unexpected non-zero reference counts",
            # but succeeds and post-impl sim is OK too!
            "synth": {
                "-flatten_hierarchy": "full",
                "-control_set_opt_threshold": "1",
                "-shreg_min_size": "3",
                "-resource_sharvng": "on",
                "-directive": "AreaOptimized_high",
            },
            "opt": {"-directive": "ExploreArea"},
        },
        "AreaPower": {
            # see the comment above for AreaOptimized_medium directive
            "synth": {
                "-flatten_hierarchy": "full",
                "-control_set_opt_threshold": "1",
                "-shreg_min_size": "3",
                "-resource_sharing": "auto",
                "-gated_clock_conversion": "auto",
                "-directive": "AreaOptimized_medium",
            },
            "opt": {"-directive": "ExploreArea"},
        },
        "AreaTiming": {
            "synth": {"-flatten_hierarchy": "rebuilt", "-retiming": None},
            "opt": {"-directive": "ExploreWithRemap"},
        },
        "AreaExploreWithRemap": {
            "synth": {"-flatten_hierarchy": "full", "-retiming": None},
            "opt": {"-directive": "ExploreWithRemap"},
        },
        "AreaExploreWithRemap2": {
            "synth": {"-flatten_hierarchy": "full", "-retiming": None},
            "opt": {"-directive": "ExploreArea"},
        },
        "AreaExplore": {
            "synth": {"-flatten_hierarchy": "full"},
            "opt": {"-directive": "ExploreArea"},
        },
        "Power": {
            "synth": {
                "-flatten_hierarchy": "full",
                "-gated_clock_conversion": "auto",
                "-control_set_opt_threshold": "1",
                "-shreg_min_size": "3",
                "-resource_sharing": "auto",
            },
            "opt": {"-directive": "ExploreSequentialArea"},
            # "power_opt": {},
        },
    },
    # see https://www.xilinx.com/support/documentation/sw_manuals/xilinx2020_1/ug904-vivado-implementation.pdf
    "impl": {
        "Debug": {
            "place": {"-directive": "RuntimeOptimized"},
            "place_opt": {},
            "route": {"-directive": "RuntimeOptimized"},
            "phys_opt": {"-directive": "RuntimeOptimized"},
        },
        "Runtime": {
            "place": {"-directive": "RuntimeOptimized"},
            "place_opt": {},
            "route": {"-directive": "RuntimeOptimized"},
            "phys_opt": {"-directive": "RuntimeOptimized"},
        },
        "Default": {
            "place": {"-directive": "Default"},
            "place_opt": {},
            "route": {"-directive": "Default"},
            "phys_opt": {"-directive": "Default"},
        },
        "Timing": {
            "place": {"-directive": "ExtraPostPlacementOpt"},
            "place_opt": {
                "-retarget": None,
                "-propconst": None,
                "-sweep": None,
                "-aggressive_remap": None,
                "-shift_register_opt": None,
            },
            "phys_opt": {"-directive": "AggressiveExplore"},
            "place_opt2": {"-directive": "Explore"},
            "route": {"-directive": "AggressiveExplore"},
        },
        "ExtraTimingCongestion": {
            "place": {"-directive": "AltSpreadLogic_high"},
            "place_opt": {
                "-retarget": None,
                "-propconst": None,
                "-sweep": None,
                "-remap": None,
                "-muxf_remap": None,
                "-aggressive_remap": None,
                "-shift_register_opt": None,
            },
            "place_opt2": {"-directive": "Explore"},
            "phys_opt": {"-directive": "AggressiveExplore"},
            "route": {"-directive": "AlternateCLBRouting"},
        },
        "ExtraTiming": {
            "place": {"-directive": "ExtraTimingOpt"},
            "place_opt": {
                "-retarget": None,
                "-propconst": None,
                "-sweep": None,
                "-muxf_remap": None,
                "-aggressive_remap": None,
                "-shift_register_opt": None,
            },
            "place_opt2": {"-directive": "Explore"},
            "phys_opt": {"-directive": "AggressiveExplore"},
            "route": {"-directive": "NoTimingRelaxation"},
        },
        "ExtraTimingAutoPlace1": {
            "place": {
                # Also Auto_2, Auto_3. Only available since Vivado 2022.1
                "-directive": "Auto_1",
                " -timing_summary": None,
            },
            "place_opt": {
                "-propconst": None,
                "-sweep": None,
                "-muxf_remap": None,
                "-aggressive_remap": None,
                "-shift_register_opt": None,
            },
            "place_opt2": {"-directive": "Explore"},
            "phys_opt": {"-directive": "AggressiveExplore"},
            "route": {"-directive": "NoTimingRelaxation"},
        },
        "ExtraTimingAltRouting": {
            "place": {"-directive": "ExtraTimingOpt"},
            "place_opt": {
                "-retarget": None,
                "-propconst": None,
                "-sweep": None,
                "-aggressive_remap": None,
                "-shift_register_opt": None,
            },
            "phys_opt": {"-directive": "AggressiveExplore"},
            "route": {"-directive": "AlternateCLBRouting"},
        },
        "Area": {
            "place": {"-directive": "Default"},
            "place_opt": {"-directive": "ExploreArea"},
            "phys_opt": {"-directive": "Explore"},
            "route": {"-directive": "Explore"},
        },
        "AreaHigh": {
            "place": {"-directive": "Default"},
            "place_opt": {"-directive": "ExploreArea"},
            "phys_opt": {"-directive": "Explore"},
            "route": {"-directive": "Explore"},
        },
        "AreaPower": {
            "place": {"-directive": "Default"},
            "place_opt": {
                "-retarget": None,
                "-propconst": None,
                "-sweep": None,
                "-aggressive_remap": None,
                "-shift_register_opt": None,
                "-dsp_register_opt": None,
                "-resynth_seq_area": None,
                "-merge_equivalent_drivers": None,
            },
            "place_opt2": {"-directive": "ExploreArea"},
            # FIXME!!! This is the only option that results in correct post-impl timing sim! Why??!
            "phys_opt": {"-directive": "AggressiveExplore"},
            "route": {"-directive": "Explore"},
        },
        "AreaTiming": {
            "place": {"-directive": "ExtraPostPlacementOpt"},
            "place_opt": {
                "-retarget": None,
                "-propconst": None,
                "-sweep": None,
                "-aggressive_remap": None,
                "-shift_register_opt": None,
                "-dsp_register_opt": None,
                "-resynth_seq_area": None,
                "-merge_equivalent_drivers": None,
            },
            "place_opt2": {"-directive": "ExploreArea"},
            "phys_opt": {"-directive": "AggressiveExplore"},
            "route": {"-directive": "Explore"},
        },
        "AreaExploreWithRemap": {
            "place": {"-directive": "Default"},
            "place_opt": {"-directive": "ExploreWithRemap"},
            "phys_opt": {"-directive": "Explore"},
            "route": {"-directive": "Explore"},
        },
        "AreaExploreWithRemap2": {
            "place": {"-directive": "Default"},
            "place_opt": {"-directive": "ExploreWithRemap"},
            "phys_opt": {"-directive": "Explore"},
            "route": {"-directive": "Explore"},
        },
        "AreaExplore": {
            "place": {"-directive": "Default"},
            "place_opt": {"-directive": "ExploreArea"},
            "phys_opt": {"-directive": "Explore"},
            "route": {"-directive": "Explore"},
        },
        "Power": {
            "place": {"-directive": "Default"},
            "place_opt": {"-directive": "ExploreSequentialArea"},
            # "power_opt": {},
            "phys_opt": {"-directive": "Explore"},
            "route": {"-directive": "Explore"},
        },
    },
}


class VivadoAltSynth(VivadoSynth, FpgaSynthFlow):
    """Synthesize with Xilinx Vivado using an alternative TCL-based flow"""

    class Settings(VivadoSynth.Settings):
        synth: RunOptions = RunOptions(strategy="Default")
        impl: RunOptions = RunOptions(strategy="Default")

        @validator("synth", "impl", always=True)
        def validate_synth(cls, value, values, field):
            if value.strategy:
                strategy_steps = strategies[field.name].get(value.strategy)
                if strategy_steps is None:
                    raise ValueError(f"Unknown strategy: {value.strategy}")
                value.steps = {
                    **strategy_steps,
                    **value.steps,
                }
            if field.name == "synth":
                steps = ["synth", "opt", "power_opt"]
            else:
                steps = [
                    "place",
                    "power_opt",
                    "place_opt",
                    "place_opt2",
                    "phys_opt",
                    "phys_opt2",
                    "route",
                ]
            for step in steps:
                if step not in value.steps:
                    value.steps[step] = None
            return value

        suppress_msgs: List[str] = [
            "Vivado 12-7122",  # Auto Incremental Compile:: No reference checkpoint was found in run
            "Synth 8-7080",  # "Parallel synthesis criteria is not met"
            "Synth 8-350",  # warning partial connection
            "Synth 8-256",  # info do synthesis
            "Synth 8-638",
            # "Synth 8-3969", # BRAM mapped to LUT due to optimization
            # "Synth 8-4480", # BRAM with no output register
            # "Drc 23-20",  # DSP without input pipelining
            # "Netlist 29-345",  # Update IP version
        ]

    def run(self):
        ss = self.settings
        assert isinstance(ss, self.Settings)

        if ss.out_of_context:
            if "synth" in ss.synth.steps and ss.synth.steps["synth"] is not None:
                ss.synth.steps["synth"]["-mode"] = "out_of_context"

        # always need a synth step?
        synth_steps = ss.synth.steps.get("synth")
        if synth_steps is None:
            synth_steps = {}
        if any(x in ss.blacklisted_resources for x in ("bram_tile", "bram")):
            # FIXME also add "-max_uram 0", only for UltraScale+ devices
            synth_steps["-max_bram"] = 0
        if "dsp" in ss.blacklisted_resources:
            synth_steps["-max_dsp"] = 0
        ss.synth.steps["synth"] = synth_steps

        def flatten_dict(d):
            return " ".join([f"{k} {v}" if v is not None else k for k, v in d.items()])

        def steps_to_str(steps):
            return "\n " + "\n ".join(
                f"{name}: {flatten_dict(step)}" for name, step in steps.items() if step
            )

        log.info("Synthesis steps:%s", steps_to_str(ss.synth.steps))
        log.info("Implementation steps:%s", steps_to_str(ss.impl.steps))

        self.add_template_filter(
            "flatten_dict",
            flatten_dict,
        )
        clock_xdc_path = self.copy_from_template("clock.xdc")
        script_path = self.copy_from_template(
            "vivado_alt_synth.tcl",
            xdc_files=[clock_xdc_path],
        )

        self.vivado.run("-source", script_path)
