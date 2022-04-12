#!/usr/bin/env python3
import cadquery
from cadquery import CQ, cq
from pathlib import Path
from typing import List
import ezdxf
import itertools


class TwoDToThreeD(object):
    dxf_filepath = Path.cwd().parent / "oxford" / "master.dxf"
    # dxf_filepath = Path(__file__).parent.parent / "oxford" / "master.dxf"  # this makes CQ-editor sad because __file__ is not defined

    def __init__(self, instructions, source: Path = dxf_filepath):
        self.stacks = instructions
        self.dxf_filepath = source

    def build(self, stacks_to_build: List[str] = [""]):
        if stacks_to_build == [""]:  # build them all by default
            stacks_to_build = [x["name"] for x in self.stacks]

        drawing_layers_needed = []
        for stack_instructions in self.stacks:
            if stack_instructions["name"] in stacks_to_build:
                for stack_layer in stack_instructions["layers"]:
                    drawing_layers_needed += stack_layer["drawing_layer_names"]
        drawing_layers_needed_unique = list(set(drawing_layers_needed))

        # all the wires we'll need here
        wires = self.get_wires(self.dxf_filepath, drawing_layers_needed_unique)

        stacks = {}
        for stack_instructions in self.stacks:
            asy = cadquery.Assembly()
            asy.name = stack_instructions["name"]
            z_base = 0
            for stack_layer in stack_instructions["layers"]:
                these_wires = []
                for drawing_layer_name in stack_layer["drawing_layer_names"]:
                    these_wires += wires[drawing_layer_name]
                t = stack_layer["thickness"]
                wp = CQ().add(these_wires).toPending().extrude(t).translate([0, 0, z_base])
                z_base = z_base + t
                asy.add(wp, name=stack_layer["name"], color=cadquery.Color(stack_layer["color"]))
            stacks[stack_instructions["name"]] = asy
        return stacks
        # asy.save(str(Path(__file__).parent / "output" / f"{stack_instructions['name']}.step"))
        # cq.Shape.exportBrep(cq.Compound.makeCompound(itertools.chain.from_iterable([x[1].shapes for x in asy.traverse()])), str(Path(__file__).parent / "output" / "badger.brep"))

    def get_wires(self, dxf_filepath: Path, layer_names: List[str] = []) -> List[cq.Workplane]:
        """returns the wires from the given dxf layers"""
        # list of of all layers in the dxf
        file_path_str = str(dxf_filepath)
        dxf = ezdxf.readfile(file_path_str)
        all_layers = set(dxf.modelspace().groupby(dxfattrib="layer").keys())
        wires = {}
        for layer_name in layer_names:
            to_exclude = list(all_layers - set((layer_name,)))
            wires[layer_name] = cadquery.importers.importDXF(file_path_str, exclude=to_exclude).wires().vals()

        return wires

    # for name, layer in
    # to_exclude = [k for k in dxf_layernames if layername != k]

    # return(dxf_obj.wires())


#   def make_heater_plate(self):
#     heater = CQ().add(self.base_plate).toPending().extrude(self.heater_t)
#     heater = heater.faces(">Z[-1]").workplane().add(self.plate_mounts).translate((0,0,self.heater_t)).toPending().cutBlind(-self.screw_depth)

#     heater = heater.translate((0,0,-self.heater_t-self.cu_base_t-self.pcb_thickness/2-self.pcb_spacer_h))
#     return (heater)

#   def make_tower_plate(self):
#     towers = CQ().add(self.cu_base).toPending().extrude(self.cu_base_t)
#     towers = towers.faces("<Z[-2]").workplane().add(self.cu_towers).translate((0,0,self.cu_base_t)).toPending().extrude(self.cu_tower_h)
#     towers = towers.faces("<Z[-2]").workplane().add(self.cu_nubs).translate((0,0,self.cu_base_t)).toPending().extrude(self.cu_nub_h)
#     towers = towers.add(self.plate_mounts).toPending().cutThruAll()
#     towers = towers.add(self.cu_dowel_pf).toPending().cutThruAll()

#     towers = towers.translate((0,0,-self.cu_base_t-self.pcb_thickness/2-self.pcb_spacer_h))
#     return (towers)

#   def get_ventscrews_a(self):
#     ventscrew = self.vent_screw.translate((0,0,-1.7))
#     ventscrews = CQ().pushPoints(self.screw_spots).eachpoint(lambda loc: ventscrew.val().moved(loc), True)
#     return ventscrews

#   def get_ventscrews_b(self):
#     ventscrew = self.vent_screw.translate((0,0,3.3))
#     ventscrews = CQ().pushPoints(self.screw_spots).eachpoint(lambda loc: ventscrew.val().moved(loc), True)
#     return ventscrews

#   def make_reservation(self, do_ventscrews:bool=False):
#     if do_ventscrews:
#       vss = self.get_ventscrews_a()
#     sr = CQ().box(self.reserve_xy,self.reserve_xy,self.reserve_h,centered=(True,True,False))
#     sr = sr.translate((0,0,-self.pcb_thickness-self.pcb_spacer_h-self.cu_base_t))
#     wires = CQ().box(self.wire_slot_depth, 2.54*20, 2.54*2, centered=(False, True, False)).translate((-self.reserve_xy/2,0,self.wire_slot_z+self.pcb_thickness/2))
#     wiresA = wires.translate((0, self.wire_slot_ofasyfset,0))
#     wiresB = wires.translate((0,-self.wire_slot_offset,0))
#     sr = sr.cut(wiresA).cut(wiresB)
#     if do_ventscrews:
#       sr = sr.add(vss)
#     # these next two lines are very expensive (and optional)!
#     sr = sr.add(self.get_pcb())
#     #sr = CQ().union(sr)
#     return sr

