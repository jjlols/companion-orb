// Palm Blob v1 — palm-sized rolling desk pet (no face)
// Units: mm
// Export each part: set PART and Render (F6) -> STL
//
// PART options:
//  "shell_bottom" | "shell_top" | "chassis" | "led_window" | "button_cap" | "wheel_spacer" | "bumper_tpu"

PART = "shell_bottom";

OD = 64;
WALL = 1.8;
ID = OD - 2*WALL;
CLEAR = 0.35;

MAGNET_D = 6.0;
MAGNET_H = 2.0;
LED_D = 8.0;
BUTTON_D = 6.5;
USB_W = 9.2;
USB_H = 3.6;

N20_L = 26.0;
N20_W = 12.2;
N20_H = 10.2;
BATTERY_L = 40;
BATTERY_W = 25;
BATTERY_H = 8.5;
WEIGHT_D = 22;
WEIGHT_H = 4;

$fn = 64;

module hemisphere_shell(outer_r, inner_r, upper=false) {
    difference() {
        intersection() {
            sphere(r=outer_r);
            if (upper)
                translate([0,0,0]) cube([outer_r*2+2, outer_r*2+2, outer_r+1], center=true);
            else
                translate([0,0,-outer_r/2-0.5]) cube([outer_r*2+2, outer_r*2+2, outer_r+1], center=true);
        }
        sphere(r=inner_r);
        if (upper)
            translate([0,0,-outer_r]) cube([outer_r*2+2, outer_r*2+2, outer_r*2], center=true);
        else
            translate([0,0,outer_r]) cube([outer_r*2+2, outer_r*2+2, outer_r*2], center=true);
    }
}

module magnet_pocket(ang, z_sign=1) {
    rotate([0,0,ang])
        translate([ID/2 - 1.2, 0, 0])
            rotate([0,90,0])
                cylinder(h=MAGNET_H + 0.4, d=MAGNET_D + 0.25, center=true);
}

module shell_bottom() {
    r_o = OD/2;
    r_i = ID/2;
    difference() {
        union() {
            hemisphere_shell(r_o, r_i, upper=false);
            // rim lip
            difference() {
                cylinder(h=2.2, r=r_o);
                translate([0,0,-0.1]) cylinder(h=2.5, r=r_i - 1.2);
            }
            // alignment pegs
            for (a = [0, 120, 240])
                rotate([0,0,a])
                    translate([(r_o + r_i - 1.2)/2, 0, 2.2])
                        cylinder(h=2.2, d=2.8);
            // chassis posts
            for (x = [-12, 12])
                translate([x, 0, -r_i + 6])
                    cylinder(h=4, d=4);
            // button boss
            translate([0, r_i - 2.2, -5])
                rotate([90,0,0])
                    cylinder(h=3.5, d=BUTTON_D + 2.5);
        }
        // magnet pockets (press from inside)
        for (a = [45, 135, 225, 315])
            translate([0,0,0.6]) magnet_pocket(a);
        // USB-C / cable notch rear (-Y)
        translate([0, -r_o + 1, -4.5])
            cube([USB_W, 8, USB_H], center=true);
        // button through-hole
        translate([0, r_i + 1, -5])
            rotate([90,0,0])
                cylinder(h=8, d=BUTTON_D);
        // hollow chassis post holes (M2 optional)
        for (x = [-12, 12])
            translate([x, 0, -r_i + 5.5])
                cylinder(h=5, d=1.8);
        // rim seating cleanup
        translate([0,0,2.15])
            cylinder(h=1, r=r_i - 1.15);
    }
}

module shell_top() {
    r_o = OD/2;
    r_i = ID/2;
    difference() {
        union() {
            hemisphere_shell(r_o, r_i, upper=true);
            // mating collar
            translate([0,0,-2.0])
                difference() {
                    cylinder(h=2.0, r=r_o - 0.35);
                    translate([0,0,-0.1]) cylinder(h=2.3, r=r_i - 1.0);
                }
        }
        // peg holes
        for (a = [0, 120, 240])
            rotate([0,0,a])
                translate([(r_o - 0.35 + r_i - 1.0)/2, 0, -2.05])
                    cylinder(h=2.3, d=2.8 + CLEAR*2);
        // magnet pockets
        for (a = [45, 135, 225, 315])
            translate([0,0,-0.6]) magnet_pocket(a);
        // LED window
        translate([0, 0, r_i - 4])
            cylinder(h=6, d=LED_D);
        // LED lip seat
        translate([0, 0, r_i - 3.2])
            cylinder(h=1.2, d=LED_D + 1.6);
    }
    // LED retainer ring (printed with top)
    difference() {
        translate([0,0,r_i - 3.2])
            cylinder(h=1.0, d=LED_D + 1.6);
        translate([0,0,r_i - 3.3])
            cylinder(h=1.3, d=LED_D - 0.15);
    }
}

