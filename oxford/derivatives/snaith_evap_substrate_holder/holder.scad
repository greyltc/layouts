// generates the substrate holder
// grey@mutovis.com
// 12 april 2019

include <meta.scad>

// holder
linear_extrude(height=holder_thicknes){
    difference(){
        plate();
        voids(pocket=true,little_drill_d=m2_tap_drill_d);
    }
}