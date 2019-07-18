// generates the substrate holder
// grey@mutovis.com
// 12 april 2019

include <meta.scad>

// Part thickness [mm]
Numbers=3; // [2, 3, 4, 5]

//stopper
linear_extrude(height=Numbers){
    difference(){
        plate();
        voids(pocket=false,little_drill_d=m2_clearance_drill_d);
    }
}