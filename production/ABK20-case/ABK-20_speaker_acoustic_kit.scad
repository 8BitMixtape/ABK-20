// ==============================================================================
// ABK-20 Synthesizer: Modular Acoustic Bass Audition Kit
// ==============================================================================
// Standalone 3D-printable test suite to get MAXIMUM BASS out of the rear micro-speaker:
//
// 1. cup_sealed_9p5mm          - Standard Sealed Cup (28x15x9.5mm, Vb ≈ 2.1 cm³, standard fit)
// 2. cup_sealed_xl_12mm        - XL Big Sealed Cup (34x17x12.0mm, Vb ≈ 4.3 cm³, 2x compliance!)
// 3. cup_sealed_max_14mm       - MAX Sub-Bass Sealed (35x17x14.0mm, Vb ≈ 5.5 cm³, 2.6x compliance!)
// 4. cup_ported_slot           - Standard Flush Slot Port (28x15x9.5mm, fb ≈ 520 Hz)
// 5. cup_ported_xl_labyrinth   - XL Folded Sub-Bass Maze (34x17x12.0mm, fb ≈ 295 Hz deep rumble!)
// 6. cup_ported_pipe_side      - External Side Pipe (28x15x9.5mm, 45° bi-directional self-supporting)
// 7. cup_ported_pipe_extended  - Extended Snorkel Pipe (28x15x9.5mm, +10mm flared horn, 45° ramped)
// 8. cup_downward_vent         - Downward Boundary Port (28x15x9.5mm, couples with desk/bottom plate)
// 9. front_chimney             - 8.1mm Waveguide Horn (Funnels sound to faceplate grill)
//
// Select "audition_plate" or any individual part from the dropdown.
// ALL PARTS ARE 100% SELF-SUPPORTING: Slice with "Supports: None"!
// ==============================================================================

$fn = 60;

/* [Part Selector] */
// Select which part to view or export as STL:
part_to_show = "audition_plate"; // [audition_plate, audition_plate_pipes, cup_pipe_ext_std_9p5mm, cup_pipe_ext_xl_12mm, cup_pipe_ext_max_14mm, cup_sealed_9p5mm, cup_sealed_xl_12mm, cup_sealed_max_14mm, cup_ported_slot, cup_ported_xl_labyrinth, cup_ported_pipe_side, cup_downward_vent, front_chimney, assembly, assembly_cutaway]

/* [Standard Cup Dimensions] */
pod_l = 28.0;
pod_w = 15.0;
pod_r = 4.5;
pod_wall = 1.4;
pod_flange = 1.2;
wire_notch_w = 2.5;
wire_notch_h = 1.4;

/* [XL & MAX Big Bass Cup Dimensions] */
xl_l = 34.0;
xl_w = 17.0;
xl_depth = 12.0;

max_l = 35.0;
max_w = 17.0;
max_depth = 14.0;

/* [Acoustic Port Settings] */
slot_w = 1.8;
slot_h = 2.8;
slot_l = 24.0;
pipe_inner_d = 2.5;
pipe_wall = 1.0;
down_vent_d = 2.4;

/* [Front Chimney Waveguide Dimensions] */
chimney_height = 8.1;
chimney_bottom_l = 21.6;
chimney_bottom_w = 8.6;
chimney_bottom_r = 3.32;
horn_flare = 1.5;
chimney_wall = 1.2;


// ==============================================================================
// 2D HELPERS
// ==============================================================================

module capsule_2d(length, width, radius) {
    rx = max(0.1, length/2 - radius);
    ry = max(0.1, width/2 - radius);
    hull() {
        translate([-rx, -ry]) circle(r=radius);
        translate([ rx, -ry]) circle(r=radius);
        translate([-rx,  ry]) circle(r=radius);
        translate([ rx,  ry]) circle(r=radius);
    }
}


// ==============================================================================
// BASE CUP SHELL (PARAMETRIC DIMENSIONS)
// ==============================================================================

module base_cup_body(l=pod_l, w=pod_w, depth=9.5, wall=pod_wall, flange=pod_flange) {
    total_l = l + flange * 2;
    total_w = w + flange * 2;
    total_r = pod_r + flange;

