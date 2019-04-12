// generates the substrate holder
// grey@mutovis.com
// 12 april 2019

cir_rad = 114;
flat_spacing = 197;
pocket_xy = 30.2;
pocket_x_spacing = pocket_xy + 5;
pocket_y_spacing = pocket_xy + 3.8;
m2_tap_drill_d = 1.6;
m2_clearance_drill_d = 2.2;
holder_thicknes = 3;
stopper_thicknes = 1;

module rounded_square(d=1,a=10){
    // identical to (because freecad doesn't support this):
    //minkowski(){
    //    square([a-d,a-d],center=true);
    //    circle(d=d);
    //}

    b = a/2;
    difference(){
        square([2*b,2*b],center=true);
        translate([(b-d/2),(b-d/2),0]) rotate(0) difference(){
            square([d/2,d/2]);
            circle(d=d);
            
        }
        translate([-(b-d/2),(b-d/2),0]) rotate(90) difference(){
            square([d/2,d/2]);
            circle(d=d);
        }
        translate([(b-d/2),-(b-d/2),0]) rotate(-90) difference(){
            square([d/2,d/2]);
            circle(d=d);
        }
        translate([-(b-d/2),-(b-d/2),0]) rotate(-180) difference(){
            square([d/2,d/2]);
            circle(d=d);
        }
    }
}

module plate(){
    intersection(){
        circle(r=cir_rad);
        square([flat_spacing,1000],center=true);
    }
}


module cutout(pocket=true){
    if (pocket == true){
        corner_drill_d = 1.6;
        union(){
            square([pocket_xy,pocket_xy],center=true);
            translate([pocket_xy/2,pocket_xy/2]) circle(d=corner_drill_d);
            translate([-pocket_xy/2,pocket_xy/2]) circle(d=corner_drill_d);
            translate([pocket_xy/2,-pocket_xy/2]) circle(d=corner_drill_d);
            translate([-pocket_xy/2,-pocket_xy/2]) circle(d=corner_drill_d);
        }
    } else {
        drill_d = 8;
        rounded_square(d=drill_d,a=pocket_xy);
    }
}

module voids(pocket=true, little_drill_d=m2_tap_drill_d){
    // middle line
    translate([0,pocket_y_spacing/2,0]){
        cutout(pocket);
        translate([0,pocket_y_spacing,0]) cutout(pocket);
        translate([0,2*pocket_y_spacing,0]) cutout(pocket);
        translate([0,-1*pocket_y_spacing,0]) cutout(pocket);
        translate([0,-2*pocket_y_spacing,0]) cutout(pocket);
        translate([0,-3*pocket_y_spacing,0]) cutout(pocket);
    }
    // one left of middle
    translate([pocket_x_spacing,pocket_y_spacing/2,0]){
        cutout(pocket);
        translate([0,pocket_y_spacing,0]) cutout(pocket);
        translate([0,2*pocket_y_spacing,0]) cutout(pocket);
        translate([0,-1*pocket_y_spacing,0]) cutout(pocket);
        translate([0,-2*pocket_y_spacing,0]) cutout(pocket);
        translate([0,-3*pocket_y_spacing,0]) cutout(pocket);
    }
    // one right of middle
    translate([-pocket_x_spacing,pocket_y_spacing/2,0]){
        cutout(pocket);
        translate([0,pocket_y_spacing,0]) cutout(pocket);
        translate([0,2*pocket_y_spacing,0]) cutout(pocket);
        translate([0,-1*pocket_y_spacing,0]) cutout(pocket);
        translate([0,-2*pocket_y_spacing,0]) cutout(pocket);
        translate([0,-3*pocket_y_spacing,0]) cutout(pocket);
    }
    // right line
    translate([-2*pocket_x_spacing,pocket_y_spacing/2,0]){
        cutout(pocket);
        translate([0,pocket_y_spacing,0]) cutout(pocket);
        translate([0,-1*pocket_y_spacing,0]) cutout(pocket);
        translate([0,-2*pocket_y_spacing,0]) cutout(pocket);
    }
    // left line
    translate([2*pocket_x_spacing,pocket_y_spacing/2,0]){
        cutout(pocket);
        translate([0,pocket_y_spacing,0]) cutout(pocket);
        translate([0,-1*pocket_y_spacing,0]) cutout(pocket);
        translate([0,-2*pocket_y_spacing,0]) cutout(pocket);
    }
    // inner support holes
    translate([pocket_x_spacing/2,-pocket_y_spacing,0]) circle(d=little_drill_d);
    translate([pocket_x_spacing/2,pocket_y_spacing,0]) circle(d=little_drill_d);
    translate([-pocket_x_spacing/2,-pocket_y_spacing,0]) circle(d=little_drill_d);
    translate([-pocket_x_spacing/2,pocket_y_spacing,0]) circle(d=little_drill_d);
    // outer support holes
    translate([3*pocket_x_spacing/2,-2*pocket_y_spacing,0]) circle(d=little_drill_d);
    translate([3*pocket_x_spacing/2,2*pocket_y_spacing,0]) circle(d=little_drill_d);
    translate([-3*pocket_x_spacing/2,2*pocket_y_spacing,0]) circle(d=little_drill_d);
    translate([-3*pocket_x_spacing/2,-2*pocket_y_spacing,0]) circle(d=little_drill_d);
    // middle edge holes
    translate([3*pocket_x_spacing/2,0,0]) circle(d=little_drill_d);
    translate([-3*pocket_x_spacing/2,0,0]) circle(d=little_drill_d);
}