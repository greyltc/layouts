#!/usr/bin/env python3
import cadquery
from cadquery import CQ, cq
from pathlib import Path
from typing import List, Dict
import ezdxf
import itertools


class TwoDToThreeD(object):
    sources: List[Path]
    stacks: List[Dict]
    # dxf_filepath = Path(__file__).parent.parent / "oxford" / "master.dxf"  # this makes CQ-editor sad because __file__ is not defined

    def __init__(self, instructions: List[Dict], sources: List[Path]):
        self.stacks: List[Dict] = instructions
        self.sources: List[Path] = sources

    def build(self, stacks_to_build: List[str] = [""]):
        if stacks_to_build == [""]:  # build them all by default
            stacks_to_build = [x["name"] for x in self.stacks]

        drawing_layers_needed = []
        for stack_instructions in self.stacks:
            if stack_instructions["name"] in stacks_to_build:
                for stack_layer in stack_instructions["layers"]:
                    drawing_layers_needed += stack_layer["drawing_layer_names"]
                    if "edge_case" in stack_layer:
                        drawing_layers_needed.append(stack_layer["edge_case"])
        drawing_layers_needed_unique = list(set(drawing_layers_needed))

        # all the wires we'll need here
        wires = self.get_wires(self.sources, drawing_layers_needed_unique)

        stacks = {}
        for stack_instructions in self.stacks:
            # asy = cadquery.Assembly()
            asy = None
            if stack_instructions["name"] in stacks_to_build:
                # asy.name = stack_instructions["name"]
                z_base = 0
                for stack_layer in stack_instructions["layers"]:
                    t = stack_layer["thickness"]
                    boundary_layer_name = stack_layer["drawing_layer_names"][0]  # boundary layer must always be the first one listed
                    w0 = wires[boundary_layer_name][0]
                    wp = CQ().sketch().face(w0)
                    for w in wires[boundary_layer_name][1::]:
                        wp = wp.face(w, mode="s")
                    wp = wp.finalize().extrude(t)  # the workpiece is now made
                    wp = wp.faces(">Z").sketch()
                    if "array" in stack_layer:
                        array_points = stack_layer["array"]
                    else:
                        array_points = [(0, 0, 0)]

                    for drawing_layer_name in stack_layer["drawing_layer_names"][1:]:
                        some_wires = wires[drawing_layer_name]
                        for awire in some_wires:
                            wp = wp.push(array_points).face(awire, mode="a", ignore_selection=False)

                    wp = wp.faces()
                    if "edge_case" in stack_layer:
                        edge_wire_sets = cadquery.sortWiresByBuildOrder(wires[stack_layer["edge_case"]])
                        edge_wires = edge_wire_sets[0]
                        es = CQ().sketch().face(edge_wires[0])
                        for edge_wire in edge_wires[1:]:
                            es = es.face(edge_wire, mode="s")
                        wp = wp.face(es.faces(), mode="i")
                        wp = wp.clean()
                    # wp = wp.finalize().cutThruAll()  # this is a fail, but should work
                    wp = wp.finalize().extrude(-t, combine="cut")

                    new = wp.translate([0, 0, z_base])
                    if asy is None:  # some silly hack needed to work around https://github.com/CadQuery/cadquery/issues/993
                        asy = cadquery.Assembly(new, name=stack_layer["name"], color=cadquery.Color(stack_layer["color"]))
                        # asy.name = stack_instructions["name"]
                    else:
                        asy.add(new, name=stack_layer["name"], color=cadquery.Color(stack_layer["color"]))
                    z_base = z_base + t
                stacks[stack_instructions["name"]] = asy
        return stacks
        # asy.save(str(Path(__file__).parent / "output" / f"{stack_instructions['name']}.step"))
        # cq.Shape.exportBrep(cq.Compound.makeCompound(itertools.chain.from_iterable([x[1].shapes for x in asy.traverse()])), str(Path(__file__).parent / "output" / "badger.brep"))

    def get_wires(self, dxf_filepaths: List[Path], layer_names: List[str] = []) -> List[cq.Workplane]:
        """returns the wires from the given dxf layers"""
        # list of of all layers in the dxf
        layer_sets = []
        for filepath in dxf_filepaths:
            file_path_str = str(filepath)
            dxf = ezdxf.readfile(file_path_str)
            layer_sets.append(set(dxf.modelspace().groupby(dxfattrib="layer").keys()))

        if len(layer_sets) > 1:
            bad_intersection = set.intersection(*layer_sets)
            if bad_intersection:
                raise ValueError(f"Identical layer names found in multiple drawings: {bad_intersection}")
        wires = {}
        for layer_name in layer_names:
            for i, layer_set in enumerate(layer_sets):
                if layer_name in layer_set:
                    which_file = dxf_filepaths[i]
                    break
            to_exclude = list(layer_set - set((layer_name,)))
            wires[layer_name] = cadquery.importers.importDXF(which_file, exclude=to_exclude).wires().vals()

        return wires


