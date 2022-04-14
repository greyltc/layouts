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
            asy = cadquery.Assembly()
            if stack_instructions["name"] in stacks_to_build:
                asy.name = stack_instructions["name"]
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
                        edge_wire = wires[stack_layer["edge_case"]][0]
                        wp = wp.face(edge_wire, mode="i")
                        wp = wp.clean()
                    # wp = wp.finalize().cutThruAll()  # this is a fail, but should work
                    wp = wp.finalize().extrude(-t, combine="cut")

                    asy.add(wp.translate([0, 0, z_base]), name=stack_layer["name"], color=cadquery.Color(stack_layer["color"]))
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
    ]

    support_thickness = 0.65
    feature_thickness = 0.2
    shim_thickness = 0.5

    support_color = "GOLDENROD"
    feature_color = "GRAY28"
    shim_color = "DARKGREEN"

    # define how we'll tile things
    spacing5 = 30
    array5 = [(x * spacing5, y * spacing5, 0) for x, y in itertools.product(range(-2, 3), range(-2, 3))]

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

    ttt = TwoDToThreeD(instructions=instructions, sources=sources)
    # to_build = ["active_mask_stack", "metal_mask_stack"]
    # to_build = ["active_mask_stack_5x5"]
    to_build = [""]  # all of them
    asys = ttt.build(to_build)
    # asy: cadquery.Assembly = list(asys.values())[0]  # TODO:take more than the first value

    for key, asy in asys.items():
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
            asy.save(str(Path(__file__).parent / "output" / f"{asy.name}.step"))
            # cadquery.exporters.assembly.exportCAF(asy, str(Path(__file__).parent / "output" / f"{asy.name}.std"))
            # cq.Shape.exportBrep(cq.Compound.makeCompound(itertools.chain.from_iterable([x[1].shapes for x in asy.traverse()])), str(Path(__file__).parent / "output" / f"{asy.name}.brep"))

            save_indivitual_stls = False
            save_indivitual_steps = False
            save_indivitual_breps = False

            # save them
            for key, val in asy.traverse():
                shapes = val.shapes
                if shapes != []:
                    c = cq.Compound.makeCompound(shapes)
                    if save_indivitual_stls == True:
                        cadquery.exporters.export(c.locate(val.loc), str(Path(__file__).parent / "output" / f"{asy.name}-{val.name}.stl"))
                    if save_indivitual_steps == True:
                        cadquery.exporters.export(c.locate(val.loc), str(Path(__file__).parent / "output" / f"{asy.name}-{val.name}.step"))
                    if save_indivitual_breps == True:
                        cq.Shape.exportBrep(c.locate(val.loc), str(Path(__file__).parent / "output" / f"{asy.name}-{val.name}.brep"))


# temp is what we get when run via cq-editor
if __name__ in ["__main__", "temp"]:
    main()