#   def make_silicone(self):
#     silicone = CQ().add(self.silicone).toPending().extrude(self.silicone_t)
#     silicone = silicone.translate((0,0,-self.pcb_thickness/2-self.pcb_spacer_h+self.cu_tower_h))
#     return silicone

#   def make_dowels(self):
#     dowels = CQ().add(self.dowels).toPending().extrude(self.dowel_height)
#     dowels = dowels.translate((0,0,-self.pcb_thickness/2-self.pcb_spacer_h-sel#         c = cq.Compound.makeCompound(shapes)
#     cu_tower_h+self.silicone_working_t))
#     return glass

#   def make_spacer_pcb(self):
#     spacer = CQ().add(self.spacer_pcb).toPending().extrude(self.pcb_spacer_h)
#     spacer = spacer.translate((0, 0, -self.pcb_thickness/2-self.pcb_spacer_h))
#     return (spacer)

#   def get_pcb(self):
#     return self.pcb

#   def make_pusher_plate(self):
#     pusher = CQ().add(self.pusher_plate).toPending().extrude(self.pusher_t)
#     pusher = pusher.add(self.plate_mounts).toPending().cutThruAll()
#     pusher = pusher.translate((0,0,self.pcb_thickness/2+self.slots_t + self.silicone_working_t))
#     return pusher

#   def make_slot_plate(self):
#     slots = CQ().add(self.slot_plate).toPending().extrude(self.slots_t)
#     slots = slots.add(self.plate_mounts).toPending().cutThruAll()
#     slots = slots.translate((0,0,self.pcb_thickness/2))
#     return (slots)            # wp = CQ()
#     spacer = s.make_spacer_pcb()
#     asy.add(spacer, name="spacer", color=cadquery.Color("DARKGREEN"))

#     # the towerplate
#     tp = self.make_tower_plate()
#     asy.add(tp, name="towers", color=cadquery.Color("GOLDENROD"))#         c = cq.Compound.makeCompound(shapes)


#     # dowels
#     dwl = self.make_dowels()
#     asy.add(dwl, name="dowels", color=cadquery.Color("BLACK"))

#     # silicone
#     sil = self.make_silicone()
#     asy.add(sil, name="silicone", color=cadquery.Color("WHITE"))

#     # glass
#     glass = self.make_glass()
#     asy.add(glass, name="glass", color=cadquery.Color("SKYBLUE"))

#     # the heater base plate
#     heater = s.make_heater_plate()Yeah, I think the same basic design should hopefully be good for both single ones and tiled over the big cluster area (with the special cluster features added in). I guess that thicker support layer should be the one that we bend.

#     asy.add(heater, name="heater", color=cadquery.Color("MATRAGRAY"))

#     # the spring pin PCB
#     pcb = self.get_pcb()
#     asy.add(pcb, name="pcb", color=cadquery.Color("brown"))

#     if do_ventscrews:
#       # the vent screws
#       vss_a = self.get_ventscrews_a()
#       vss_b = self.get_ventscrews_b()
#       asy.add(vss_a.add(vss_b), name="ventscrew")

#     # the alignment slot plate
#     slots = self.make_slot_plate()
#     asy.add(slots, name="sample_slots", color=cadquery.Color("GRAY45"))

#     pusher = self.make_pusher_plate()
#     asy.add(pusher, name="pusher", color=cadquery.Color("GRAY28"))

#     reserve = self.make_reservation(do_ventscrews=do_ventscrews)
#     asy.add(reserve, name="space_reservation")


#     return asy


def main():
    instructions = [
        {
            "name": "inner_active_mask_stack",
            "layers": [
                {
                    "name": "active_support",
                    "color": "GOLDENROD",
                    "thickness": 0.6,
                    "drawing_layer_names": [
                        "glass_extents",
                        "aggressive_support_active",
                    ],
                },
                {
                    "name": "active_feature",
                    "color": "BLACK",
                    "thickness": 0.2,
                    "drawing_layer_names": [
                        "glass_extents",
                        "active_layer",
                    ],
                },
                {
                    "name": "spacer_shim",
                    "color": "DARKGREEN",
                    "thickness": 0.1,
                    "drawing_layer_names": [
                        "glass_extents",
                        "spacer_shim",
                    ],
                },
            ],
        },
        {
            "name": "metal_mask_stack",
            "layers": [
                {
                    "name": "metal_support",
                    "color": "GOLDENROD",
                    "thickness": 0.6,
                    "drawing_layer_names": [
                        "glass_extents",
                        "aggressive_metal_support_tc_metal",
                        "aggressive_metal_support_small_upper",
                        "aggressive_metal_support_large_lower",
                    ],
                },
                {
                    "name": "metal_feature",
                    "color": "BLACK",
                    "thickness": 0.2,
                    "drawing_layer_names": [
                        "glass_extents",
                        "tc_metal",
                        "pixel_electrodes_small_upper",
                        "pixel_electrodes_large_lower",
                    ],
                },
                {
                    "name": "spacer_shim_thin",
                    "color": "DARKGREEN",
                    "thickness": 0.1,
                    "drawing_layer_names": [
                        "glass_extents",
                        "spacer_shim_thin",
                    ],
                },
            ],
        },
    ]

    ttt = TwoDToThreeD(instructions=instructions)
    asys = ttt.build()
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
            cadquery.exporters.assembly.exportCAF(asy, str(Path(__file__).parent / "output" / f"{asy.name}.std"))
            cq.Shape.exportBrep(cq.Compound.makeCompound(itertools.chain.from_iterable([x[1].shapes for x in asy.traverse()])), str(Path(__file__).parent / "output" / f"{asy.name}.brep"))

            save_indivitual_stls = False
            save_indivitual_steps = True
            save_indivitual_breps = True

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
