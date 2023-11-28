#!/usr/bin/env python3

import itertools
import os
from pathlib import Path

from geometrics.toolbox.twod_to_threed import TwoDToThreeD


def main(do):
    # define where we'll read shapes from
    try:
        wrk_dir = Path(__file__).parent
    except Exception as e:
        wrk_dir = Path(f"{Path.cwd()}{os.sep}dummy").parent
    sources = [
        wrk_dir.parent / "oxford" / "master.dxf",
        wrk_dir.parent / "oxford" / "derivatives" / "5x5_cluster_master.dxf",
        wrk_dir.parent / "oxford" / "derivatives" / "4x4_cluster_master.dxf",
        wrk_dir.parent / "oxford" / "derivatives" / "hoye_evap.dxf",
    ]

    # instructions for 2d->3d
    lightmask_thickness = 0.45
    support_thickness = 0.75
    feature_thickness = 0.2
    shim_thickness = 0.05
    shim_thickness_thicker = 0.1
    glass_thickness = 1.1
    device_layer_scale_factor = 10000
    tco_thickness = 60e-6 * device_layer_scale_factor
    active_thickness = 600e-6 * device_layer_scale_factor
    metal_thickness = 100e-6 * device_layer_scale_factor
    contact_cylinder_height = tco_thickness + active_thickness + metal_thickness
    angle = 30

    support_color = "GOLDENROD"
    feature_color = "GRAY55"
    shim_color = "DARKGREEN"
    lightmask_color = "BLACK"

    glass_color = "CYAN"
    tco_color = "RED"

    # define how we'll tile things
    spacing5 = 30
    array5 = [(x * spacing5, y * spacing5, 0) for x, y in itertools.product(range(-2, 3), range(-2, 3))]

    spacing4 = 34.04
    array4 = [((x + 0.5) * spacing4, (y + 0.5) * spacing4, 0) for x, y in itertools.product(range(-2, 2), range(-2, 2))]
    # array4 = array4[5:6]

    instructions = []

    instructions.append(
        {
            "name": "hoye_metal_stack_5x",
            "layers": [
                # {
                #     "name": "shelf_riser",
                #     "color": shim_color,
                #     "thickness": 1.95,
                #     "drawing_layer_names": [
                #         "hoye_holder_extents",
                #         "shelf_riser",
                #     ],
                # },
                {
                    "name": "support",
                    "color": support_color,
                    "thickness": 0.75,
                    "drawing_layer_names": [
                        "hoye_holder_extents",
                        "hoye_metal_support",
                    ],
                },
                {
                    "name": "feature",
                    "color": feature_color,
                    "thickness": 0.2,
                    "drawing_layer_names": [
                        "hoye_holder_extents",
                        "hoye_metal_feature",
                    ],
                },
                {
                    "name": "shim",
                    "color": shim_color,
                    "thickness": 0.1,
                    "drawing_layer_names": [
                        "hoye_holder_extents",
                        "hoye_shim",
                    ],
                },
                {
                    "name": "holder",
                    "color": feature_color,
                    "thickness": 2,
                    "drawing_layer_names": [
                        "hoye_holder_extents",
                        "hoye_holder",
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "one_large_lightmask",
            "layers": [
                {
                    "name": "black_anodized_Al",
                    "color": lightmask_color,
                    "thickness": lightmask_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "lightmask_small_upper",
                        "lightmask_large_lower",
                        "lightmask_large_lower_tiny",
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "two_large_lightmask",
            "layers": [
                {
                    "name": "lightholes",
                    "color": lightmask_color,
                    "thickness": lightmask_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "lightmask_large_upper",
                        "lightmask_large_lower",
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "no_large_lightmask",
            "layers": [
                {
                    "name": "lightholes",
                    "color": lightmask_color,
                    "thickness": lightmask_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "lightmask_small_upper",
                        "lightmask_small_lower",
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "tco_150x150mm",
            "layers": [
                {
                    "name": "cluster_sheet",
                    "color": glass_color,
                    "thickness": glass_thickness,
                    "drawing_layer_names": [
                        "cluster_sheet",
                    ],
                },
                {
                    "name": "cluster_tco",
                    "color": tco_color,
                    "thickness": tco_thickness,
                    "drawing_layer_names": [
                        "tc_etch_chemical",
                    ],
                    "array": array5,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "tco_30x30mm",
            "layers": [
                {
                    "name": "glass_piece",
                    "color": glass_color,
                    "thickness": glass_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                    ],
                },
                {
                    "name": "tco",
                    "color": tco_color,
                    "thickness": tco_thickness,
                    "drawing_layer_names": [
                        "tc_etch_chemical",
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "active_mask_stack",
            "layers": [
                {
                    "name": "active_support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "aggressive_support_active",
                    ],
                },
                {
                    "name": "active_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "active_layer_upper",
                        "active_layer_lower",
                    ],
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "spacer_shim_thin",
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "active_mask_loft",
            "layers": [
                {
                    "name": "single_piece_mask",
                    "color": feature_color,
                    "thickness": 1.0,
                    "edm_dent": "spacer_shim_active",
                    "edm_dent_depth": 0.05,
                    "drawing_layer_names": [
                        "glass_extents",
                        ("active_layer_upper", "active_layer_upper_loft"),
                        ("active_layer_lower", "active_layer_lower_loft"),
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "active_mask_stack_5x5",
            "layers": [
                {
                    "name": "active_support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "outline_loose_alignment_5x5",
                        "aggressive_support_active",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
                {
                    "name": "active_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_5x5",
                        "active_layer_upper",
                        "active_layer_lower",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "outline_no_alignment_5x5",
                        "spacer_shim_thin",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "active_mask_stack_4x4",
            "layers": [
                {
                    "name": "active_support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "outline_loose_alignment_4x4",
                        "aggressive_support_active",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "active_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_4x4",
                        "active_layer_upper",
                        "active_layer_lower",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "outline_no_alignment_4x4",
                        "spacer_shim_thin",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "metal2_mask_stack",
            "layers": [
                {
                    "name": "support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "aggressive_metal_support_tc_metal",
                        "aggressive_metal_support_large_upper",
                        "aggressive_metal_support_large_lower",
                    ],
                },
                {
                    "name": "feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "tc_metal",
                        "pixel_electrodes_large_upper_2",
                        "pixel_electrodes_large_upper_4",
                        "pixel_electrodes_large_upper_6",
                        "pixel_electrodes_large_lower_1",
                        "pixel_electrodes_large_lower_3",
                        "pixel_electrodes_large_lower_5",
                    ],
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "spacer_shim_thin",
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "metal2_mask_loft",
            "layers": [
                {
                    "name": "single_piece_mask",
                    "color": feature_color,
                    "thickness": 1.0,
                    "edm_dent": "spacer_shim_thick",
                    "edm_dent_depth": 0.05,
                    "drawing_layer_names": [
                        "glass_extents",
                        "tc_metal",
                        ("pixel_electrodes_large_upper_2_edm", "pixel_electrodes_large_upper_2_loft"),
                        ("pixel_electrodes_large_upper_4", "pixel_electrodes_large_upper_4_loft"),
                        ("pixel_electrodes_large_upper_6_edm", "pixel_electrodes_large_upper_6_loft"),
                        ("pixel_electrodes_large_lower_1_edm", "pixel_electrodes_large_lower_1_loft"),
                        ("pixel_electrodes_large_lower_3", "pixel_electrodes_large_lower_3_loft"),
                        ("pixel_electrodes_large_lower_5_edm", "pixel_electrodes_large_lower_5_loft"),
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "metal2_mask_angle",
            "layers": [
                {
                    "name": "single_piece_mask",
                    "color": feature_color,
                    "thickness": 1.0,
                    "edm_dent": "spacer_shim_thick",
                    "edm_dent_depth": 0.05,
                    "drawing_layer_names": [
                        "glass_extents",
                        "tc_metal",
                        # ("pixel_electrodes_large_upper_edm_2", "pixel_electrodes_large_upper_2_loft"),
                        # ("pixel_electrodes_small_upper_4", "pixel_electrodes_large_upper_4_loft"),
                        # ("pixel_electrodes_large_upper_edm_6", "pixel_electrodes_large_upper_6_loft"),
                        ("pixel_electrodes_large_upper_edm_high_res", -angle),
                        "pixel_electrodes_large_upper_edm",
                        # ("pixel_electrodes_large_lower_edm_1", "pixel_electrodes_large_lower_1_loft"),
                        # ("pixel_electrodes_large_lower_3", "pixel_electrodes_large_lower_3_loft"),
                        # ("pixel_electrodes_large_lower_edm_5", "pixel_electrodes_large_lower_5_loft"),
                        ("pixel_electrodes_large_lower_edm_high_res", -angle),
                        "pixel_electrodes_large_lower_edm",
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "metal2_mask_angle_5x5",
            "layers": [
                {
                    "name": "single_piece_mask",
                    "color": feature_color,
                    "thickness": 1.0,
                    "edm_dent": "spacer_shim_thick",
                    "edm_dent_depth": 0.05,
                    "drawing_layer_names": [
                        "outline_5x5",
                        "tc_metal",
                        # ("pixel_electrodes_large_upper_edm_2", "pixel_electrodes_large_upper_2_loft"),
                        # ("pixel_electrodes_small_upper_4", "pixel_electrodes_large_upper_4_loft"),
                        # ("pixel_electrodes_large_upper_edm_6", "pixel_electrodes_large_upper_6_loft"),
                        ("pixel_electrodes_large_upper_edm_high_res", -angle),
                        "pixel_electrodes_large_upper_edm",
                        # ("pixel_electrodes_large_lower_edm_1", "pixel_electrodes_large_lower_1_loft"),
                        # ("pixel_electrodes_large_lower_3", "pixel_electrodes_large_lower_3_loft"),
                        # ("pixel_electrodes_large_lower_edm_5", "pixel_electrodes_large_lower_5_loft"),
                        ("pixel_electrodes_large_lower_edm_high_res", -angle),
                        "pixel_electrodes_large_lower_edm",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "metal2_mask_stack_5x5",
            "layers": [
                {
                    "name": "support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "outline_loose_alignment_5x5",
                        "aggressive_metal_support_tc_metal",
                        "aggressive_metal_support_large_upper",
                        "aggressive_metal_support_large_lower",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
                {
                    "name": "feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_5x5",
                        "tc_metal",
                        "pixel_electrodes_large_upper_2",
                        "pixel_electrodes_large_upper_4",
                        "pixel_electrodes_large_upper_6",
                        "pixel_electrodes_large_lower_1",
                        "pixel_electrodes_large_lower_3",
                        "pixel_electrodes_large_lower_5",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "outline_no_alignment_5x5",
                        "spacer_shim_thin",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "metal2_mask_stack_4x4",
            "layers": [
                {
                    "name": "support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "outline_loose_alignment_4x4",
                        "aggressive_metal_support_tc_metal",
                        "aggressive_metal_support_large_upper",
                        "aggressive_metal_support_large_lower",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_4x4",
                        "tc_metal",
                        "pixel_electrodes_large_upper_2",
                        "pixel_electrodes_large_upper_4",
                        "pixel_electrodes_large_upper_6",
                        "pixel_electrodes_large_lower_1",
                        "pixel_electrodes_large_lower_3",
                        "pixel_electrodes_large_lower_5",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "outline_no_alignment_4x4",
                        "spacer_shim_thin",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "led_metal_mask_stack",
            "layers": [
                {
                    "name": "support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "led_electrode_support",
                    ],
                },
                {
                    "name": "feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "tc_metal_led",
                        "led_electrode_1",
                        "led_electrode_2",
                        "led_electrode_3",
                        "led_electrode_4",
                        "led_electrode_5",
                        "led_electrode_6",
                    ],
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "spacer_shim_thin",
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "led_metal_mask_stack_5x5",
            "layers": [
                {
                    "name": "support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "outline_loose_alignment_5x5",
                        "led_electrode_support",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
                {
                    "name": "feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_5x5",
                        "tc_metal_led",
                        "led_electrode_1",
                        "led_electrode_2",
                        "led_electrode_3",
                        "led_electrode_4",
                        "led_electrode_5",
                        "led_electrode_6",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "outline_no_alignment_5x5",
                        "spacer_shim_thin",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "led_metal_mask_stack_4x4",
            "layers": [
                {
                    "name": "support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "outline_loose_alignment_4x4",
                        "led_electrode_support",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_4x4",
                        "tc_metal_led",
                        "led_electrode_1",
                        "led_electrode_2",
                        "led_electrode_3",
                        "led_electrode_4",
                        "led_electrode_5",
                        "led_electrode_6",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "outline_no_alignment_4x4",
                        "spacer_shim_thin",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "metal_mask_stack",
            "layers": [
                {
                    "name": "support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "aggressive_metal_support_tc_metal",
                        "aggressive_metal_support_small_upper",
                        "aggressive_metal_support_large_lower",
                    ],
                },
                {
                    "name": "feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "tc_metal",
                        "pixel_electrodes_small_upper_2",
                        "pixel_electrodes_small_upper_4",
                        "pixel_electrodes_small_upper_6",
                        "pixel_electrodes_large_lower_1",
                        "pixel_electrodes_large_lower_3",
                        "pixel_electrodes_large_lower_5",
                    ],
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "spacer_shim_thin",
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "metal_mask_stack_thick_shim",
            "layers": [
                {
                    "name": "support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "aggressive_metal_support_tc_metal",
                        "aggressive_metal_support_small_upper",
                        "aggressive_metal_support_large_lower",
                    ],
                },
                {
                    "name": "feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "tc_metal",
                        "pixel_electrodes_small_upper_2",
                        "pixel_electrodes_small_upper_4",
                        "pixel_electrodes_small_upper_6",
                        "pixel_electrodes_large_lower_1",
                        "pixel_electrodes_large_lower_3",
                        "pixel_electrodes_large_lower_5",
                    ],
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness_thicker,
                    "drawing_layer_names": [
                        "glass_extents",
                        "spacer_shim_thin",
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "metal_mask_loft",
            "layers": [
                {
                    "name": "single_piece_mask",
                    "color": feature_color,
                    "thickness": 1.0,
                    "edm_dent": "spacer_shim_thick",
                    "edm_dent_depth": 0.05,
                    "drawing_layer_names": [
                        "glass_extents",
                        "tc_metal",
                        ("pixel_electrodes_small_upper_2", "pixel_electrodes_small_upper_2_loft"),
                        ("pixel_electrodes_small_upper_4", "pixel_electrodes_small_upper_4_loft"),
                        ("pixel_electrodes_small_upper_6", "pixel_electrodes_small_upper_6_loft"),
                        ("pixel_electrodes_large_lower_1_edm", "pixel_electrodes_large_lower_1_loft"),
                        ("pixel_electrodes_large_lower_3", "pixel_electrodes_large_lower_3_loft"),
                        ("pixel_electrodes_large_lower_5_edm", "pixel_electrodes_large_lower_5_loft"),
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "metal_mask_angle",
            "layers": [
                {
                    "name": "single_piece_mask",
                    "color": feature_color,
                    "thickness": 1.0,
                    "edm_dent": "spacer_shim_thick",
                    "edm_dent_depth": 0.05,
                    "drawing_layer_names": [
                        "glass_extents",
                        "tc_metal",
                        # ("pixel_electrodes_small_upper_2", "pixel_electrodes_small_upper_2_loft"),
                        # ("pixel_electrodes_small_upper_4", "pixel_electrodes_small_upper_4_loft"),
                        # ("pixel_electrodes_small_upper_6", "pixel_electrodes_small_upper_6_loft"),
                        ("pixel_electrodes_small_upper_high_res", -angle),
                        "pixel_electrodes_small_upper_2",
                        "pixel_electrodes_small_upper_4",
                        "pixel_electrodes_small_upper_6",
                        # ("pixel_electrodes_large_lower_1", "pixel_electrodes_large_lower_1_loft"),
                        # ("pixel_electrodes_large_lower_3", "pixel_electrodes_large_lower_3_loft"),
                        # ("pixel_electrodes_large_lower_5", "pixel_electrodes_large_lower_5_loft"),
                        ("pixel_electrodes_large_lower_edm_high_res", -angle),
                        "pixel_electrodes_large_lower_edm",
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "metal_mask_angle_5x5",
            "layers": [
                {
                    "name": "single_piece_mask",
                    "color": feature_color,
                    "thickness": 1.0,
                    "edm_dent": "spacer_shim_thick",
                    "edm_dent_depth": 0.05,
                    "drawing_layer_names": [
                        "outline_5x5",
                        "tc_metal",
                        # ("pixel_electrodes_small_upper_2", "pixel_electrodes_small_upper_2_loft"),
                        # ("pixel_electrodes_small_upper_4", "pixel_electrodes_small_upper_4_loft"),
                        # ("pixel_electrodes_small_upper_6", "pixel_electrodes_small_upper_6_loft"),
                        ("pixel_electrodes_small_upper_high_res", -angle),
                        "pixel_electrodes_small_upper_2",
                        "pixel_electrodes_small_upper_4",
                        "pixel_electrodes_small_upper_6",
                        # ("pixel_electrodes_large_lower_1", "pixel_electrodes_large_lower_1_loft"),
                        # ("pixel_electrodes_large_lower_3", "pixel_electrodes_large_lower_3_loft"),
                        # ("pixel_electrodes_large_lower_5", "pixel_electrodes_large_lower_5_loft"),
                        ("pixel_electrodes_large_lower_edm_high_res", -angle),
                        "pixel_electrodes_large_lower_edm",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "metal_mask_loft_5x5",
            "layers": [
                {
                    "name": "single_piece_mask",
                    "color": feature_color,
                    "thickness": 1.0,
                    "edm_dent": "spacer_shim_thick",
                    "edm_dent_depth": 0.05,
                    "drawing_layer_names": [
                        "outline_5x5",
                        "tc_metal",
                        ("pixel_electrodes_small_upper_2", "pixel_electrodes_small_upper_2_loft"),
                        ("pixel_electrodes_small_upper_4", "pixel_electrodes_small_upper_4_loft"),
                        ("pixel_electrodes_small_upper_6", "pixel_electrodes_small_upper_6_loft"),
                        ("pixel_electrodes_large_lower_1_edm", "pixel_electrodes_large_lower_1_loft"),
                        ("pixel_electrodes_large_lower_3", "pixel_electrodes_large_lower_3_loft"),
                        ("pixel_electrodes_large_lower_5_edm", "pixel_electrodes_large_lower_5_loft"),
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "metal_mask_stack_5x5",
            "layers": [
                {
                    "name": "support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "outline_loose_alignment_5x5",
                        "aggressive_metal_support_tc_metal",
                        "aggressive_metal_support_small_upper",
                        "aggressive_metal_support_large_lower",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
                {
                    "name": "feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_5x5",
                        "tc_metal",
                        "pixel_electrodes_small_upper_2",
                        "pixel_electrodes_small_upper_4",
                        "pixel_electrodes_small_upper_6",
                        "pixel_electrodes_large_lower_1",
                        "pixel_electrodes_large_lower_3",
                        "pixel_electrodes_large_lower_5",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "outline_no_alignment_5x5",
                        "spacer_shim_thin",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "metal_mask_loft_4x4",
            "layers": [
                {
                    "name": "single_piece_mask",
                    "color": feature_color,
                    "thickness": 1.0,
                    "edm_dent": "spacer_shim_thick",
                    "edm_dent_depth": 0.05,
                    "drawing_layer_names": [
                        "outline_4x4",
                        "tc_metal",
                        ("pixel_electrodes_small_upper_2", "pixel_electrodes_small_upper_2_loft"),
                        ("pixel_electrodes_small_upper_4", "pixel_electrodes_small_upper_4_loft"),
                        ("pixel_electrodes_small_upper_6", "pixel_electrodes_small_upper_6_loft"),
                        ("pixel_electrodes_large_lower_1_edm", "pixel_electrodes_large_lower_1_loft"),
                        ("pixel_electrodes_large_lower_3", "pixel_electrodes_large_lower_3_loft"),
                        ("pixel_electrodes_large_lower_5_edm", "pixel_electrodes_large_lower_5_loft"),
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "metal_mask_stack_4x4",
            "layers": [
                {
                    "name": "support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "outline_loose_alignment_4x4",
                        "aggressive_metal_support_tc_metal",
                        "aggressive_metal_support_small_upper",
                        "aggressive_metal_support_large_lower",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_4x4",
                        "tc_metal",
                        "pixel_electrodes_small_upper_2",
                        "pixel_electrodes_small_upper_4",
                        "pixel_electrodes_small_upper_6",
                        "pixel_electrodes_large_lower_1",
                        "pixel_electrodes_large_lower_3",
                        "pixel_electrodes_large_lower_5",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "outline_no_alignment_4x4",
                        "spacer_shim_thin",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "metal6_mask_stack",
            "layers": [
                {
                    "name": "support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "aggressive_metal_support_tc_metal",
                        "aggressive_metal_support_small_upper",
                        "aggressive_metal_support_small_lower",
                    ],
                },
                {
                    "name": "feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "tc_metal",
                        "pixel_electrodes_small_upper_2",
                        "pixel_electrodes_small_upper_4",
                        "pixel_electrodes_small_upper_6",
                        "pixel_electrodes_small_lower_1",
                        "pixel_electrodes_small_lower_3",
                        "pixel_electrodes_small_lower_5",
                    ],
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "spacer_shim_thin",
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "metal6_mask_stack_thick_shim",
            "layers": [
                {
                    "name": "support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "aggressive_metal_support_tc_metal",
                        "aggressive_metal_support_small_upper",
                        "aggressive_metal_support_small_lower",
                    ],
                },
                {
                    "name": "feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "tc_metal",
                        "pixel_electrodes_small_upper_2",
                        "pixel_electrodes_small_upper_4",
                        "pixel_electrodes_small_upper_6",
                        "pixel_electrodes_small_lower_1",
                        "pixel_electrodes_small_lower_3",
                        "pixel_electrodes_small_lower_5",
                    ],
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness_thicker,
                    "drawing_layer_names": [
                        "glass_extents",
                        "spacer_shim_thin",
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "metal6_mask_loft",
            "layers": [
                {
                    "name": "single_piece_mask",
                    "color": feature_color,
                    "thickness": 1.0,
                    "edm_dent": "spacer_shim_thick",
                    "edm_dent_depth": 0.05,
                    "drawing_layer_names": [
                        "glass_extents",
                        "tc_metal",
                        ("pixel_electrodes_small_upper_2", "pixel_electrodes_small_upper_2_loft"),
                        ("pixel_electrodes_small_upper_4", "pixel_electrodes_small_upper_4_loft"),
                        ("pixel_electrodes_small_upper_6", "pixel_electrodes_small_upper_6_loft"),
                        ("pixel_electrodes_small_lower_1", "pixel_electrodes_small_lower_1_loft"),
                        ("pixel_electrodes_small_lower_3", "pixel_electrodes_small_lower_3_loft"),
                        ("pixel_electrodes_small_lower_5", "pixel_electrodes_small_lower_5_loft"),
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "metal6_mask_angle",
            "layers": [
                {
                    "name": "single_piece_mask",
                    "color": feature_color,
                    "thickness": 1.0,
                    "edm_dent": "spacer_shim_thick",
                    "edm_dent_depth": 0.05,
                    "drawing_layer_names": [
                        "glass_extents",
                        "tc_metal",
                        # ("pixel_electrodes_small_upper_2", "pixel_electrodes_small_upper_2_loft"),
                        # ("pixel_electrodes_small_upper_4", "pixel_electrodes_small_upper_4_loft"),
                        # ("pixel_electrodes_small_upper_6", "pixel_electrodes_small_upper_6_loft"),
                        ("pixel_electrodes_small_upper_high_res", -angle),
                        "pixel_electrodes_small_upper_2",
                        "pixel_electrodes_small_upper_4",
                        "pixel_electrodes_small_upper_6",
                        # ("pixel_electrodes_small_lower_1", "pixel_electrodes_small_lower_1_loft"),
                        # ("pixel_electrodes_small_lower_3", "pixel_electrodes_small_lower_3_loft"),
                        # ("pixel_electrodes_small_lower_5", "pixel_electrodes_small_lower_5_loft"),
                        ("pixel_electrodes_small_lower_high_res", -angle),
                        "pixel_electrodes_small_lower_1",
                        "pixel_electrodes_small_lower_3",
                        "pixel_electrodes_small_lower_5",
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "metal6_mask_angle_5x5",
            "layers": [
                {
                    "name": "single_piece_mask",
                    "color": feature_color,
                    "thickness": 1.0,
                    "edm_dent": "spacer_shim_thick",
                    "edm_dent_depth": 0.05,
                    "drawing_layer_names": [
                        "outline_5x5",
                        "tc_metal",
                        # ("pixel_electrodes_small_upper_2", "pixel_electrodes_small_upper_2_loft"),
                        # ("pixel_electrodes_small_upper_4", "pixel_electrodes_small_upper_4_loft"),
                        # ("pixel_electrodes_small_upper_6", "pixel_electrodes_small_upper_6_loft"),
                        ("pixel_electrodes_small_upper_high_res", -angle),
                        "pixel_electrodes_small_upper_2",
                        "pixel_electrodes_small_upper_4",
                        "pixel_electrodes_small_upper_6",
                        # ("pixel_electrodes_small_lower_1", "pixel_electrodes_small_lower_1_loft"),
                        # ("pixel_electrodes_small_lower_3", "pixel_electrodes_small_lower_3_loft"),
                        # ("pixel_electrodes_small_lower_5", "pixel_electrodes_small_lower_5_loft"),
                        ("pixel_electrodes_small_lower_high_res", -angle),
                        "pixel_electrodes_small_lower_1",
                        "pixel_electrodes_small_lower_3",
                        "pixel_electrodes_small_lower_5",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "metal6_mask_stack_5x5",
            "layers": [
                {
                    "name": "support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "outline_loose_alignment_5x5",
                        "aggressive_metal_support_tc_metal",
                        "aggressive_metal_support_small_upper",
                        "aggressive_metal_support_small_lower",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
                {
                    "name": "feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_5x5",
                        "tc_metal",
                        "pixel_electrodes_small_upper_2",
                        "pixel_electrodes_small_upper_4",
                        "pixel_electrodes_small_upper_6",
                        "pixel_electrodes_small_lower_1",
                        "pixel_electrodes_small_lower_3",
                        "pixel_electrodes_small_lower_5",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "outline_no_alignment_5x5",
                        "spacer_shim_thin",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "metal6_mask_stack_4x4",
            "layers": [
                {
                    "name": "support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "outline_loose_alignment_4x4",
                        "aggressive_metal_support_tc_metal",
                        "aggressive_metal_support_small_upper",
                        "aggressive_metal_support_small_lower",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_4x4",
                        "tc_metal",
                        "pixel_electrodes_small_upper_2",
                        "pixel_electrodes_small_upper_4",
                        "pixel_electrodes_small_upper_6",
                        "pixel_electrodes_small_lower_1",
                        "pixel_electrodes_small_lower_3",
                        "pixel_electrodes_small_lower_5",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "outline_no_alignment_4x4",
                        "spacer_shim_thin",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "contact_insulation_4x4",
            "layers": [
                {
                    "name": "support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "outline_loose_alignment_4x4",
                        "contact_insulation_support",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_4x4",
                        "contact_insulation",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "outline_no_alignment_4x4",
                        "spacer_shim_thin",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "vapor_deposition_encapsulation",
            "layers": [
                {
                    "name": "support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "v_dep_encap_spt",
                    ],
                },
                {
                    "name": "feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "v_dep_encap",
                    ],
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "spacer_shim_thin",
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "vapor_deposition_encapsulation_4x4",
            "layers": [
                {
                    "name": "support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "outline_loose_alignment_4x4",
                        "v_dep_encap_spt",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_4x4",
                        "v_dep_encap",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "outline_no_alignment_4x4",
                        "spacer_shim_thin",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "tc_mask_4x4",
            "layers": [
                {
                    "name": "support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "outline_loose_alignment_4x4",
                        "tc_mask_support",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_4x4",
                        "tc_mask",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "outline_no_alignment_4x4",
                        "spacer_shim_thin",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "tc_undermetal_mask_4x4",
            "layers": [
                {
                    "name": "support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "outline_loose_alignment_4x4",
                        "tc_mask_support",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_4x4",
                        "tc_undermetal",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "outline_no_alignment_4x4",
                        "spacer_shim_thin",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "full_top_tco_angle",
            "layers": [
                {
                    "name": "single_piece_mask",
                    "color": feature_color,
                    "thickness": 1,
                    "drawing_layer_names": [
                        "glass_extents",
                        ("full_area_top_tco", -angle),
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "full_top_tco_angle_4x4",
            "layers": [
                {
                    "name": "single_piece_mask",
                    "color": feature_color,
                    "thickness": 1.0,
                    #"edm_dent": "spacer_shim_active",
                    #"edm_dent_depth": 0.05,
                    "drawing_layer_names": [
                        "outline_4x4",
                        ("full_area_top_tco", -angle),
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "full_insulation_angle_4x4",
            "layers": [
                {
                    "name": "single_piece_mask",
                    "color": feature_color,
                    "thickness": 1.0,
                    #"edm_dent": "spacer_shim_active",
                    #"edm_dent_depth": 0.05,
                    "drawing_layer_names": [
                        "outline_4x4",
                        ("full_area_insulation", -angle),
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "full_interlayer_angle_4x4",
            "layers": [
                {
                    "name": "single_piece_mask",
                    "color": feature_color,
                    "thickness": 1.0,
                    #"edm_dent": "spacer_shim_active",
                    #"edm_dent_depth": 0.05,
                    "drawing_layer_names": [
                        "outline_4x4",
                        ("full_area_recombination_slash_interlayer", -angle),
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "lightmask_cal_angle",
            "layers": [
                {
                    "name": "single_piece_mask",
                    "color": feature_color,
                    "thickness": 0.4,
                    "drawing_layer_names": [
                        "glass_extents",
                        ("lightmask_cal_small_upper", -angle),
                        ("lightmask_cal_large_lower", -angle),
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "full_metal_angle",
            "layers": [
                {
                    "name": "single_piece_mask",
                    "color": feature_color,
                    "thickness": 1,
                    "drawing_layer_names": [
                        "glass_extents",
                        ("full_area_metal", -angle),
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "full_metal",
            "layers": [
                {
                    "name": "single_piece_mask",
                    "color": feature_color,
                    "thickness": 1,
                    "drawing_layer_names": [
                        "glass_extents",
                        "full_area_metal_20x20",
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "full_metal_angle_4x4",
            "layers": [
                {
                    "name": "single_piece_mask",
                    "color": feature_color,
                    "thickness": 1.0,
                    "edm_dent": "spacer_shim_thin",
                    "edm_dent_depth": 0.05,
                    "drawing_layer_names": [
                        "outline_4x4",
                        ("full_area_metal", -angle),
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "interlayer2_mask_stack",
            "layers": [
                {
                    "name": "interlayer_support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "aggressive_support_recombi",
                    ],
                },
                {
                    "name": "inerlayer_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "recombination_slash_interlayer2",
                    ],
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "spacer_shim_thin",
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "interlayer2_mask_stack_4x4",
            "layers": [
                {
                    "name": "interlayer_support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "outline_loose_alignment_4x4",
                        "aggressive_support_recombi",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "inerlayer_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_4x4",
                        "recombination_slash_interlayer2",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "outline_no_alignment_4x4",
                        "spacer_shim_thin",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "interlayer_mask_stack",
            "layers": [
                {
                    "name": "interlayer_support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "aggressive_support_recombi",
                    ],
                },
                {
                    "name": "inerlayer_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "recombination_slash_interlayer",
                    ],
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "spacer_shim_thin",
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "interlayer_mask_angle",
            "layers": [
                {
                    "name": "single_piece_mask",
                    "color": feature_color,
                    "thickness": 1.0,
                    "edm_dent": "spacer_shim_thick",
                    "edm_dent_depth": 0.05,
                    "drawing_layer_names": [
                        "glass_extents",
                        ("recombination_slash_interlayer", -angle),
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "interlayer_mask_stack_5x5",
            "layers": [
                {
                    "name": "interlayer_support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "outline_loose_alignment_5x5",
                        "aggressive_support_recombi",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
                {
                    "name": "inerlayer_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_5x5",
                        "recombination_slash_interlayer",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "outline_no_alignment_5x5",
                        "spacer_shim_thin",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "interlayer_mask_angle_4x4",
            "layers": [
                {
                    "name": "single_piece_mask",
                    "color": feature_color,
                    "thickness": 1.0,
                    "edm_dent": "spacer_shim_active",
                    "edm_dent_depth": 0.05,
                    "drawing_layer_names": [
                        "outline_4x4",
                        ("recombination_slash_interlayer", -angle),
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "interlayer_mask_stack_4x4",
            "layers": [
                {
                    "name": "interlayer_support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "outline_loose_alignment_4x4",
                        "aggressive_support_recombi",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "inerlayer_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_4x4",
                        "recombination_slash_interlayer",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "outline_no_alignment_4x4",
                        "spacer_shim_thin",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "top_tco2_mask_stack_4x4",
            "layers": [
                {
                    "name": "top_tco_support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "outline_loose_alignment_4x4",
                        "aggressive_support_tandem",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "top_tco_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_4x4",
                        "top_tco_large_lower",
                        "top_tco_large_upper",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "outline_no_alignment_4x4",
                        "spacer_shim_thin",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "top_tco_mask_stack",
            "layers": [
                {
                    "name": "top_tco_support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "aggressive_support_tandem",
                    ],
                },
                {
                    "name": "top_tco_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "top_tco_large_lower",
                        "top_tco_small_upper",
                    ],
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "spacer_shim_thin",
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "top_tco_mask_stack_5x5",
            "layers": [
                {
                    "name": "top_tco_support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "outline_loose_alignment_5x5",
                        "aggressive_support_tandem",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
                {
                    "name": "top_tco_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_5x5",
                        "top_tco_large_lower",
                        "top_tco_small_upper",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "outline_no_alignment_5x5",
                        "spacer_shim_thin",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "top_tco_mask_stack_4x4",
            "layers": [
                {
                    "name": "top_tco_support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "outline_loose_alignment_4x4",
                        "aggressive_support_tandem",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "top_tco_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_4x4",
                        "top_tco_large_lower",
                        "top_tco_small_upper",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "outline_no_alignment_4x4",
                        "spacer_shim_thin",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
            ],
        }
    )

    # NOTE this design is a fail. it shadows the fingers
    instructions.append(
        {
            "name": "flappy_tandem_metal_mask_stack",
            "layers": [
                {
                    "name": "tandem_metal_support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "aggressive_metal_support_tc_metal",
                        "aggressive_metal_support_small_upper_flappy",
                        "aggressive_metal_support_large_lower_flappy",
                    ],
                },
                {
                    "name": "tandem_metal_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "tc_metal",
                        "pixel_electrodes_small_upper_flappy",
                        "pixel_electrodes_large_lower_flappy",
                    ],
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "spacer_shim_thin",
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "tc_metal_mask_stack",
            "layers": [
                {
                    "name": "tandem_metal_support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "tc_metal_support",
                    ],
                },
                {
                    "name": "tandem_metal_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "tc_metal",
                    ],
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "spacer_shim_thin",
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "tc_metal_mask_stack_5x5",
            "layers": [
                {
                    "name": "tandem_metal_support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "outline_loose_alignment_5x5",
                        "tc_metal_support",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
                {
                    "name": "tandem_metal_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_5x5",
                        "tc_metal",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "outline_no_alignment_5x5",
                        "spacer_shim_thin",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "tc_metal_mask_stack_4x4",
            "layers": [
                {
                    "name": "tandem_metal_support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "outline_loose_alignment_4x4",
                        "tc_metal_support",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "tandem_metal_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_4x4",
                        "tc_metal",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "outline_no_alignment_4x4",
                        "spacer_shim_thin",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "tandem2_metal_mask_stack",
            "layers": [
                {
                    "name": "tandem_metal_support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "aggressive_support_tandem2_metal",
                    ],
                },
                {
                    "name": "tandem_metal_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "pixel_electrodes_large_upper_finger",
                        "pixel_electrodes_large_lower_finger",
                    ],
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "spacer_shim_thin",
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "tandem2_metal_mask_stack_4x4",
            "layers": [
                {
                    "name": "tandem_metal_support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "outline_loose_alignment_4x4",
                        "aggressive_support_tandem2_metal",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "tandem_metal_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_4x4",
                        "pixel_electrodes_large_upper_finger",
                        "pixel_electrodes_large_lower_finger",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "outline_no_alignment_4x4",
                        "spacer_shim_thin",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "tandem_metal_mask_stack",
            "layers": [
                {
                    "name": "tandem_metal_support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "aggressive_support_tandem_metal",
                    ],
                },
                {
                    "name": "tandem_metal_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "pixel_electrodes_small_upper_finger",
                        "pixel_electrodes_large_lower_finger",
                    ],
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "spacer_shim_thin",
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "tandem_metal_mask_stack_5x5",
            "layers": [
                {
                    "name": "tandem_metal_support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "outline_loose_alignment_5x5",
                        "aggressive_support_tandem_metal",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
                {
                    "name": "tandem_metal_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_5x5",
                        "pixel_electrodes_small_upper_finger",
                        "pixel_electrodes_large_lower_finger",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "outline_no_alignment_5x5",
                        "spacer_shim_thin",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "tandem_metal_mask_stack_4x4",
            "layers": [
                {
                    "name": "tandem_metal_support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "outline_loose_alignment_4x4",
                        "aggressive_support_tandem_metal",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "tandem_metal_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_4x4",
                        "pixel_electrodes_small_upper_finger",
                        "pixel_electrodes_large_lower_finger",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "outline_no_alignment_4x4",
                        "spacer_shim_thin",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "full_device_Stack",
            "layers": [
                {
                    "z_base": -glass_thickness,
                    "name": "glass_piece",
                    "color": glass_color,
                    "thickness": glass_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                    ],
                },
                {
                    "name": "tco",
                    "color": tco_color,
                    "thickness": tco_thickness,
                    "drawing_layer_names": [
                        "tc_etch_chemical",
                    ],
                },
                {
                    "name": "active_layer",
                    "color": "CHOCOLATE",
                    "thickness": active_thickness,
                    "drawing_layer_names": [
                        "active_layer_upper",
                        "active_layer_lower",
                    ],
                },
                {
                    "name": "small_pixels",
                    "color": "GOLD",
                    "thickness": metal_thickness,
                    "drawing_layer_names": [
                        "pixel_electrodes_small_lower_1",
                        "pixel_electrodes_small_lower_3",
                        "pixel_electrodes_small_lower_5",
                    ],
                },
                {
                    "name": "large_pixel",
                    "color": "GOLD",
                    "thickness": metal_thickness,
                    "z_base": tco_thickness + active_thickness,
                    "drawing_layer_names": [
                        "pixel_electrodes_large_upper_2",
                        "pixel_electrodes_large_upper_4",
                        "pixel_electrodes_large_upper_6",
                    ],
                },
                {
                    "name": "tc_metal",
                    "color": "GOLD",
                    "thickness": metal_thickness,
                    "z_base": tco_thickness,
                    "drawing_layer_names": [
                        "tc_metal",
                    ],
                },
                {
                    "name": "contact_points",
                    "color": "WHITE",
                    "z_base": 0,
                    "thickness": contact_cylinder_height,
                    "drawing_layer_names": [
                        "contact_pin_diameter",
                        # "contact_point",
                    ],
                },
                {
                    "name": "large_lightmask",
                    "color": "CHOCOLATE",
                    "thickness": active_thickness,
                    "z_base": tco_thickness,
                    "drawing_layer_names": [
                        "large_upper_current_gen",
                    ],
                },
                {
                    "name": "small_lightmask",
                    "color": "CHOCOLATE",
                    "thickness": active_thickness,
                    "z_base": tco_thickness,
                    "drawing_layer_names": [
                        "lightmask_small_lower",
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "sim_onesqcm_tandem",
            "xyscale": 1,
            "final_scale": 1/device_layer_scale_factor,
            "sim_mode": True,
            "layers": [
                # {
                #     "name": "current_gen",
                #     "color": "CHOCOLATE",
                #     "thickness": 0,
                #     "drawing_layer_names": [
                #         "lightmask_large_upper",
                #     ],
                # },
                {
                    "name": "tco",
                    "color": tco_color,
                    "z_base": 0,
                    "thickness": tco_thickness,
                    "drawing_layer_names": [
                        "top_tco_large_upper",
                        ("lightmask_large_upper", 0)  # zero here means drawing layer shape should be embossed onto the 3D layer
                    ],
                },
                {
                    "name": "metal",
                    "color": "GOLD",
                    "thickness": metal_thickness,
                    "drawing_layer_names": [
                        "pixel_electrodes_large_upper_finger",
                    ],
                },
                {
                    "name": "contact_cutter",
                    "color": "WHITE",
                    "z_base": 0,
                    "thickness": metal_thickness+tco_thickness,
                    "drawing_layer_names": [
                        "sim_neck_cutter_outer",
                    ],
                },
            ],
        }
    )

    if "masks" in do:
        ttt = TwoDToThreeD(instructions=instructions, sources=sources)
        # to_build = ["active_mask_stack", "metal_mask_stack", "tco_30x30mm", "active_mask_stack_4x4", "tco_150x150mm"]
        # to_build = ["tco_30x30mm"]
        #to_build = ["full_device_Stack"]
        to_build = ["sim_onesqcm_tandem"]
        # to_build = ["tandem_metal_mask_stack"]
        # to_build = ["metal_mask_stack"]
        # to_build = ["tc_metal_mask_stack", "tc_metal_mask_stack_5x5", "tc_metal_mask_stack_4x4"]
        # to_build = ["metal2_mask_stack", "metal2_mask_stack_4x4", "metal2_mask_stack_5x5", "one_big_lightmask"]
        # to_build = ["no_large_lightmask", "one_large_lightmask", "two_large_lightmask", "led_metal_mask_stack", "led_metal_mask_stack_5x5", "led_metal_mask_stack_4x4"]
        # to_build = ["no_large_lightmask", "one_large_lightmask", "two_large_lightmask", "led_metal_mask_stack"]
        # to_build = ["metal2_mask_angle", "metal2_mask_angle_5x5", "metal6_mask_angle"]  # all of them
        # to_build = ["metal2_mask_angle", "metal2_mask_angle_5x5", "metal6_mask_angle_5x5", "metal6_mask_angle"]
        # to_build = ["metal6_mask_angle_5x5"]
        # to_build = ["metal_mask_loft", "metal_mask_angle", "metal2_mask_angle", "metal6_mask_angle", "interlayer_mask_angle"]
        # to_build = ["metal_mask_loft", "metal6_mask_loft", "metal2_mask_loft"]
        # to_build = ["metal_mask_loft", "metal6_mask_loft", "metal2_mask_loft", "active_mask_loft", "interlayer_mask_angle", "interlayer_mask_angle_4x4", "interlayer_mask_stack_4x4"]
        # to_build = ["interlayer_mask_angle_4x4", "metal_mask_loft_4x4"]
        # to_build = ["metal_mask_loft_5x5"]
        # to_build = ["interlayer_mask_angle_4x4", "metal_mask_loft"]
        # to_build = ["full_metal_angle_4x4", "full_top_tco_angle_4x4", "full_insulation_angle_4x4", "full_interlayer_angle_4x4"]
        # to_build = ["full_metal_angle_4x4"]
        # to_build = ["lightmask_cal_angle"]
        # to_build = ["hoye_metal_stack_5x", "one_large_lightmask"]
        # to_build = ["tc_mask_4x4", "contact_insulation_4x4", "led_metal_mask_stack", "led_metal_mask_stack_4x4", "tandem2_metal_mask_stack_4x4", "interlayer2_mask_stack_4x4", "top_tco2_mask_stack_4x4", "vapor_deposition_encapsulation_4x4", "vapor_deposition_encapsulation", "tc_undermetal_mask_4x4", "active_mask_stack"]  # june order
        # to_build = ["vapor_deposition_encapsulation_4x4", "vapor_deposition_encapsulation", "tc_undermetal_mask_4x4", "active_mask_stack"]
        # to_build = ["metal_mask_stack_thick_shim"]
        # to_build = ["metal_mask_stack_4x4", "metal_mask_stack_thick_shim", "metal6_mask_stack_thick_shim", "metal2_mask_stack_4x4", "metal6_mask_stack_4x4", "interlayer_mask_stack_4x4", "active_mask_stack_4x4"]  # march order = [2, 60, 60, 2, 2, 2, 2]
        # to_build = ["metal_mask_stack_thick_shim"]
        # to_build = [""]  # all of them
        built = ttt.build(to_build, nparallel=12)

        TwoDToThreeD.outputter(built, wrk_dir, save_dxfs=True, save_pdfs=True, save_steps=True, save_stls=True, edm_outputs=True, nparallel=12)

        # ttt.faceputter(wrk_dir)  # output the face data for comsol

        # march order = [2, 60, 60, 2, 2, 2, 2]
        #march_build = ["metal_mask_stack_4x4", "metal_mask_stack_thick_shim", "metal6_mask_stack_thick_shim", "metal2_mask_stack_4x4", "metal6_mask_stack_4x4", "interlayer_mask_stack_4x4", "active_mask_stack_4x4"]
        # march_build = ["metal_mask_stack_thick_shim"]
        #march_built = ttt.build(march_build, nparallel=5)
        #TwoDToThreeD.outputter(march_built, wrk_dir, save_dxfs=True, save_steps=False, save_stls=False, edm_outputs=False, nparallel=6)

# temp is what we get when run via cq-editor
if __name__ in ["__main__", "temp"]:
    # define what to do
    do = ("masks",)

    main(do)