    difference() {
        // Outer body with rim flange
        union() {
            linear_extrude(depth)
                capsule_2d(l, w, pod_r);
            translate([0, 0, depth - 1.2])
                linear_extrude(1.2)
                capsule_2d(total_l, total_w, total_r);
        }

        // Inner acoustic cavity (solid roof of thickness wall at Z=0)
        translate([0, 0, wall])
            linear_extrude(depth + 1)
            capsule_2d(l - wall*2, w - wall*2, max(0.5, pod_r - wall));

        // Wire exit notch on the left (-X)
        translate([-l/2 - flange - 1, -wire_notch_w/2, depth - wire_notch_h])
            cube([flange + wall + 2, wire_notch_w, wire_notch_h + 1]);
    }
}


// ==============================================================================
// 1. SEALED SUSPENSION CUPS (STANDARD, XL, MAX)
// ==============================================================================
// Pure acoustic suspension: tight, punchy bass transients, zero distortion.

module pod_sealed(l=pod_l, w=pod_w, depth=9.5, c=[0.85, 0.25, 0.35]) {
    color(c)
    base_cup_body(l=l, w=w, depth=depth);
}


// ==============================================================================
// 2. FLUSH END-VENT SLOT PORT (BASS-REFLEX LABYRINTH)
// ==============================================================================

module pod_slot_ported(l=pod_l, w=pod_w, depth=9.5) {
    color([0.95, 0.45, 0.15])
    difference() {
        base_cup_body(l=l, w=w, depth=depth);

        // Integrated slot tunnel along +Y wall, venting flush through +X end wall
        translate([l/2 - slot_l, w/2 - pod_wall - slot_w, pod_wall])
            cube([slot_l + pod_flange + 2, slot_w, slot_h]);
    }
}


// ==============================================================================
// 3. FOLDED U-TURN LABYRINTH PORT (XL SUB-BASS MAZE ~295 Hz)
// ==============================================================================

module pod_xl_labyrinth_ported(l=xl_l, w=xl_w, depth=xl_depth) {
    color([0.95, 0.65, 0.10])
    difference() {
        base_cup_body(l=l, w=w, depth=depth);

        // Forward leg of tunnel along +Y wall
        translate([-6, w/2 - pod_wall - slot_w, pod_wall])
            cube([l/2 + 4, slot_w, slot_h]);

        // U-turn passage around +X end
        translate([l/2 - pod_wall - slot_w*2, -1, pod_wall])
            cube([slot_w*2, w/2, slot_h]);

        // Return leg venting out +X end at lower Y position
        translate([l/2 - 14, 1, pod_wall])
            cube([16 + pod_flange + 2, slot_w, slot_h]);
    }
}


// ==============================================================================
// 4. EXTERNAL SIDE PIPE (FLUSH END MOUTH, 515 Hz)
// ==============================================================================
// Features bi-directional 45° fairing ramps supporting both the contact flange
// plane (when printing rim-down on the bed) and the roof (when printing roof-down).

module pod_pipe_side(depth=9.5) {
    pipe_od = pipe_inner_d + pipe_wall * 2;
    pipe_y = pod_w/2 + pipe_od/2 - 0.7;
    pipe_z = depth / 2;
    pipe_start_x = -7.0;
    pipe_end_x = pod_l / 2 + pod_flange;

    color([0.88, 0.40, 0.20])
    difference() {
        union() {
            base_cup_body(depth=depth);

            // Bi-directional 45° self-supporting fairing body:
            hull() {
                translate([pipe_start_x, pipe_y, pipe_z])
                    sphere(d=pipe_od);
                translate([pipe_end_x, pipe_y, pipe_z])
                    rotate([0, 90, 0])
                    cylinder(d=pipe_od, h=0.1);

                // 45° support ramp down to contact flange plane (Z = depth)
                translate([pipe_start_x, pod_w/2 - 0.2, depth])
                    rotate([0, 90, 0])
                    cylinder(d=0.2, h=pipe_end_x - pipe_start_x);

                // 45° support ramp down to roof plane (Z = 0)
                translate([pipe_start_x, pod_w/2 - 0.2, 0])
                    rotate([0, 90, 0])
                    cylinder(d=0.2, h=pipe_end_x - pipe_start_x);
            }
        }

        // Pipe internal bore
        translate([pipe_start_x, pipe_y, pipe_z])
            rotate([0, 90, 0])
            cylinder(d=pipe_inner_d, h=pipe_end_x - pipe_start_x + 2);

        // Acoustic port coupling hole into the main chamber
        translate([pipe_start_x + 1, 0, pipe_z])
            rotate([-90, 0, 0])
            cylinder(d=pipe_inner_d, h=pipe_y + 1);
    }
}


