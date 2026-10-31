// Parametric 3D-Printed Direct PCB Case for 8Bit Mixtape ABK-20
// Two-part enclosure (Top Shell with integrated faceplate + Bottom Cover)
// Fits directly around the 75 x 80 mm ABK-20 PCB without Eurorack rails/screws.

/* [PCB & Enclosure Dimensions] */
// PCB width in mm (ABK-20 = 75.0mm)
pcb_width = 75.0; // [50:0.1:120]
// PCB depth in mm (ABK-20 = 80.0mm)
pcb_depth = 80.0; // [50:0.1:120]
// PCB thickness in mm
pcb_thickness = 1.6; // [1.0:0.1:2.5]
// PCB corner radius in mm (set to 0 for sharp-cornered DIY PCBs)
pcb_corner_radius = 0.5; // [0:0.1:10]
// Radial clearance around the PCB inside the shell (per side: 1.0 adds 2mm total width & depth)
pcb_xy_clearance = 1.00; // [0:0.05:5]
// Distance from PCB center (Z=0) to the underside of the top shell ceiling
pcb_to_ceiling = 8.1; // [4:0.1:20]
// Internal depth below PCB center (Z=0) to clear bottom components (audio jacks reach -10.8mm)
depth_below_pcb = 10.0; // [8:0.5:30]

/* [Shell Wall & Lip Settings] */
// Outer side wall thickness
wall_thickness = 2.4; // [1.2:0.1:5]
// Top faceplate ceiling thickness
top_thickness = 2.0; // [1.2:0.1:5]
// Bottom cover floor thickness
bottom_thickness = 2.0; // [1.2:0.1:5]
// Chamfer on the outer top & bottom edges for a comfortable handheld feel
outer_edge_chamfer = 0.8; // [0:0.1:2.0]
// Width of the internal corner ledges that stop the top of the PCB
pcb_corner_ledge_size = 5.5; // [3:0.5:12]
// Height of the bottom cover's interlocking inner lip
bottom_lip_height = 3.0; // [1.5:0.5:8]
// Thickness of the bottom cover's interlocking inner lip
bottom_lip_thickness = 1.2; // [0.8:0.1:2.5]
// Fit tolerance between the bottom cover lip and top shell inner wall
bottom_lip_clearance = 0.15; // [0.05:0.05:0.5]
// Add 4 corner support pillars on the bottom cover to pinch and hold the PCB against the top ledges
add_bottom_pcb_pillars = true;

/* [NeoPixel Diffuser & Baffle Grid] */
// Add the 5x4 internal LED baffle grid (like BlinkeShit case3000)
use_led_grid = true;
// Thin 3D-printed diffuser layer on top of the LEDs (0 = open holes, 0.10-0.25 = thin printed diffuser skin)
diffuser_cover_thickness = 0.20; // [0.00:0.02:1.00]
// Thickness of the dividing walls between LED pixels
grid_thickness = 0.60; // [0.20:0.05:2.00]
// Clearance between the bottom of the LED grid walls and the PCB surface
grid_bottom_clearance = 0.10; // [0.00:0.05:2.00]

/* [Top Face Cutouts] */
// Use parametric PCB cutouts (clean, no Eurorack slots) or import from SVG
use_svg_for_top_holes = false;
// SVG holes file (only used if use_svg_for_top_holes = true)
svg_holes = "svgs/ABK_frontplate_02_holes.svg";
// Cutout for 5x4 NeoPixel LED matrix window (used when use_led_grid = false)
cut_neopixel_window = true;
neopixel_window_w = 45.4; // [40:0.1:55]
neopixel_window_h = 33.1; // [25:0.1:45]
neopixel_window_r = 1.0; // [0:0.1:5]
// Cutout for vertical 1x4 pin headers (J1 & J2 at bottom corners)
cut_pin_headers = true;
header_cutout_w = 4.4; // [3:0.1:8]
header_cutout_h = 12.4; // [8:0.1:18]
// Optional cutout for ATtiny85 DIP-8 socket (U1)
cut_attiny_window = false;
// Optional hole for top-back button (SW1)
cut_sw1_hole = false;

