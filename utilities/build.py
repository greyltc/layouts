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
    ]

    # instructions for 2d->3d
    lightmask_thickness = 0.45
    support_thickness = 0.75
    feature_thickness = 0.2
    shim_thickness = 0.05
    glass_thickness = 1.1
    device_layer_scale_factor = 10000
    tco_thickness = 140e-6 * device_layer_scale_factor
    active_thickness = 600e-6 * device_layer_scale_factor
    metal_thickness = 100e-6 * device_layer_scale_factor
    contact_cylinder_height = tco_thickness + active_thickness + metal_thickness

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

    instructions = []

    instructions.append(
        {
            "name": "one_large_lightmask",
            "layers": [
                {
                    "name": "lightholes",
                    "color": lightmask_color,
                    "thickness": lightmask_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "lightmask_small_upper",
                        "lightmask_large_lower",
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
                        "active_layer",
                    ],
                },
                {
                    "name": "spacer_shim",
                    "color": shim_color,
                    "thickness": shim_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "spacer_shim",
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
                        "active_layer",
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
                        "spacer_shim",
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
                        "active_layer",
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
                        "spacer_shim",
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
                    "name": "metal_support",
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
                    "name": "metal_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "tc_metal",
                        "pixel_electrodes_large_upper",
                        "pixel_electrodes_large_lower",
                    ],
                },
                {
                    "name": "spacer_shim_thin",
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
            "name": "metal2_mask_stack_edm",
            "layers": [
                {
                    "name": "metal_feature",
                    "color": feature_color,
                    "thickness": 1.0,
                    "edm_dent": ("spacer_shim_thick", 0.05),
                    "drawing_layer_names": [
                        "glass_extents",
                        "tc_metal",
                        "pixel_electrodes_large_lower_t1_a_edm_loft",
                        "pixel_electrodes_large_lower_t1_b_edm_loft",
                        "pixel_electrodes_large_lower_t2_a_edm_loft",
                        "pixel_electrodes_large_lower_t2_b_edm_loft",
                        "pixel_electrodes_large_lower_bp_a_edm_loft",
                        "pixel_electrodes_large_lower_bp_b_edm_loft",
                        "pixel_electrodes_large_upper_t1_a_edm_loft",
                        "pixel_electrodes_large_upper_t1_b_edm_loft",
                        "pixel_electrodes_large_upper_t2_a_edm_loft",
                        "pixel_electrodes_large_upper_t2_b_edm_loft",
                        "pixel_electrodes_large_upper_bp_a_edm_loft",
                        "pixel_electrodes_large_upper_bp_b_edm_loft",
                        "spacer_shim_thick",
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "metal2_mask_stack_edm_5x5",
            "layers": [
                {
                    "name": "metal_feature",
                    "color": feature_color,
                    "thickness": 1.0,
                    "edm_dent": ("spacer_shim_thick", 0.05),
                    "drawing_layer_names": [
                        "outline_5x5",
                        "tc_metal",
                        "pixel_electrodes_large_lower_t1_a_edm_loft",
                        "pixel_electrodes_large_lower_t1_b_edm_loft",
                        "pixel_electrodes_large_lower_t2_a_edm_loft",
                        "pixel_electrodes_large_lower_t2_b_edm_loft",
                        "pixel_electrodes_large_lower_bp_a_edm_loft",
                        "pixel_electrodes_large_lower_bp_b_edm_loft",
                        "pixel_electrodes_large_upper_t1_a_edm_loft",
                        "pixel_electrodes_large_upper_t1_b_edm_loft",
                        "pixel_electrodes_large_upper_t2_a_edm_loft",
                        "pixel_electrodes_large_upper_t2_b_edm_loft",
                        "pixel_electrodes_large_upper_bp_a_edm_loft",
                        "pixel_electrodes_large_upper_bp_b_edm_loft",
                        "spacer_shim_thick",
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
                    "name": "metal_support",
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
                    "name": "metal_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_5x5",
                        "tc_metal",
                        "pixel_electrodes_large_upper",
                        "pixel_electrodes_large_lower",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
                {
                    "name": "spacer_shim_thin",
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
                    "name": "metal_support",
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
                    "name": "metal_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_4x4",
                        "tc_metal",
                        "pixel_electrodes_large_upper",
                        "pixel_electrodes_large_lower",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "spacer_shim_thin",
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
                    "name": "metal_support",
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
                    "name": "metal_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "tc_metal",
                        "leds",
                    ],
                },
                {
                    "name": "spacer_shim_thin",
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
                    "name": "metal_support",
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
                    "name": "metal_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_5x5",
                        "tc_metal",
                        "leds",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
                {
                    "name": "spacer_shim_thin",
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
                    "name": "metal_support",
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
                    "name": "metal_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_4x4",
                        "tc_metal",
                        "leds",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "spacer_shim_thin",
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
                    "name": "metal_support",
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
                    "name": "metal_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "tc_metal",
                        "pixel_electrodes_small_upper",
                        "pixel_electrodes_large_lower",
                    ],
                },
                {
                    "name": "spacer_shim_thin",
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
            "name": "metal_mask_stack_5x5",
            "layers": [
                {
                    "name": "metal_support",
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
                    "name": "metal_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_5x5",
                        "tc_metal",
                        "pixel_electrodes_small_upper",
                        "pixel_electrodes_large_lower",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
                {
                    "name": "spacer_shim_thin",
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
            "name": "metal_mask_stack_4x4",
            "layers": [
                {
                    "name": "metal_support",
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
                    "name": "metal_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_4x4",
                        "tc_metal",
                        "pixel_electrodes_small_upper",
                        "pixel_electrodes_large_lower",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "spacer_shim_thin",
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
                    "name": "metal_support",
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
                    "name": "metal_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "glass_extents",
                        "tc_metal",
                        "pixel_electrodes_small_upper",
                        "pixel_electrodes_small_lower",
                    ],
                },
                {
                    "name": "spacer_shim_thin",
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
            "name": "metal6_mask_stack_edm",
            "layers": [
                {
                    "name": "metal_feature",
                    "color": feature_color,
                    "thickness": 1.0,
                    "edm_dent": ("spacer_shim_thick", 0.05),
                    "drawing_layer_names": [
                        "glass_extents",
                        "tc_metal",
                        "pixel_electrodes_small_lower_m1_a_edm_loft",
                        "pixel_electrodes_small_lower_m1_b_edm_loft",
                        "pixel_electrodes_small_lower_m2_a_edm_loft",
                        "pixel_electrodes_small_lower_m2_b_edm_loft",
                        "pixel_electrodes_small_lower_m3_a_edm_loft",
                        "pixel_electrodes_small_lower_m3_b_edm_loft",
                        "pixel_electrodes_small_upper_m1_a_edm_loft",
                        "pixel_electrodes_small_upper_m1_b_edm_loft",
                        "pixel_electrodes_small_upper_m2_a_edm_loft",
                        "pixel_electrodes_small_upper_m2_b_edm_loft",
                        "pixel_electrodes_small_upper_m3_a_edm_loft",
                        "pixel_electrodes_small_upper_m3_b_edm_loft",
                        "spacer_shim_thick",
                    ],
                },
            ],
        }
    )

    instructions.append(
        {
            "name": "metal6_mask_stack_5x5",
            "layers": [
                {
                    "name": "metal_support",
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
                    "name": "metal_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_5x5",
                        "tc_metal",
                        "pixel_electrodes_small_upper",
                        "pixel_electrodes_small_lower",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
                },
                {
                    "name": "spacer_shim_thin",
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
                    "name": "metal_support",
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
                    "name": "metal_feature",
                    "color": feature_color,
                    "thickness": feature_thickness,
                    "drawing_layer_names": [
                        "outline_4x4",
                        "tc_metal",
                        "pixel_electrodes_small_upper",
                        "pixel_electrodes_small_lower",
                    ],
                    "edge_case": "inner_outline_4x4",
                    "array": array4,
                },
                {
                    "name": "spacer_shim_thin",
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
                        "spacer_shim",
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
                        "spacer_shim",
                    ],
                    "edge_case": "inner_outline_5x5",
                    "array": array5,
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
                        "spacer_shim",
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
                    "name": "spacer_shim_thin",
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
                    "name": "spacer_shim_thin",
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
                    "name": "spacer_shim_thin",
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
                    "name": "spacer_shim_thin",
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
                    "name": "spacer_shim_thin",
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
                    "name": "spacer_shim_thin",
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
                    "name": "spacer_shim_thin",
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
                    "name": "spacer_shim_thin",
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
                    "name": "spacer_shim_thin",
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
                    "name": "spacer_shim_thin",
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
                        "active_layer",
                    ],
                },
                {
                    "name": "small_pixels",
                    "color": "GOLD",
                    "thickness": metal_thickness,
                    "drawing_layer_names": [
                        "pixel_electrodes_small_lower",
                    ],
                },
                {
                    "name": "large_pixel",
                    "color": "GOLD",
                    "thickness": metal_thickness,
                    "z_base": tco_thickness + active_thickness,
                    "drawing_layer_names": [
                        "pixel_electrodes_large_upper",
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

    if "masks" in do:
        ttt = TwoDToThreeD(instructions=instructions, sources=sources)
        # to_build = ["active_mask_stack", "metal_mask_stack", "tco_30x30mm", "active_mask_stack_4x4", "tco_150x150mm"]
        # to_build = ["tco_30x30mm"]
        # to_build = ["full_device_Stack"]
        # to_build = ["tandem_metal_mask_stack"]
        # to_build = ["metal_mask_stack"]
        # to_build = ["tc_metal_mask_stack", "tc_metal_mask_stack_5x5", "tc_metal_mask_stack_4x4"]
        # to_build = ["metal2_mask_stack", "metal2_mask_stack_4x4", "metal2_mask_stack_5x5", "one_big_lightmask"]
        # to_build = ["no_large_lightmask", "one_large_lightmask", "two_large_lightmask", "led_metal_mask_stack", "led_metal_mask_stack_5x5", "led_metal_mask_stack_4x4"]
        # to_build = ["no_large_lightmask", "one_large_lightmask", "two_large_lightmask", "led_metal_mask_stack"]
        to_build = ["metal2_mask_stack_edm", "metal2_mask_stack_edm_5x5", "metal6_mask_stack_edm"]  # all of them
        # to_build = [""]  # all of them
        asys = ttt.build(to_build, nparallel=5)

        # ttt.faceputter(wrk_dir)  # output the face data for comsol

        TwoDToThreeD.outputter(asys, wrk_dir, save_dxfs=True, save_steps=True, save_stls=False, nparallel=6)


# temp is what we get when run via cq-editor
if __name__ in ["__main__", "temp"]:
    # define what to do
    do = ("masks",)

    main(do)