// ==============================================================================
// 5. EXTENDED SNORKEL PIPE (PARAMETRIC SIZES: STANDARD, XL, MAX)
// ==============================================================================
// Extended snorkel bass port with a solid flat support keel continuous with
// the PCB contact flange plane (Z = depth).
// 100% FLAT BED CONTACT when printing rim-down: ZERO SUPPORTS NEEDED!
// Also provides rock-solid mechanical grounding against the PCB when mounted!

module pod_pipe_extended(l=pod_l, w=pod_w, depth=9.5, ext_len=10.0, c=[0.90, 0.30, 0.15]) {
    pipe_od = pipe_inner_d + pipe_wall * 2;
    pipe_y = w/2 + pipe_od/2 - 0.7;
    pipe_z = depth / 2;
    pipe_start_x = -l/2 + 5.0;
    pipe_end_x = l/2 + pod_flange + ext_len;

    color(c)
    difference() {
        union() {
            base_cup_body(l=l, w=w, depth=depth);

            // Extended pipe body with SOLID SUPPORT KEEL connecting to PCB contact plane (Z=depth):
            hull() {
                // Main pipe cylinder and spherical back dome
                translate([pipe_start_x, pipe_y, pipe_z])
                    sphere(d=pipe_od);
                translate([pipe_end_x - 3, pipe_y, pipe_z])
                    rotate([0, 90, 0])
                    cylinder(d=pipe_od, h=0.1);

                // Flat support foot on the PCB contact plane (Z=depth) along the whole length!
                translate([pipe_start_x, w/2, depth - 0.1])
                    cube([pipe_end_x - pipe_start_x - 3, pipe_od, 0.1]);

                // 45° slope toward roof (Z=0) for smooth aesthetic top
                translate([pipe_start_x, w/2, max(0, pipe_z - pipe_od)])
                    rotate([0, 90, 0])
                    cylinder(d=0.2, h=l/2 + pod_flange - pipe_start_x);
            }

            // Trumpet flared mouth with support foot to PCB contact plane
            hull() {
                translate([pipe_end_x - 3, pipe_y, pipe_z])
                    rotate([0, 90, 0]) cylinder(d=pipe_od, h=0.1);
                translate([pipe_end_x, pipe_y, pipe_z])
                    rotate([0, 90, 0]) cylinder(d=pipe_od + 1.8, h=0.1);
                // Flat foot under trumpet mouth touching Z=depth
                translate([pipe_end_x - 3, pipe_y - (pipe_od+1.8)/2, depth - 0.1])
                    cube([3, pipe_od + 1.8, 0.1]);
            }
        }

        // Pipe internal bore
        translate([pipe_start_x, pipe_y, pipe_z])
            rotate([0, 90, 0])
            cylinder(d=pipe_inner_d, h=pipe_end_x - pipe_start_x - 2.5);

        // Flared trumpet mouth at exhaust exit
        translate([pipe_end_x - 3.1, pipe_y, pipe_z])
            rotate([0, 90, 0])
            cylinder(d1=pipe_inner_d, d2=pipe_inner_d + 1.8, h=3.2);

        // Acoustic port coupling hole into the main chamber
        translate([pipe_start_x + 1, 0, pipe_z])
            rotate([-90, 0, 0])
            cylinder(d=pipe_inner_d, h=pipe_y + 1);
    }
}


// ==============================================================================
// 6. DOWNWARD-FIRING BOUNDARY PORT
// ==============================================================================