/* [Component Clearance Pockets (Underside Indents)] */
// Add ca. 1.2mm underside clearance pockets above the toggle switch and IC socket
add_component_pockets = true;
// Depth of the underside component clearance pockets (thins the ceiling in these areas)
component_pocket_depth = 1.2; // [0.5:0.1:2.0]
// Width of the toggle switch (SW3) pocket
sw3_pocket_w = 9.0; // [6:0.1:15]
// Height of the toggle switch (SW3) pocket
sw3_pocket_h = 13.5; // [8:0.1:20]
// Toggle switch pocket center X (PCB coords)
sw3_pocket_x = -23.30;
// Toggle switch pocket center Y (PCB coords)
sw3_pocket_y = -25.16;
// Width of the ATtiny85 IC socket (U1) pocket
u1_pocket_w = 10.0; // [6:0.1:16]
// Height of the ATtiny85 IC socket (U1) pocket
u1_pocket_h = 12.5; // [8:0.1:20]
// ATtiny85 IC socket pocket center X (PCB coords, centered at X=-30.00)
u1_pocket_x = -30.00;
// ATtiny85 IC socket pocket center Y (PCB coords, centered at Y=+10.35)
u1_pocket_y = 10.35;

/* [Prototype Top-Mounted Audio Jacks] */
// Cut openings for top-mounted audio jacks (earlier prototype board variant)
cut_top_jack_openings = false;
// Opening cutout style
top_jack_cutout_style = "notch"; // [notch:U-Notch Open to Top Edge (Clearance for Plugs), window:Enclosed Rectangular Window, circular_holes:Circular Holes for Vertical Bushings]
// Extend cutout towards the side walls
top_jack_extend_to_side = "inner_wall"; // [inner_wall:Flush to inner face of side wall (Solid Side Wall), centered:Centered at jack body, outer_wall:Cut through side wall]
// Width of each jack cutout (used for centered mode, or inner span)
top_jack_cutout_w = 14.0; // [10:0.5:25]
// Cutout start Y position behind jack body (PCB coords, jack body rear is at Y=27.57)
top_jack_y_start = 26.5; // [20:0.5:35]
// Cutout end Y position for enclosed window mode
top_jack_window_y_end = 43.5; // [35:0.5:46]
// Corner radius of the jack opening
top_jack_corner_r = 1.0; // [0:0.1:4]
// Opening width/diameter in the back wall for the top-mounted jacks
top_jack_wall_cutout_w = 8.0; // [6:0.1:18]

/* [Side & Back Wall Cutouts] */
// Add cutout on the right side wall for the thumbwheel potentiometer (POT3-Vol1)
add_thumbwheel_cutout = true;
// Length of the thumbwheel slot
thumbwheel_slot_length = 26.0; // [15:0.5:35]
// Height of the thumbwheel slot
thumbwheel_slot_height = 8.0; // [4:0.1:12]
// Corner radius of the thumbwheel slot
thumbwheel_slot_radius = 3.0; // [0:0.1:6]
// Thumbwheel center Y in PCB coordinates
thumbwheel_pcb_y = 8.90; // [-40:0.05:40]
// Thumbwheel center Z in PCB coordinates
thumbwheel_pcb_z = -3.50; // [-15:0.05:5]

// Add cutouts on the back wall for the two 3.5mm audio jacks (Jack1 & Jack2)
add_jack_cutouts = true;
// Diameter of the audio jack holes
jack_hole_dia = 6.0; // [5:0.1:14]
// Open the jack holes to the bottom edge of the top shell (arch/drop-in slot so protruding jack barrels slide in easily)
jack_drop_in_slot = true;
// Left audio jack (Jack1) X in PCB coordinates
jack1_pcb_x = -30.14; // [-40:0.05:40]
// Right audio jack (Jack2) X in PCB coordinates
jack2_pcb_x = 30.60; // [-40:0.05:40]
// Audio jacks center Y in PCB coordinates (Jack1 & Jack2)
jack_pcb_y = 35.67; // [20:0.05:45]
// Audio jacks barrel center Z in PCB coordinates (bottom-mounted: -7.30, top-mounted: +7.30)
jack_pcb_z = -7.30; // [-15:0.05:0]

// Add cutout on the back wall for the USB-C port (J5)
add_usb_cutout = true;
// Width of the USB-C cutout
usb_slot_width = 13.0; // [8:0.1:18]
// Height of the USB-C cutout
usb_slot_height = 7.0; // [3:0.1:12]
// Corner radius of the USB-C cutout
usb_slot_radius = 2.0; // [0:0.1:5]
// USB-C center X in PCB coordinates
usb_pcb_x = -0.34; // [-40:0.05:40]
// USB-C center Y in PCB coordinates
usb_pcb_y = 37.26; // [20:0.05:45]
// USB-C center Z in PCB coordinates
usb_pcb_z = -3.00; // [-15:0.05:0]

