// generates the substrate holder
// grey@mutovis.com
// 12 april 2019

include <meta.scad>

//stopper
linear_extrude(height=stopper_thicknes){
    difference(){
        plate();
        voids(pocket=false,little_drill_d=m2_clearance_drill_d);
    }
}