module pod_downward_vent(depth=9.5) {
    color([0.70, 0.35, 0.90])
    difference() {
        base_cup_body(depth=depth);

        // Downward vent hole through the flat roof at +X end
        translate([pod_l/2 - pod_r, 0, -1])
            cylinder(d=down_vent_d, h=pod_wall + 2);
    }
}


// ==============================================================================
// 7. FRONT ACOUSTIC CHIMNEY (WAVEGUIDE HORN)
// ==============================================================================

module front_chimney() {
    top_l = chimney_bottom_l + horn_flare * 2;
    top_w = chimney_bottom_w + horn_flare * 2;
    top_r = chimney_bottom_r + horn_flare;

    color([0.20, 0.75, 0.90])
    difference() {
        hull() {
            translate([0, 0, 0])
                linear_extrude(0.1)
                capsule_2d(chimney_bottom_l + chimney_wall*2, 
                           chimney_bottom_w + chimney_wall*2, 
                           chimney_bottom_r + chimney_wall);
            translate([0, 0, chimney_height])
                linear_extrude(0.1)
                capsule_2d(top_l + chimney_wall*2, 
                           top_w + chimney_wall*2, 
                           top_r + chimney_wall);
        }

        hull() {
            translate([0, 0, -0.5])
                linear_extrude(0.1)
                capsule_2d(chimney_bottom_l, chimney_bottom_w, chimney_bottom_r);
            translate([0, 0, chimney_height + 0.5])
                linear_extrude(0.1)
                capsule_2d(top_l, top_w, top_r);
        }
    }
}


// ==============================================================================
// PHYSICAL SPEAKER MODEL (FOR VISUALIZATION)
// ==============================================================================

module physical_speaker_model() {
    color([0.15, 0.16, 0.18])
    translate([0, 0, -2.8]) linear_extrude(2.8) capsule_2d(20.0, 8.5, 3.2);

    color([0.95, 0.95, 0.95])
    translate([0, 0, 0])
        difference() {
            union() {
                linear_extrude(0.25) capsule_2d(20.0, 8.5, 3.2);
                translate([-11.2, -1.8, 0]) cube([2.5, 3.6, 0.25]);
            }
            translate([0, 0, -0.5]) linear_extrude(1.0) capsule_2d(15.0, 5.0, 2.2);
        }

    color([0.10, 0.10, 0.12])
    translate([0, 0, -0.1]) linear_extrude(0.1) capsule_2d(15.0, 5.0, 2.2);

    color([0.9, 0.1, 0.1]) translate([-11.0, -0.8, -0.5]) rotate([0, -90, 0]) cylinder(d=0.7, h=10);
    color([0.1, 0.1, 0.1]) translate([-11.0,  0.8, -0.5]) rotate([0, -90, 0]) cylinder(d=0.7, h=10);
}


// ==============================================================================
// SCENE RENDER SELECTION
// ==============================================================================