/* [3D PCB & Component Models] */
// What to render (use top_shell, bottom_cover, faceplate_only, or print_plate to export STLs for 3D printing)
part_to_show = "assembly"; // [assembly:3D Assembly View, print_plate:Both Parts Flat for 3D Printing, top_shell:Top Shell Only, bottom_cover:Bottom Cover Only, faceplate_only:Top Faceplate Only (Flat)]
// Color of the Top Shell
case_color = "#ff69b4"; // [#ff69b4:Hot Pink, #ff1493:Deep Pink, #ffb6c1:Light Pink, #00e5ff:Cyan, #39ff14:Neon Green, #ff8c00:Orange, #ffd700:Yellow, #9b59b6:Purple, #7aa2c4:Steel Blue, #f5f5f5:White, #333333:Charcoal Black]
// Color of the Bottom Cover
bottom_color = "#ff1493"; // [#ff69b4:Hot Pink, #ff1493:Deep Pink, #ffb6c1:Light Pink, #00e5ff:Cyan, #39ff14:Neon Green, #ff8c00:Orange, #ffd700:Yellow, #9b59b6:Purple, #5a82a6:Steel Blue, #f5f5f5:White, #333333:Charcoal Black]
// Show the 3D PCB in the assembly view
show_pcb = true;
// STL file of the PCB with components
pcb_stl_file = "ABK-20_pcb.stl";
// Show 3D models of PJ-317 audio jacks to inspect openings and alignment
show_jack_models = true;
// Position of jack models in assembly view
jack_model_position = "auto"; // [auto:Match Cutouts Mode, top:Top-Mounted (Prototype), bottom:Bottom-Mounted (Standard Production), both:Show Both Top & Bottom]
// File for jack plastic body
jack_body_stl = "AudioJack_3.5mm_PJ-317_body.stl";
// File for jack metal threaded bushing & pins
jack_metal_stl = "AudioJack_3.5mm_PJ-317_metal.stl";
// Single combined jack STL file
jack_combined_stl = "AudioJack_3.5mm_PJ-317.stl";
// Use two-tone split STL model (colored body + silver metal)
jack_use_split_model = true;
// Color of the 3D jack body
jack_model_body_color = "#e0115f"; // [#e0115f:Ruby Pink, #ff1493:Deep Pink, #ff69b4:Hot Pink, #333333:Charcoal Black, #00e5ff:Cyan]
// Color of the 3D jack metal bushing & pins
jack_model_metal_color = "#d0d0d5";
// Show USB-C port 3D model
show_usb_model = true;
// STL file for USB-C receptacle
usb_stl_file = "USB_C_Receptacle.stl";
// Show the bottom cover in assembly view
show_bottom_cover = true;
// Explode distance for the bottom cover in the assembly view
explode_distance = 15.0; // [0:1:60]
// Opacity of the 3D case in assembly view
assembly_opacity = 0.45; // [0.1:0.05:1.0]

// ---------------------------------------------------------
// Derived Dimensions (Centered at PCB X=0, Y=0, Z=0)
// ---------------------------------------------------------
inner_w = pcb_width + 2 * pcb_xy_clearance;
inner_d = pcb_depth + 2 * pcb_xy_clearance;
inner_r = pcb_corner_radius + pcb_xy_clearance;

outer_w = inner_w + 2 * wall_thickness;
outer_d = inner_d + 2 * wall_thickness;
outer_r = max(inner_r, 2.0) + wall_thickness;

z_pcb_top = pcb_thickness / 2;       // +0.8mm
z_pcb_bot = -pcb_thickness / 2;      // -0.8mm
z_ceiling_inner = pcb_to_ceiling;    // e.g. +8.1mm
z_top_outer = z_ceiling_inner + top_thickness; // e.g. +10.1mm
z_split = -depth_below_pcb;          // e.g. -12.5mm (bottom edge of top_shell)
z_bot_outer = z_split - bottom_thickness; // e.g. -14.5mm

// 5x4 NeoPixel Matrix Constants (extracted from ABK-20.kicad_pcb)
led_cols = 5;
led_rows = 4;
led_pitch_x = 8.922;
led_pitch_y = 7.959;
led_start_x = -17.621; // NEO16 (col 0, row 0) X
led_start_y = -2.075;  // NEO16 (col 0, row 0) Y
led_grid_center_x = led_start_x + (led_cols - 1) * led_pitch_x / 2; // 0.223
led_grid_center_y = led_start_y + (led_rows - 1) * led_pitch_y / 2; // 9.863
led_grid_outer_w = led_cols * led_pitch_x + grid_thickness;
led_grid_outer_h = led_rows * led_pitch_y + grid_thickness;