def main():
    # define where we'll read shapes from
    sources = [
        Path.cwd().parent / "oxford" / "master.dxf",
        Path.cwd().parent / "oxford" / "derivatives" / "5x5_cluster_master.dxf",
        Path.cwd().parent / "oxford" / "derivatives" / "4x4_cluster_master.dxf",
    ]

    support_thickness = 0.65
    feature_thickness = 0.2
    shim_thickness = 0.05

    support_color = "GOLDENROD"
    feature_color = "SKYBLUE2"
    shim_color = "DARKGREEN"

    # define how we'll tile things
    spacing5 = 30
    array5 = [(x * spacing5, y * spacing5, 0) for x, y in itertools.product(range(-2, 3), range(-2, 3))]

    spacing4 = 34.04
    array4 = [((x + 0.5) * spacing4, (y + 0.5) * spacing4, 0) for x, y in itertools.product(range(-2, 2), range(-2, 2))]

    instructions = []
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
                        "outline_5x5",
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
                        "outline_no_alignment_5x5",
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
                        "outline_4x4",
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
                        "outline_no_alignment_4x4",
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
                        "outline_5x5",
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
                        "outline_no_alignment_5x5",
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
                        "outline_4x4",
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
                        "outline_no_alignment_4x4",
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
            "name": "metal6_mask_stack_5x5",
            "layers": [
                {
                    "name": "metal_support",
                    "color": support_color,
                    "thickness": support_thickness,
                    "drawing_layer_names": [
                        "outline_5x5",
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
                        "outline_no_alignment_5x5",
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
                        "outline_4x4",
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
                        "outline_no_alignment_4x4",
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
                        "outline_5x5",
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
                        "outline_no_alignment_5x5",
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
                        "outline_4x4",
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
                        "outline_no_alignment_4x4",
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
                        "outline_5x5",
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
                        "outline_no_alignment_5x5",
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
                        "outline_4x4",
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
                        "outline_no_alignment_4x4",
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
                        "outline_5x5",
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
                        "outline_no_alignment_5x5",
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
                        "outline_4x4",
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
                        "outline_no_alignment_4x4",
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

    ttt = TwoDToThreeD(instructions=instructions, sources=sources)
    # to_build = ["active_mask_stack", "metal_mask_stack"]
    # to_build = ["tandem_metal_mask_stack"]
    to_build = [""]  # all of them
    asys = ttt.build(to_build)
    # asy: cadquery.Assembly = list(asys.values())[0]  # TODO:take more than the first value

    for stack_name, asy in asys.items():
        if "show_object" in globals():  # we're in cq-editor
            assembly_mode = True  # at the moment, when true we can't select/deselect subassembly parts
            if assembly_mode:
                show_object(asy)
            else:
                for key, val in asy.traverse():
                    shapes = val.shapes
                    if shapes != []:
                        c = cq.Compound.makeCompound(shapes)
                        odict = {}
                        if val.color is not None:
                            co = val.color.wrapped.GetRGB()
                            rgb = (co.Red(), co.Green(), co.Blue())
                            odict["color"] = rgb
                        show_object(c.locate(val.loc), name=val.name, options=odict)
        else:
            # save assembly
            asy.save(str(Path(__file__).parent / "output" / f"{stack_name}.step"))
            asy.save(str(Path(__file__).parent / "output" / f"{stack_name}.glb"), "GLTF")
            # cadquery.exporters.assembly.exportCAF(asy, str(Path(__file__).parent / "output" / f"{stack_name}.std"))
            # cq.Shape.exportBrep(cq.Compound.makeCompound(itertools.chain.from_iterable([x[1].shapes for x in asy.traverse()])), str(Path(__file__).parent / "output" / f"{stack_name}.brep"))

            save_individual_stls = False
            save_individual_steps = False
            save_individual_breps = False
            save_individual_dxfs = True

            # save each shape individually
            for key, val in asy.traverse():
                shapes = val.shapes
                if shapes != []:
                    c = cq.Compound.makeCompound(shapes)
                    if save_individual_stls == True:
                        cadquery.exporters.export(c.locate(val.loc), str(Path(__file__).parent / "output" / f"{stack_name}-{val.name}.stl"))
                    if save_individual_steps == True:
                        cadquery.exporters.export(c.locate(val.loc), str(Path(__file__).parent / "output" / f"{stack_name}-{val.name}.step"))
                    if save_individual_breps == True:
                        cq.Shape.exportBrep(c.locate(val.loc), str(Path(__file__).parent / "output" / f"{stack_name}-{val.name}.brep"))
                    if save_individual_dxfs == True:
                        cl = c.locate(val.loc)
                        bb = cl.BoundingBox()
                        zmid = (bb.zmin + bb.zmax) / 2
                        nwp = CQ("XY", origin=(0, 0, zmid)).add(cl)
                        dxface = nwp.section()
                        cadquery.exporters.export(dxface, str(Path(__file__).parent / "output" / f"{stack_name}-{val.name}.dxf"), cadquery.exporters.ExportTypes.DXF)


# temp is what we get when run via cq-editor
if __name__ in ["__main__", "temp"]:
    main()