module chassis() {
    deck_t = 2.2;
    difference() {
        union() {
            // deck
            translate([0,0,deck_t/2])
                cube([36, 28, deck_t], center=true);
            // side rails
            for (y = [-13, 13])
                translate([0, y, 5])
                    cube([36, 2, 10], center=true);
            // battery keepers
            for (x = [-BATTERY_L/2 - 0.2, BATTERY_L/2 + 0.2])
                translate([x, 0, deck_t + BATTERY_H/2])
                    cube([1.6, BATTERY_W, BATTERY_H], center=true);
            // weight cup
            translate([0,0,-WEIGHT_H/2])
                cylinder(h=WEIGHT_H + 1.2, d=WEIGHT_D + 1.6, center=true);
            // motor cradles
            for (y = [-8.5, 8.5]) {
                translate([0, y, deck_t + N20_H/2])
                    cube([N20_L + 1, N20_W + 1.2, N20_H + 0.6], center=true);
                // end clamps
                for (x = [-(N20_L/2 + 1.0), (N20_L/2 + 1.0)])
                    translate([x, y, deck_t + N20_H/2])
                        cube([2.0, 8, N20_H], center=true);
            }
            // electronics shelf
            translate([-10, 0, deck_t + BATTERY_H + 1])
                cube([22, 18, 1.6], center=true);
            // XIAO posts
            for (p = [[-18,-7],[ -18,7],[-1,-7],[-1,7]])
                translate([p[0], p[1], deck_t + BATTERY_H + 1])
                    cylinder(h=3.5, d=2.4);
            // DRV pad rails
            translate([12, 0, deck_t + BATTERY_H + 1])
                cube([DRV_L + 1, DRV_W + 1, 1.4], center=true);
        }
        // weight pocket
        translate([0,0,-WEIGHT_H/2 - 0.2])
            cylinder(h=WEIGHT_H, d=WEIGHT_D + 0.3, center=true);
        // motor cavities (slightly larger)
        for (y = [-8.5, 8.5])
            translate([0, y, deck_t + N20_H/2 + 0.2])
                cube([N20_L + CLEAR*2, N20_W + CLEAR*2, N20_H], center=true);
        // shaft / wheel escapes toward ±Y
        for (y = [-14, 14])
            translate([0, y, deck_t + 6])
                cube([10, 8, 12], center=true);
        // registration holes for shell posts
        for (x = [-12, 12])
            translate([x, 0, -1])
                cylinder(h=deck_t + 3, d=4.2);
        // battery floor relief
        translate([0,0,deck_t + 0.2])
            cube([BATTERY_L + 0.6, BATTERY_W + 0.6, 0.6], center=true);
        // cable channels
        translate([0,0,deck_t + 1])
            cube([4, 30, 2], center=true);
    }
}

module led_window() {
    cylinder(h=1.2, d=LED_D - 0.25);
}

module button_cap() {
    union() {
        cylinder(h=4.5, d=BUTTON_D - 0.6);
        translate([0,0,4.5]) cylinder(h=1.0, d=BUTTON_D + 2);
    }
}

module wheel_spacer() {
    difference() {
        cylinder(h=5, d=8);
        translate([0,0,-0.1]) cylinder(h=5.2, d=3.1);
    }
}

module bumper_tpu() {
    difference() {
        cylinder(h=8, r=OD/2 + 1.2, center=true);
        cylinder(h=9, r=OD/2 - 0.15, center=true);
    }
}

if (PART == "shell_bottom") shell_bottom();
else if (PART == "shell_top") shell_top();
else if (PART == "chassis") chassis();
else if (PART == "led_window") led_window();
else if (PART == "button_cap") button_cap();
else if (PART == "wheel_spacer") wheel_spacer();
else if (PART == "bumper_tpu") bumper_tpu();
else text("Unknown PART");