// ---------------------------------------------------------
// 2D Helper Modules (Centered at 0,0)
// ---------------------------------------------------------
module rounded_rect_center(w, d, r) {
  actual_r = min(r, min(w, d) / 2);
  if (actual_r > 0) {
    offset(r=actual_r, $fn=64)
      square([max(0.01, w - 2 * actual_r), max(0.01, d - 2 * actual_r)], center=true);
  } else {
    square([w, d], center=true);
  }
}

module TopFaceCutouts2D() {
  if (use_svg_for_top_holes) {
    // Shift SVG into PCB center coordinates and mask out the 4 Eurorack mounting slots at top/bottom edges
    intersection() {
      translate([-40.92, -46.14])
        import(svg_holes);
      square([pcb_width, pcb_depth - 2.0], center=true);
    }
  } else {
    // 1. 5x4 NeoPixel Matrix Window (only cut through if not using the LED grid and diffuser_cover_thickness == 0)
    if (!use_led_grid && cut_neopixel_window && diffuser_cover_thickness == 0) {
      translate([led_grid_center_x, led_grid_center_y])
        rounded_rect_center(neopixel_window_w, neopixel_window_h, neopixel_window_r);
    }

    // 2. Slide Potentiometer (RV1) Slot + 2 Mounting Screw Holes
    translate([29.06, 8.78])
      rounded_rect_center(2.8, 22.2, 1.4);
    translate([29.08, 24.27])
      circle(d=2.4, $fn=32);
    translate([29.08, -6.71])
      circle(d=2.4, $fn=32);

    // 3. Bottom Row Controls: Toggle Switch (SW3), Center Pot (POT2-CV1), Pushbutton (SW2)
    translate([-23.30, -25.16])
      circle(d=6.2, $fn=48);
    translate([-0.03, -24.80])
      circle(d=7.8, $fn=48);
    translate([22.17, -25.09])
      circle(d=11.6, $fn=64);

    // 4. Top-Left SMD Pushbutton (SW4)
    translate([-30.47, 21.68])
      circle(d=3.8, $fn=36);

    // 5. Vertical 1x4 Pin Socket Headers (J1 Left & J2 Right)
    if (cut_pin_headers) {
      translate([-32.69, -32.70])
        rounded_rect_center(header_cutout_w, header_cutout_h, 0.6);
      translate([33.24, -32.70])
        rounded_rect_center(header_cutout_w, header_cutout_h, 0.6);
    }

    // 6. Optional ATtiny85 Socket Window (U1)
    if (cut_attiny_window) {
      translate([-30.00, 10.35])
        rounded_rect_center(10.0, 12.5, 1.0);
    }

    // 7. Optional Top-Back Button Hole (SW1)
    if (cut_sw1_hole) {
      translate([-14.72, 34.27])
        circle(d=5.8, $fn=36);
    }

    // 8. Optional Prototype Top-Mounted Audio Jacks (Jack1 & Jack2)
    if (cut_top_jack_openings) {
      if (top_jack_cutout_style == "notch") {
        y_top_limit = outer_d / 2 + 1.0;
        notch_h = y_top_limit - top_jack_y_start;
        notch_center_y = top_jack_y_start + notch_h / 2;

        x_side_limit = (top_jack_extend_to_side == "outer_wall") ? (outer_w / 2 + 1.0) : (inner_w / 2);

        intersection() {
          union() {
            // Left Audio Jack (Jack1)
            if (top_jack_extend_to_side == "centered") {
              translate([jack1_pcb_x, notch_center_y])
                rounded_rect_center(top_jack_cutout_w, notch_h + 0.1, top_jack_corner_r);
            } else {
              // Extends outward to the inner side wall and inward to clear jack
              x_inner = jack1_pcb_x + top_jack_cutout_w / 2; // ~-23.24
              x_outer = -x_side_limit;
              w = x_inner - x_outer;
              translate([x_outer + w / 2, notch_center_y])
                rounded_rect_center(w, notch_h + 0.1, top_jack_corner_r);
            }

            // Right Audio Jack (Jack2)
            if (top_jack_extend_to_side == "centered") {
              translate([jack2_pcb_x, notch_center_y])
                rounded_rect_center(top_jack_cutout_w, notch_h + 0.1, top_jack_corner_r);
            } else {
              // Extends outward to the inner side wall and inward to clear jack
              x_inner = jack2_pcb_x - top_jack_cutout_w / 2; // ~+23.60
              x_outer = x_side_limit;
              w = x_outer - x_inner;
              translate([x_inner + w / 2, notch_center_y])
                rounded_rect_center(w, notch_h + 0.1, top_jack_corner_r);
            }
          }

          // In inner_wall mode, constrain cutout strictly inside the inner cavity so side walls are never cut!
          if (top_jack_extend_to_side == "inner_wall") {
            rounded_rect_center(inner_w, outer_d * 2, inner_r);
          }
        }
      } else if (top_jack_cutout_style == "window") {
        // Enclosed rectangular window
        window_h = top_jack_window_y_end - top_jack_y_start;
        window_center_y = top_jack_y_start + window_h / 2;
        for (jx = [jack1_pcb_x, jack2_pcb_x]) {
          translate([jx, window_center_y])
            rounded_rect_center(top_jack_cutout_w, window_h, top_jack_corner_r);
        }
      } else if (top_jack_cutout_style == "circular_holes") {
        // Circular holes for vertical bushings
        for (jx = [jack1_pcb_x, jack2_pcb_x]) {
          translate([jx, 35.67])
            circle(d=6.5, $fn=48);
        }
      }
    }
  }
}

