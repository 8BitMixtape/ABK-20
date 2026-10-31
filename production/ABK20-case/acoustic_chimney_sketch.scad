// ==============================================================================
// ABK-20 Synthesizer: Acoustic Chimney & Sub-Chamber Reference Sketch
// ==============================================================================
// Standalone engineering model demonstrating the acoustic waveguide chimney
// and tuned rear back-box pod.
// NOTE: This is a reference sketch and does NOT modify the active case files.
// Open this file directly in OpenSCAD for full 3D inspection.
// ==============================================================================

$fn = 40;

// --- PARAMETERS ---
pcb_to_ceiling   = 8.1;    // Gap between PCB top surface and faceplate ceiling
faceplate_thick  = 2.0;    // Top shell wall thickness
spk_w            = 21.4;   // Speaker total width
spk_h            = 8.4;    // Speaker total height
spk_r            = 3.32;   // Speaker corner radius
chimney_wall     = 1.2;    // Chimney wall thickness
draft_flare      = 1.5;    // Outward horn flare (expands aperture for horn loading)

// Speaker PCB Center Coordinates (matching hardware/ABK-20.kicad_pcb)
// PCB center is (0,0) in enclosure coordinates:
spk_pcb_x        = -9.38;  // 105.33 - 114.71
spk_pcb_y        = -1.50;  // 81.50 - 83.00

// Display Selector
part_to_show = "assembly_cutaway"; // [assembly_cutaway, chimney_only, pod_only, grills_showcase]

// --- HELPER: Stadium (Capsule) 2D Shape ---
module stadium_2d(w, h, r) {
    hull() {
        translate([-(w/2 - r), -(h/2 - r)]) circle(r=r);
        translate([ (w/2 - r), -(h/2 - r)]) circle(r=r);
        translate([-(w/2 - r),  (h/2 - r)]) circle(r=r);
        translate([ (w/2 - r),  (h/2 - r)]) circle(r=r);
    }
}

// --- MODULE 1: 3D Acoustic Waveguide Chimney (Underneath Faceplate) ---
// Extends DOWNWARD from faceplate ceiling (Z = pcb_to_ceiling) to PCB (Z = 0)
module acoustic_chimney() {
    color([0.2, 0.7, 0.9, 0.85])
    difference() {
        // Outer horn flare
        hull() {
            // Bottom at PCB surface (Z = 0)
            translate([0, 0, 0])
                linear_extrude(0.1)
                stadium_2d(spk_w + chimney_wall*2, spk_h + chimney_wall*2, spk_r + chimney_wall);
            // Top at Faceplate ceiling (Z = pcb_to_ceiling)
            translate([0, 0, pcb_to_ceiling])
                linear_extrude(0.1)
                stadium_2d(spk_w + draft_flare*2 + chimney_wall*2, spk_h + draft_flare*2 + chimney_wall*2, spk_r + draft_flare + chimney_wall);
        }
        // Inner acoustic duct (funnel)
        hull() {
            translate([0, 0, -0.5])
                linear_extrude(0.1)
                stadium_2d(spk_w, spk_h, spk_r);
            translate([0, 0, pcb_to_ceiling + 0.5])
                linear_extrude(0.1)
                stadium_2d(spk_w + draft_flare*2, spk_h + draft_flare*2, spk_r + draft_flare);
        }
    }
}

// --- MODULE 2: Faceplate Sound Grills ---
module faceplate_grill(style="slots") {
    color([0.1, 0.9, 0.8])
    if (style == "slots") {
        // 4 Stadium Slots matching internal vents
        for (sx = [-5.5, -1.8, 1.8, 5.5]) {
            translate([sx, 0, 0])
                linear_extrude(faceplate_thick + 1)
                hull() {
                    translate([0, -1.8]) circle(d=1.2);
                    translate([0,  1.8]) circle(d=1.2);
                }
        }
    } else if (style == "matrix") {
        // 3x6 Dot Grid
        for (rx = [-6.25 : 2.5 : 6.25]) {
            for (ry = [-2.2, 0, 2.2]) {
                translate([rx, ry, 0])
                    cylinder(d=1.1, h=faceplate_thick + 1);
            }
        }
    } else if (style == "louvers") {
        // 5 Horizontal Sound Louvers
        for (ly = [-2.5 : 1.25 : 2.5]) {
            translate([0, ly, 0])
                linear_extrude(faceplate_thick + 1)
                hull() {
                    translate([-7.0, 0]) circle(d=0.9);
                    translate([ 7.0, 0]) circle(d=0.9);
                }
        }
    }
}

// --- MODULE 3: Rear Back-Chamber Pod (Sub-Chamber in Bottom Case) ---
module acoustic_back_pod(depth=8.0, wall=1.4) {
    color([0.9, 0.3, 0.4, 0.85])
    translate([0, 0, -depth - 1.6]) // Sits below PCB
    difference() {
        union() {
            // Main pod body
            linear_extrude(depth)
                stadium_2d(spk_w + wall*2 + 2, spk_h + wall*2 + 2, spk_r + wall + 1);
            // Tuned Bass-Reflex Port Tube (Length = 20mm, D_outer = 4.5mm)
            translate([spk_w/2, 0, depth/2])
                rotate([0, 90, 0])
                cylinder(d=4.5, h=18, $fn=24);
        }
        // Hollow acoustic chamber
        translate([0, 0, wall])
            linear_extrude(depth)
            stadium_2d(spk_w + 2, spk_h + 2, spk_r + 1);
        // Port inner bore (D = 2.5mm)
        translate([spk_w/2 - 1, 0, depth/2])
            rotate([0, 90, 0])
            cylinder(d=2.5, h=22, $fn=24);
    }
}

// --- MODULE 4: Dummy PCB with Loch ---
module dummy_pcb() {
    color([0.15, 0.5, 0.25, 0.8])
    difference() {
        translate([0, 0, -1.6])
            linear_extrude(1.6)
            square([40, 30], center=true);
        // Loch holes
        for (x = [-6 : 2 : 6]) {
            translate([x, 0, -2]) cylinder(d=0.8, h=3);
        }
        for (x = [-5 : 2 : 5]) {
            translate([x, -1.75, -2]) cylinder(d=0.8, h=3);
            translate([x,  1.75, -2]) cylinder(d=0.8, h=3);
        }
    }
}

// --- RENDER SCENE ---
if (part_to_show == "assembly_cutaway") {
    // Cutaway view showing the entire vertical acoustic stack
    difference() {
        union() {
            // Faceplate section
            translate([0, 0, pcb_to_ceiling])
                difference() {
                    color([0.25, 0.3, 0.4, 0.6])
                        linear_extrude(faceplate_thick) square([44, 34], center=true);
                    faceplate_grill("slots");
                }
            acoustic_chimney();
            dummy_pcb();
            acoustic_back_pod();
        }
        // Cutaway bounding box (remove front-right quadrant to inspect interior)
        translate([0, -25, -20])
            cube([30, 50, 40]);
    }
} else if (part_to_show == "chimney_only") {
    acoustic_chimney();
} else if (part_to_show == "pod_only") {
    acoustic_back_pod();
} else if (part_to_show == "grills_showcase") {
    translate([-20, 0, 0]) faceplate_grill("slots");
    translate([  0, 0, 0]) faceplate_grill("matrix");
    translate([ 20, 0, 0]) faceplate_grill("louvers");
}