if (part_to_show == "audition_plate") {
    // 6 Curated Bass Contenders on a single build plate:
    // Row 1: Standard Sealed (9.5mm) vs XL Sealed (12mm) vs MAX Sealed (14mm)
    translate([-26, -16, 0]) pod_sealed(l=pod_l, w=pod_w, depth=9.5, c=[0.85, 0.25, 0.35]);
    translate([  6, -16, 0]) pod_sealed(l=xl_l,  w=xl_w,  depth=12.0, c=[0.75, 0.20, 0.45]);
    translate([ 40, -16, 0]) pod_sealed(l=max_l, w=max_w, depth=14.0, c=[0.60, 0.15, 0.55]);

    // Row 2: Standard Flush Slot vs XL Sub-Bass Maze (295 Hz)
    translate([-22,  14, 0]) pod_slot_ported(depth=9.5);
    translate([ 18,  14, 0]) pod_xl_labyrinth_ported(l=xl_l, w=xl_w, depth=12.0);

    // Row 3: Extended Snorkel Pipe & Front Waveguide Chimney
    translate([-22,  44, 0]) pod_pipe_extended(depth=9.5);
    translate([ 22,  44, chimney_height])
        rotate([180, 0, 0])
        front_chimney();

} else if (part_to_show == "audition_plate_pipes") {
    // The 3 Extended Snorkel Pipe sizes in a clean 2x2 grid with ample clearance:
    // Row 1: Standard Extended (9.5mm) vs XL Extended (12mm)
    translate([-26, -18, 0]) pod_pipe_extended(l=pod_l, w=pod_w, depth=9.5, ext_len=10.0, c=[0.88, 0.35, 0.20]);
    translate([ 26, -18, 0]) pod_pipe_extended(l=xl_l,  w=xl_w,  depth=12.0, ext_len=12.0, c=[0.92, 0.40, 0.15]);

    // Row 2: MAX Extended (14mm) vs Front Waveguide Chimney
    translate([-26,  18, 0]) pod_pipe_extended(l=max_l, w=max_w, depth=14.0, ext_len=12.0, c=[0.96, 0.45, 0.10]);
    translate([ 26,  18, chimney_height])
        rotate([180, 0, 0])
        front_chimney();

} else if (part_to_show == "cup_pipe_ext_std_9p5mm") {
    pod_pipe_extended(l=pod_l, w=pod_w, depth=9.5, ext_len=10.0);

} else if (part_to_show == "cup_pipe_ext_xl_12mm") {
    pod_pipe_extended(l=xl_l, w=xl_w, depth=12.0, ext_len=12.0, c=[0.92, 0.40, 0.15]);

} else if (part_to_show == "cup_pipe_ext_max_14mm") {
    pod_pipe_extended(l=max_l, w=max_w, depth=14.0, ext_len=12.0, c=[0.96, 0.45, 0.10]);

} else if (part_to_show == "cup_sealed_9p5mm") {
    pod_sealed(l=pod_l, w=pod_w, depth=9.5);

} else if (part_to_show == "cup_sealed_xl_12mm") {
    pod_sealed(l=xl_l, w=xl_w, depth=12.0, c=[0.75, 0.20, 0.45]);

} else if (part_to_show == "cup_sealed_max_14mm") {
    pod_sealed(l=max_l, w=max_w, depth=14.0, c=[0.60, 0.15, 0.55]);

} else if (part_to_show == "cup_ported_slot") {
    pod_slot_ported(depth=9.5);

} else if (part_to_show == "cup_ported_xl_labyrinth") {
    pod_xl_labyrinth_ported(l=xl_l, w=xl_w, depth=12.0);

} else if (part_to_show == "cup_ported_pipe_side") {
    pod_pipe_side(depth=9.5);

} else if (part_to_show == "cup_downward_vent") {
    pod_downward_vent(depth=9.5);

} else if (part_to_show == "front_chimney") {
    translate([0, 0, chimney_height])
        rotate([180, 0, 0])
        front_chimney();

} else if (part_to_show == "assembly") {
    color([0.12, 0.45, 0.22, 0.85])
    difference() {
        translate([0, 0, -1.6]) linear_extrude(1.6) square([50, 32], center=true);
        for (x = [-6 : 2 : 6]) translate([x, 0, -2]) cylinder(d=0.8, h=4);
        for (x = [-5 : 2 : 5]) {
            translate([x, -1.75, -2]) cylinder(d=0.8, h=4);
            translate([x,  1.75, -2]) cylinder(d=0.8, h=4);
        }
    }
    translate([0, 0, -1.6]) physical_speaker_model();
    front_chimney();
    translate([0, 0, -12.0 - 1.6]) pod_pipe_extended(l=xl_l, w=xl_w, depth=12.0, ext_len=12.0);

} else if (part_to_show == "assembly_cutaway") {
    difference() {
        union() {
            color([0.12, 0.45, 0.22, 0.85])
                translate([0, 0, -1.6]) linear_extrude(1.6) square([50, 32], center=true);
            translate([0, 0, -1.6]) physical_speaker_model();
            front_chimney();
            translate([0, 0, -12.0 - 1.6]) pod_pipe_extended(l=xl_l, w=xl_w, depth=12.0, ext_len=12.0);
        }
        translate([0, -20, -25]) cube([40, 45, 45]);
    }
}