// 2D footprints of the 20 individual NeoPixel light cells
module LedGridCells2D() {
  for (col = [0:led_cols - 1]) {
    for (row = [0:led_rows - 1]) {
      x_center = led_start_x + col * led_pitch_x;
      y_center = led_start_y + row * led_pitch_y;
      translate([x_center, y_center])
        square([led_pitch_x - grid_thickness, led_pitch_y - grid_thickness], center=true);
    }
  }
}

// 4 Corner Ledges / Pillars 2D footprint (sits in the 4 corners of the inner cavity, clearing J1/J2 and back jacks)
module CornerSupports2D(size) {
  eff_size = size + pcb_xy_clearance;
  difference() {
    intersection() {
      rounded_rect_center(inner_w, inner_d, inner_r);
      union() {
        for (sx = [-1, 1]) {
          // Bottom two corner supports (always safe)
          translate([sx * (inner_w / 2 - eff_size / 2), -1 * (inner_d / 2 - eff_size / 2)])
            square([eff_size, eff_size], center=true);

          // Top two corner supports (suppressed when top-mounted jacks are enabled)
          if (!cut_top_jack_openings) {
            translate([sx * (inner_w / 2 - eff_size / 2), 1 * (inner_d / 2 - eff_size / 2)])
              square([eff_size, eff_size], center=true);
          }
        }
      }
    }
    // Keep clear of J1 & J2 pin sockets and their bottom solder pins
    translate([-32.69, -32.70])
      square([header_cutout_w + 1.6, header_cutout_h + 1.6], center=true);
    translate([33.24, -32.70])
      square([header_cutout_w + 1.6, header_cutout_h + 1.6], center=true);
    // Keep clear of Jack1 & Jack2 bodies at the back corners (standard bottom-mounted jacks)
    if (!cut_top_jack_openings) {
      for (jx = [jack1_pcb_x, jack2_pcb_x]) {
        translate([jx, inner_d / 2 - 6])
          square([12.5, 15.0], center=true);
      }
    }
  }
}

// Chamfered 3D box from z_min to z_max
module ChamferedBox(w, d, r, z_min, z_max, ch_bot = 0, ch_top = 0) {
  h = z_max - z_min;
  hull() {
    if (ch_bot > 0) {
      translate([0, 0, z_min])
        linear_extrude(0.01)
          rounded_rect_center(w - 2 * ch_bot, d - 2 * ch_bot, max(0, r - ch_bot));
      translate([0, 0, z_min + ch_bot])
        linear_extrude(0.01)
          rounded_rect_center(w, d, r);
    } else {
      translate([0, 0, z_min])
        linear_extrude(0.01)
          rounded_rect_center(w, d, r);
    }

    if (ch_top > 0) {
      translate([0, 0, z_max - ch_top - 0.01])
        linear_extrude(0.01)
          rounded_rect_center(w, d, r);
      translate([0, 0, z_max - 0.01])
        linear_extrude(0.01)
          rounded_rect_center(w - 2 * ch_top, d - 2 * ch_top, max(0, r - ch_top));
    } else {
      translate([0, 0, z_max - 0.01])
        linear_extrude(0.01)
          rounded_rect_center(w, d, r);
    }
  }
}

// ---------------------------------------------------------
// Part 1: Top Shell (Integrated Faceplate + Side Walls)
// ---------------------------------------------------------
module top_shell() {
  difference() {
    union() {
      // Main outer body with inner cavity subtracted
      difference() {
        ChamferedBox(outer_w, outer_d, outer_r, z_split, z_top_outer, ch_bot=0, ch_top=outer_edge_chamfer);

        // Main internal PCB cavity (from bottom split up to ceiling)
        translate([0, 0, z_split - 1])
          linear_extrude(z_ceiling_inner - z_split + 1)
            rounded_rect_center(inner_w, inner_d, inner_r);
      }

      // 4 Internal Corner Ledges above the PCB (from z_pcb_top up to z_ceiling_inner)
      // Stops the PCB at exactly z_pcb_top when inserted from the bottom
      translate([0, 0, z_pcb_top])
        linear_extrude(z_ceiling_inner - z_pcb_top)
          CornerSupports2D(pcb_corner_ledge_size);

      // Internal 5x4 NeoPixel Baffle Grid Block (extending from PCB top up to ceiling)
      if (use_led_grid) {
        z_grid_bot = z_pcb_top + grid_bottom_clearance;
        translate([led_grid_center_x, led_grid_center_y, z_grid_bot])
          linear_extrude(z_ceiling_inner - z_grid_bot + 0.01)
            square([led_grid_outer_w, led_grid_outer_h], center=true);
      }
    }

    // 1a. Cut 5x4 NeoPixel light cells (or window) up to diffuser_cover_thickness from the top outer face
    z_led_cut_top = z_top_outer - diffuser_cover_thickness + (diffuser_cover_thickness == 0 ? 1.0 : 0.0);
    if (use_led_grid) {
      translate([0, 0, z_pcb_top - 0.5])
        linear_extrude(z_led_cut_top - (z_pcb_top - 0.5))
          LedGridCells2D();
    } else if (cut_neopixel_window && diffuser_cover_thickness > 0) {
      translate([led_grid_center_x, led_grid_center_y, z_ceiling_inner - 0.5])
        linear_extrude(z_led_cut_top - (z_ceiling_inner - 0.5))
          rounded_rect_center(neopixel_window_w, neopixel_window_h, neopixel_window_r);
    }

    // 1b. Cut Top Faceplate Holes through the ceiling
    translate([0, 0, z_ceiling_inner - 1])
      linear_extrude(top_thickness + 2)
        TopFaceCutouts2D();

    // 2. Cut Right Side Wall Thumbwheel Slot (POT3-Vol1)
    if (add_thumbwheel_cutout) {
      translate([inner_w / 2 - 1, thumbwheel_pcb_y, thumbwheel_pcb_z])
        rotate([90, 0, 90])
          linear_extrude(wall_thickness + 2)
            rounded_rect_center(thumbwheel_slot_length, thumbwheel_slot_height, thumbwheel_slot_radius);
    }

    // 3. Cut Back Wall Audio Jack Holes (Jack1 & Jack2 at Y = +inner_d/2)
    if (add_jack_cutouts) {
      eff_jack_z = cut_top_jack_openings ? -jack_pcb_z : jack_pcb_z; // +7.30mm for top jacks, -7.30mm for bottom jacks
      eff_hole_w = cut_top_jack_openings ? top_jack_wall_cutout_w : jack_hole_dia;
      for (jx = [jack1_pcb_x, jack2_pcb_x]) {
        translate([jx, inner_d / 2 - 1, eff_jack_z])
          rotate([-90, 0, 0])
            linear_extrude(wall_thickness + 2) {
              circle(d=eff_hole_w, $fn=48);
              if (jack_drop_in_slot) {
                // For bottom jacks: arch/keyhole slot down to z_split so protruding jack barrels drop in from below
                // For top jacks: arch/keyhole slot down to z_pcb_top so protruding jack barrels drop in from below
                slot_bot_z = cut_top_jack_openings ? z_pcb_top : z_split;
                drop_h = eff_jack_z - slot_bot_z + 1;
                translate([0, -drop_h / 2])
                  square([eff_hole_w, drop_h], center=true);

                // For top-mounted jacks, also open upward to top ceiling edge
                if (cut_top_jack_openings) {
                  up_h = z_top_outer - eff_jack_z + 1;
                  translate([0, up_h / 2])
                    square([eff_hole_w, up_h], center=true);
                }
              }
            }
      }
    }

    // 4. Cut Back Wall USB-C Slot (J5 at Y = +inner_d/2)
    if (add_usb_cutout) {
      translate([usb_pcb_x, inner_d / 2 - 1, usb_pcb_z])
        rotate([-90, 0, 0])
          linear_extrude(wall_thickness + 2)
            rounded_rect_center(usb_slot_width, usb_slot_height, usb_slot_radius);
    }

    // 5. Underside clearance pockets above Toggle Switch & IC Socket (ca. 1.2mm deep)
    if (add_component_pockets && component_pocket_depth > 0) {
      translate([0, 0, z_ceiling_inner - 0.01])
        linear_extrude(component_pocket_depth + 0.01) {
          // Toggle switch pocket (thins the ceiling to allow switch bushing & body clearance)
          translate([sw3_pocket_x, sw3_pocket_y])
            rounded_rect_center(sw3_pocket_w, sw3_pocket_h, 1.0);

          // ATtiny85 IC socket pocket (gives chip extra headroom under the ceiling)
          translate([u1_pocket_x, u1_pocket_y])
            rounded_rect_center(u1_pocket_w, u1_pocket_h, 1.0);
        }
    }
  }
}

// ---------------------------------------------------------
// Part 2: Bottom Cover (Snap/Friction Lip + Corner PCB Pillars)
// ---------------------------------------------------------
module bottom_cover() {
  lip_outer_w = inner_w - 2 * bottom_lip_clearance;
  lip_outer_d = inner_d - 2 * bottom_lip_clearance;
  lip_outer_r = max(0.1, inner_r - bottom_lip_clearance);

  lip_inner_w = lip_outer_w - 2 * bottom_lip_thickness;
  lip_inner_d = lip_outer_d - 2 * bottom_lip_thickness;
  lip_inner_r = max(0.1, lip_outer_r - bottom_lip_thickness);

  union() {
    // 1. Flat Bottom Cover Baseplate (matches outer profile of Top Shell)
    ChamferedBox(outer_w, outer_d, outer_r, z_bot_outer, z_split, ch_bot=outer_edge_chamfer, ch_top=0);

    // 2. Interlocking Perimeter Lip (slides inside bottom of Top Shell)
    difference() {
      translate([0, 0, z_split])
        linear_extrude(bottom_lip_height)
          rounded_rect_center(lip_outer_w, lip_outer_d, lip_outer_r);

      translate([0, 0, z_split - 0.5])
        linear_extrude(bottom_lip_height + 1)
          rounded_rect_center(lip_inner_w, lip_inner_d, lip_inner_r);

      // Clear out the lip under the two back audio jacks so it never collides with jack bodies
      if (add_jack_cutouts) {
        for (jx = [jack1_pcb_x, jack2_pcb_x]) {
          translate([jx, inner_d / 2, z_split + bottom_lip_height / 2])
            cube([jack_hole_dia + 4, wall_thickness * 4, bottom_lip_height + 2], center=true);
        }
      }
    }

    // 3. 4 Corner Support Pillars (rise from z_split up to z_pcb_bot to hold the PCB against Top Shell ledges)
    if (add_bottom_pcb_pillars) {
      pillar_h = (z_pcb_bot - bottom_lip_clearance) - z_split;
      if (pillar_h > 0) {
        translate([0, 0, z_split])
          linear_extrude(pillar_h)
            intersection() {
              rounded_rect_center(lip_outer_w, lip_outer_d, lip_outer_r);
              CornerSupports2D(pcb_corner_ledge_size);
            }
      }
    }
  }
}

// ---------------------------------------------------------
// Color & Opacity Helper (Converts #RRGGBB to native [r,g,b,alpha] vector for 100% reliable OpenCSG transparency)
// ---------------------------------------------------------
function hex_char_to_int(c) = 
  (c >= "0" && c <= "9") ? ord(c) - ord("0") :
  (c >= "a" && c <= "f") ? ord(c) - ord("a") + 10 :
  (c >= "A" && c <= "F") ? ord(c) - ord("A") + 10 : 0;

function hex2_to_float(s, idx) = 
  (hex_char_to_int(s[idx]) * 16 + hex_char_to_int(s[idx+1])) / 255;

function parse_color_with_alpha(c_str, alpha = 1.0) =
  (len(c_str) >= 7 && c_str[0] == "#") ?
    [hex2_to_float(c_str, 1), hex2_to_float(c_str, 3), hex2_to_float(c_str, 5), alpha] :
    c_str;

// ---------------------------------------------------------
// 3D Component Models (PJ-317 Audio Jacks & USB-C Receptacle)
// ---------------------------------------------------------
module JackModelSingle() {
  if (jack_use_split_model) {
    color(jack_model_body_color)
      import(jack_body_stl, convexity=10);
    color(jack_model_metal_color)
      import(jack_metal_stl, convexity=10);
  } else {
    color(jack_model_body_color)
      import(jack_combined_stl, convexity=10);
  }
}

module JackModels3D() {
  render_top = (jack_model_position == "auto") ? cut_top_jack_openings :
               (jack_model_position == "top" || jack_model_position == "both");
  render_bot = (jack_model_position == "auto") ? !cut_top_jack_openings :
               (jack_model_position == "bottom" || jack_model_position == "both");

  for (jx = [jack1_pcb_x, jack2_pcb_x]) {
    // Top-mounted jacks (prototype: soldered on F.Cu, sitting on top of PCB)
    if (render_top) {
      translate([jx, jack_pcb_y, z_pcb_top])
        rotate([0, 0, -90])
          JackModelSingle();
    }
    // Bottom-mounted jacks (standard production: soldered on B.Cu, hanging under PCB)
    if (render_bot) {
      translate([jx, jack_pcb_y, z_pcb_bot])
        rotate([180, 0, -90])
          JackModelSingle();
    }
  }
}

module UsbModel3D() {
  translate([usb_pcb_x, usb_pcb_y, z_pcb_bot])
    rotate([180, 0, 0])
      color("#b0b0b8")
        import(usb_stl_file, convexity=10);
}

// ---------------------------------------------------------
// Assembly & Print Layout
// ---------------------------------------------------------
module assembly() {
  // 1. Render opaque 3D PCB FIRST
  if (show_pcb) {
    color("#2a6f4e")
      import(pcb_stl_file, convexity=10);
  }

  // 1b. Render 3D Component Models (PJ-317 audio jacks & USB-C receptacle)
  if (show_jack_models) {
    JackModels3D();
  }
  if (show_usb_model) {
    UsbModel3D();
  }

  // 2. Render transparent Top Shell (without render() so OpenCSG alpha blending works!)
  color(parse_color_with_alpha(case_color, assembly_opacity))
    top_shell();

  // 3. Render transparent Bottom Cover (with optional explode distance and visibility toggle)
  if (show_bottom_cover) {
    color(parse_color_with_alpha(bottom_color, assembly_opacity))
      translate([0, 0, -explode_distance])
        bottom_cover();
  }
}

module print_plate() {
  spacing = 10;
  // Flip Top Shell upside-down so the flat top faceplate sits directly on the print bed (zero supports needed!)
  color(case_color)
    translate([-(outer_w / 2 + spacing / 2), 0, z_top_outer])
      rotate([0, 180, 0])
        top_shell();

  // Place Bottom Cover flat on the print bed next to the Top Shell
  color(bottom_color)
    translate([outer_w / 2 + spacing / 2, 0, -z_bot_outer])
      bottom_cover();
}

// ---------------------------------------------------------
// Main Render Logic
// ---------------------------------------------------------
if (part_to_show == "assembly") {
  assembly();
} else if (part_to_show == "print_plate") {
  print_plate();
} else if (part_to_show == "top_shell") {
  // Oriented upside-down on Z=0 for supportless printing
  color(case_color)
    translate([0, 0, z_top_outer])
      rotate([0, 180, 0])
        top_shell();
} else if (part_to_show == "bottom_cover") {
  // Oriented flat on Z=0 for printing
  color(bottom_color)
    translate([0, 0, -z_bot_outer])
      bottom_cover();
} else if (part_to_show == "faceplate_only") {
  // Oriented flat on Z=0 for printing only the top faceplate with LED baffles
  color(case_color)
    translate([0, 0, z_top_outer])
      rotate([0, 180, 0])
        intersection() {
          top_shell();
          translate([0, 0, (z_top_outer + z_pcb_top) / 2])
            cube([outer_w * 2, outer_d * 2, (z_top_outer - z_pcb_top) + 0.1], center=true);
        }
}
