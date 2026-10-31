// ==============================================================================
// Parametric 3D-Printed Eurorack Front Plate with LED Matrix Frames for ABK-20
// Fits the ABK-20 Laser Cut Case (16 HP, 80.96 x 92.28 mm) or Eurorack Rails.
//
// Features:
//  1. Exact laser cut panel size (16 HP = 80.96 x 92.28 mm) with Eurorack slots.
//  2. 5x4 NeoPixel Matrix Baffle Grid extending downward to eliminate light bleed.
//  3. Choice of Top Matrix Style:
//     - "diffuser_grid": Integrated thin 3D-printed diffuser skin (0.2mm)
//     - "open_frame_grid": Crisp open framed apertures with optional top bevel
//     - "window_recess": Stepped recess for an inset acrylic diffuser window
//  4. Precise cutouts for all controls (fader, center pot, switches, buttons, headers).
//  5. Optional underside PCB corner standoffs/ledges to lock PCB height.
//  6. Print-ready orientation (top face down on bed for a silky smooth finish).
// ==============================================================================

/* [Panel Dimensions (Matches Laser Cut Model)] */
// Panel width preset or custom
panel_width_mode = "svg_exact"; // [svg_exact:Laser Cut Exact (80.96 mm), eurorack_16hp:Standard 16 HP (81.28 mm), custom:Custom Width]
// Custom panel width in mm (used if panel_width_mode == custom)
custom_panel_width = 81.0; // [50:0.1:150]
// Panel depth/height in mm (ABK-20 standard = 92.28 mm)
panel_depth = 92.283; // [60:0.1:150]
// Front plate face thickness in mm (3.0mm matches laser cut acrylic, 2.5mm prints fast)
panel_thickness = 2.5; // [1.5:0.1:5.0]
// Outer corner radius of the panel
panel_corner_radius = 2.0; // [0:0.1:10.0]
// Chamfer on the top outer perimeter edges
outer_edge_chamfer = 0.8; // [0:0.1:2.0]

/* [Eurorack Mounting Slots] */
// Add Eurorack mounting slots at top & bottom edges
add_eurorack_slots = true;
// Length of each mounting slot in mm
eurorack_slot_length = 6.8; // [4:0.1:12]
// Height of each mounting slot in mm (3.2mm fits M3 screws comfortably)
eurorack_slot_height = 3.2; // [2.5:0.1:5]
// Distance from top/bottom edge to slot center (Eurorack standard = 3.0mm)
eurorack_slot_edge_margin = 3.0; // [1.5:0.1:6]
// Inset from left/right edge to slot center (standard 16 HP = 7.44mm)
eurorack_slot_inset_x = 7.44; // [4:0.1:15]
// Add counterbore recess on top face for M3 screw heads
add_slot_counterbore = true;
// Depth of the screw head counterbore recess
counterbore_depth = 0.8; // [0:0.1:2.0]
// Counterbore width
counterbore_width = 8.8; // [6:0.1:14]
// Counterbore height
counterbore_height = 5.6; // [4:0.1:10]

/* [NeoPixel 5x4 Matrix Frames & Baffle Grid] */
// Top appearance of the LED matrix
matrix_style = "diffuser_grid"; // [diffuser_grid:Thin Printed Diffuser Skin, open_frame_grid:Open Framed Cells, window_recess:Recessed Frame for Acrylic Window]
// Thickness of the top diffuser skin (0 = open holes, 0.2 = translucent 1-2 layers)
diffuser_cover_thickness = 0.20; // [0.00:0.02:1.00]
// Thickness of the dividing baffle walls between LED pixels
grid_thickness = 0.60; // [0.20:0.05:2.00]
// Depth the baffle grid extends downward from panel underside toward the PCB
baffle_depth = 6.5; // [0:0.1:12.0]
// Inner corner radius of each light cell aperture
cell_corner_radius = 0.6; // [0:0.1:2.0]
// Bevel/chamfer on the top frame edge of each cell (open_frame_grid only)
cell_top_chamfer = 0.4; // [0:0.1:1.2]
// Depth of the stepped recess for acrylic window (window_recess mode)
acrylic_recess_depth = 1.0; // [0.5:0.1:2.5]
// Extra margin around the 5x4 matrix for the acrylic recess
acrylic_recess_margin = 1.2; // [0.5:0.1:4.0]

/* [Control Cutouts & Optional Openings] */
// Cutout for vertical 1x4 pin socket headers (J1 Left & J2 Right)
cut_pin_headers = true;
header_cutout_w = 4.4; // [3:0.1:8]
header_cutout_h = 12.4; // [8:0.1:18]
// Optional cutout for ATtiny85 DIP-8 socket (U1)
cut_attiny_window = false;
// Optional cutout for top-back button (SW1)
cut_sw1_hole = false;

/* [Component Clearance Pockets (Underside Indents)] */
// Add ca. 1.2mm underside clearance pockets above the toggle switch and IC socket
add_component_pockets = true;
// Depth of the underside component clearance pockets (thins the plate in these areas)
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
// Extend cutout towards the outer side edges
top_jack_extend_to_side = "centered"; // [centered:Centered at jack body (Solid Outer Edge), outer_wall:All the way to outer side edge (Open Corner)]
// Width of each jack cutout (used for centered mode, or inner span)
top_jack_cutout_w = 14.0; // [10:0.5:25]
// Cutout start Y position behind jack body (PCB coords, jack body rear is at Y=27.57)
top_jack_y_start = 26.5; // [20:0.5:35]
// Cutout end Y position for enclosed window mode
top_jack_window_y_end = 43.5; // [35:0.5:46]
// Corner radius of the jack opening
top_jack_corner_r = 1.0; // [0:0.1:4]
// Left audio jack (Jack1) center X (PCB coords)
top_jack1_x = -30.14;
// Right audio jack (Jack2) center X (PCB coords)
top_jack2_x = 30.60;
// Audio jack center Y (used for circular_holes mode)
top_jack_hole_y = 35.67;
// Hole diameter for circular_holes mode
top_jack_hole_dia = 6.5; // [5:0.1:10]

/* [PCB Positioning & Underside Standoffs] */
// Center-to-center offset between SVG panel origin and PCB center (matches ABK-20 laser cut case)
pcb_offset_x = 40.92;
pcb_offset_y = 46.14;
// PCB thickness in mm
pcb_thickness = 1.6;
// Distance from PCB center to underside of the front plate (8.1mm tilted, 11.0mm flat)
pcb_to_ceiling = 8.1; // [5:0.1:15]
// Add 4 corner standoff pillars on the underside to support/locate the PCB
add_pcb_corner_standoffs = true;
// Size of corner standoffs
pcb_standoff_size = 5.5; // [3:0.5:10]

/* [Display & 3D Print Layout] */
// View and export mode
part_to_show = "assembly"; // [assembly:3D Assembly with PCB, print_flat_top_down:Ready to Print (Top Face on Bed - Best Finish!), print_flat_top_up:Ready to Print (Top Face Up), frontplate_only:3D Front Plate Only]
// Front plate filament color
panel_color = "#ff69b4"; // [#ff69b4:Hot Pink, #ff1493:Deep Pink, #00e5ff:Cyan, #39ff14:Neon Green, #ff8c00:Orange, #ffd700:Yellow, #9b59b6:Purple, #333333:Charcoal Black, #f5f5f5:White]
// Show 3D PCB in assembly view
show_pcb = true;
// 3D PCB model file
pcb_stl_file = "ABK-20_pcb.stl";
// Opacity of the panel in assembly view
assembly_opacity = 0.45; // [0.1:0.05:1.0]
// Explode distance between front plate and PCB in assembly view
explode_distance = 0.0; // [0:1:40]

// ---------------------------------------------------------
// Derived Dimensions (Coordinates centered at PCB center X=0, Y=0)
// ---------------------------------------------------------
eff_panel_width = (panel_width_mode == "svg_exact") ? 80.955 :
                  (panel_width_mode == "eurorack_16hp") ? 16 * 5.08 :
                  custom_panel_width;

// Shift needed to center the panel around the PCB center
panel_center_shift_x = eff_panel_width / 2 - pcb_offset_x; // ~-0.44 mm
panel_center_shift_y = panel_depth / 2 - pcb_offset_y;      // ~0.00 mm

// Z levels (Z=0 is the UNDERSIDE of the front plate):
// Front plate body sits from Z = 0 up to Z = panel_thickness
z_plate_bot = 0;
z_plate_top = panel_thickness;

// PCB top surface sits below Z=0
z_pcb_center = -pcb_to_ceiling;
z_pcb_top = z_pcb_center + pcb_thickness / 2;

// 5x4 NeoPixel Matrix Constants (extracted from ABK-20.kicad_pcb)
led_cols = 5;
led_rows = 4;
led_pitch_x = 8.922;
led_pitch_y = 7.959;
led_start_x = -17.621; // NEO16 (col 0, row 0) X relative to PCB center
led_start_y = -2.075;  // NEO16 (col 0, row 0) Y relative to PCB center
led_grid_center_x = led_start_x + (led_cols - 1) * led_pitch_x / 2; // 0.223
led_grid_center_y = led_start_y + (led_rows - 1) * led_pitch_y / 2; // 9.863
led_grid_outer_w = led_cols * led_pitch_x + grid_thickness;
led_grid_outer_h = led_rows * led_pitch_y + grid_thickness;

cell_w = led_pitch_x - grid_thickness;
cell_h = led_pitch_y - grid_thickness;

$fn = 64;

// ---------------------------------------------------------
// 2D Helper Modules
// ---------------------------------------------------------
module rounded_rect_center(w, d, r) {
  actual_r = min(r, min(w, d) / 2);
  if (actual_r > 0) {
    offset(r=actual_r)
      square([max(0.01, w - 2 * actual_r), max(0.01, d - 2 * actual_r)], center=true);
  } else {
    square([w, d], center=true);
  }
}

// 2D Outer perimeter outline of the front plate (in PCB-centered coordinates)
module PanelOutline2D() {
  translate([panel_center_shift_x, panel_center_shift_y])
    rounded_rect_center(eff_panel_width, panel_depth, panel_corner_radius);
}

// 2D Eurorack Mounting Slots (in PCB-centered coordinates)
module EurorackSlots2D() {
  slot_y_top = panel_center_shift_y + panel_depth / 2 - eurorack_slot_edge_margin;
  slot_y_bot = panel_center_shift_y - panel_depth / 2 + eurorack_slot_edge_margin;

  // Inset from left and right edges
  slot_x_right = panel_center_shift_x + eff_panel_width / 2 - eurorack_slot_inset_x;
  slot_x_left  = panel_center_shift_x - eff_panel_width / 2 + eurorack_slot_inset_x;

  for (x = [slot_x_left, slot_x_right]) {
    // Bottom mounting slots
    translate([x, slot_y_bot])
      rounded_rect_center(eurorack_slot_length, eurorack_slot_height, eurorack_slot_height / 2);

    // Top mounting slots (only if not cut away by top jack notches)
    if (!cut_top_jack_openings || top_jack_cutout_style == "circular_holes") {
      translate([x, slot_y_top])
        rounded_rect_center(eurorack_slot_length, eurorack_slot_height, eurorack_slot_height / 2);
    }
  }
}

// 2D Counterbore Recesses for M3 screw heads
module EurorackCounterbores2D() {
  slot_y_top = panel_center_shift_y + panel_depth / 2 - eurorack_slot_edge_margin;
  slot_y_bot = panel_center_shift_y - panel_depth / 2 + eurorack_slot_edge_margin;

  slot_x_right = panel_center_shift_x + eff_panel_width / 2 - eurorack_slot_inset_x;
  slot_x_left  = panel_center_shift_x - eff_panel_width / 2 + eurorack_slot_inset_x;

  for (x = [slot_x_left, slot_x_right]) {
    // Bottom counterbores
    translate([x, slot_y_bot])
      rounded_rect_center(counterbore_width, counterbore_height, counterbore_height / 2);

    // Top counterbores (only if not cut away by top jack notches)
    if (!cut_top_jack_openings || top_jack_cutout_style == "circular_holes") {
      translate([x, slot_y_top])
        rounded_rect_center(counterbore_width, counterbore_height, counterbore_height / 2);
    }
  }
}

// 2D Prototype Top-Mounted Audio Jack Openings
module TopJackCutouts2D() {
  if (cut_top_jack_openings) {
    if (top_jack_cutout_style == "notch") {
      y_top_limit = panel_center_shift_y + panel_depth / 2 + 1.0;
      notch_h = y_top_limit - top_jack_y_start;
      notch_center_y = top_jack_y_start + notch_h / 2;

      // Left Jack (Jack 1)
      if (top_jack_extend_to_side == "centered") {
        translate([top_jack1_x, notch_center_y])
          rounded_rect_center(top_jack_cutout_w, notch_h + 0.1, top_jack_corner_r);
      } else {
        // Extends all the way to the left outer edge of the panel
        x_inner = top_jack1_x + top_jack_cutout_w / 2; // ~-23.24
        x_outer = panel_center_shift_x - eff_panel_width / 2 - 1.0;
        w = x_inner - x_outer;
        translate([x_outer + w / 2, notch_center_y])
          rounded_rect_center(w, notch_h + 0.1, top_jack_corner_r);
      }

      // Right Jack (Jack 2)
      if (top_jack_extend_to_side == "centered") {
        translate([top_jack2_x, notch_center_y])
          rounded_rect_center(top_jack_cutout_w, notch_h + 0.1, top_jack_corner_r);
      } else {
        // Extends all the way to the right outer edge of the panel
        x_inner = top_jack2_x - top_jack_cutout_w / 2; // ~+23.60
        x_outer = panel_center_shift_x + eff_panel_width / 2 + 1.0;
        w = x_outer - x_inner;
        translate([x_inner + w / 2, notch_center_y])
          rounded_rect_center(w, notch_h + 0.1, top_jack_corner_r);
      }
    } else if (top_jack_cutout_style == "window") {
      // Enclosed rectangular window
      window_h = top_jack_window_y_end - top_jack_y_start;
      window_center_y = top_jack_y_start + window_h / 2;
      for (jx = [top_jack1_x, top_jack2_x]) {
        translate([jx, window_center_y])
          rounded_rect_center(top_jack_cutout_w, window_h, top_jack_corner_r);
      }
    } else if (top_jack_cutout_style == "circular_holes") {
      // Circular holes for vertical bushings
      for (jx = [top_jack1_x, top_jack2_x]) {
        translate([jx, top_jack_hole_y])
          circle(d=top_jack_hole_dia, $fn=48);
      }
    }
  }
}

// 2D Control Cutouts (in PCB-centered coordinates)
module ControlCutouts2D() {
  // 1. Slide Potentiometer (RV1) Slot + 2 Mounting Screw Holes
  translate([29.06, 8.78])
    rounded_rect_center(2.8, 22.2, 1.4);
  translate([29.08, 24.27])
    circle(d=2.4, $fn=32);
  translate([29.08, -6.71])
    circle(d=2.4, $fn=32);

  // 2. Bottom Row Controls: Toggle Switch (SW3), Center Pot (POT2-CV1), Pushbutton (SW2)
  translate([-23.30, -25.16])
    circle(d=6.2, $fn=48);
  translate([-0.03, -24.80])
    circle(d=7.8, $fn=48);
  translate([22.17, -25.09])
    circle(d=11.6, $fn=64);

  // 3. Top-Left SMD Pushbutton (SW4)
  translate([-30.47, 21.68])
    circle(d=3.8, $fn=36);

  // 4. Vertical 1x4 Pin Socket Headers (J1 Left & J2 Right)
  if (cut_pin_headers) {
    translate([-32.69, -32.70])
      rounded_rect_center(header_cutout_w, header_cutout_h, 0.6);
    translate([33.24, -32.70])
      rounded_rect_center(header_cutout_w, header_cutout_h, 0.6);
  }

  // 5. Optional ATtiny85 Socket Window (U1)
  if (cut_attiny_window) {
    translate([-30.00, 10.35])
      rounded_rect_center(10.0, 12.5, 1.0);
  }

  // 6. Optional Top-Back Button Hole (SW1)
  if (cut_sw1_hole) {
    translate([-14.72, 34.27])
      circle(d=5.8, $fn=36);
  }

  // 7. Optional Prototype Top-Mounted Audio Jacks (Jack1 & Jack2)
  TopJackCutouts2D();
}

// 2D Footprints of the 20 individual light cells
module LedGridCells2D() {
  for (col = [0:led_cols - 1]) {
    for (row = [0:led_rows - 1]) {
      x_center = led_start_x + col * led_pitch_x;
      y_center = led_start_y + row * led_pitch_y;
      translate([x_center, y_center])
        rounded_rect_center(cell_w, cell_h, cell_corner_radius);
    }
  }
}

// 4 Corner Standoffs 2D footprint (aligns with 75x80mm PCB corners)
module PcbStandoffs2D(size) {
  difference() {
    intersection() {
      PanelOutline2D();
      union() {
        for (sx = [-1, 1]) {
          // Bottom two corner standoffs (always safe)
          translate([sx * (75.0 / 2 - size / 2), -1 * (80.0 / 2 - size / 2)])
            square([size, size], center=true);

          // Top two corner standoffs (suppressed when top-mounted jacks are present)
          if (!cut_top_jack_openings) {
            translate([sx * (75.0 / 2 - size / 2), 1 * (80.0 / 2 - size / 2)])
              square([size, size], center=true);
          }
        }
      }
    }
    // Keep clear of J1/J2 pin headers
    translate([-32.69, -32.70])
      square([header_cutout_w + 1.6, header_cutout_h + 1.6], center=true);
    translate([33.24, -32.70])
      square([header_cutout_w + 1.6, header_cutout_h + 1.6], center=true);
  }
}

// Chamfered 3D Plate with smooth top edge bevel
module ChamferedPlate(w, d, r, z_min, z_max, ch_top = 0) {
  hull() {
    translate([panel_center_shift_x, panel_center_shift_y, z_min])
      linear_extrude(0.01)
        rounded_rect_center(w, d, r);

    if (ch_top > 0) {
      translate([panel_center_shift_x, panel_center_shift_y, z_max - ch_top - 0.01])
        linear_extrude(0.01)
          rounded_rect_center(w, d, r);
      translate([panel_center_shift_x, panel_center_shift_y, z_max - 0.01])
        linear_extrude(0.01)
          rounded_rect_center(w - 2 * ch_top, d - 2 * ch_top, max(0.1, r - ch_top));
    } else {
      translate([panel_center_shift_x, panel_center_shift_y, z_max - 0.01])
        linear_extrude(0.01)
          rounded_rect_center(w, d, r);
    }
  }
}

// ---------------------------------------------------------
// 3D Front Plate Solid
// ---------------------------------------------------------
module front_plate_3d() {
  difference() {
    union() {
      // 1. Main Solid Plate Body (from Z=0 to Z=panel_thickness)
      ChamferedPlate(eff_panel_width, panel_depth, panel_corner_radius, z_plate_bot, z_plate_top, ch_top=outer_edge_chamfer);

      // 2. Downward 5x4 Matrix Baffle Block (from Z = -baffle_depth up to Z = 0)
      if (baffle_depth > 0) {
        translate([led_grid_center_x, led_grid_center_y, -baffle_depth])
          linear_extrude(baffle_depth + 0.01)
            square([led_grid_outer_w, led_grid_outer_h], center=true);
      }

      // 3. Optional Underside PCB Corner Standoffs (from Z = z_pcb_top up to Z = 0)
      if (add_pcb_corner_standoffs) {
        standoff_h = -z_pcb_top;
        if (standoff_h > 0) {
          translate([0, 0, z_pcb_top])
            linear_extrude(standoff_h + 0.01)
              PcbStandoffs2D(pcb_standoff_size);
        }
      }
    }

    // --- Subtractions ---

    // A. 5x4 NeoPixel Matrix Light Chambers
    // Depth depends on matrix_style:
    //  - diffuser_grid: cuts from bottom up to (z_plate_top - diffuser_cover_thickness)
    //  - open_frame_grid: cuts completely through top face
    //  - window_recess: cuts completely through, plus a stepped top recess
    z_cut_bot = -baffle_depth - 1.0;
    z_cut_top = (matrix_style == "diffuser_grid") ? 
                (z_plate_top - diffuser_cover_thickness) : 
                (z_plate_top + 1.0);

    translate([0, 0, z_cut_bot])
      linear_extrude(z_cut_top - z_cut_bot)
        LedGridCells2D();

    // B. Beveled Chamfer on Top Apertures (open_frame_grid mode)
    if (matrix_style == "open_frame_grid" && cell_top_chamfer > 0) {
      translate([0, 0, z_plate_top - cell_top_chamfer])
        for (col = [0:led_cols - 1]) {
          for (row = [0:led_rows - 1]) {
            x_c = led_start_x + col * led_pitch_x;
            y_c = led_start_y + row * led_pitch_y;
            translate([x_c, y_c, 0])
              hull() {
                linear_extrude(0.01)
                  rounded_rect_center(cell_w, cell_h, cell_corner_radius);
                translate([0, 0, cell_top_chamfer + 0.01])
                  linear_extrude(0.01)
                    rounded_rect_center(cell_w + 2 * cell_top_chamfer, cell_h + 2 * cell_top_chamfer, cell_corner_radius + cell_top_chamfer);
              }
          }
        }
    }

    // C. Stepped Recess for Acrylic Diffuser Window (window_recess mode)
    if (matrix_style == "window_recess") {
      recess_w = led_grid_outer_w + 2 * acrylic_recess_margin;
      recess_h = led_grid_outer_h + 2 * acrylic_recess_margin;
      translate([led_grid_center_x, led_grid_center_y, z_plate_top - acrylic_recess_depth])
        linear_extrude(acrylic_recess_depth + 1.0)
          rounded_rect_center(recess_w, recess_h, 1.5);
    }

    // D. Control Cutouts (through the full plate)
    translate([0, 0, -1.0])
      linear_extrude(panel_thickness + 2.0)
        ControlCutouts2D();

    // E. Eurorack Mounting Slots
    if (add_eurorack_slots) {
      translate([0, 0, -1.0])
        linear_extrude(panel_thickness + 2.0)
          EurorackSlots2D();

      // F. M3 Counterbore Recesses on Top Face
      if (add_slot_counterbore && counterbore_depth > 0) {
        translate([0, 0, z_plate_top - counterbore_depth])
          linear_extrude(counterbore_depth + 1.0)
            EurorackCounterbores2D();
      }
    }

    // G. Underside Clearance Indents / Pockets above Toggle Switch & IC Socket (ca. 1.2mm deep)
    if (add_component_pockets && component_pocket_depth > 0) {
      translate([0, 0, -0.01])
        linear_extrude(component_pocket_depth + 0.01) {
          // Toggle switch pocket (thins the plate to 1.3-1.8mm so switch bushing reaches front nut)
          translate([sw3_pocket_x, sw3_pocket_y])
            rounded_rect_center(sw3_pocket_w, sw3_pocket_h, 1.0);

          // ATtiny85 IC socket pocket (gives chip extra headroom under the front plate)
          translate([u1_pocket_x, u1_pocket_y])
            rounded_rect_center(u1_pocket_w, u1_pocket_h, 1.0);
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
// Assembly & Print Layouts
// ---------------------------------------------------------
// Visual representation of the two top-mounted 3.5mm PJ-317 audio jacks (from hardware/3d_models)
module TopJackModel3D() {
  for (jx = [top_jack1_x, top_jack2_x]) {
    translate([jx, 35.67, z_pcb_top])
      rotate([0, 0, -90]) {
        color("#e0115f")
          import("AudioJack_3.5mm_PJ-317_body.stl", convexity=10);
        color("#d0d0d5")
          import("AudioJack_3.5mm_PJ-317_metal.stl", convexity=10);
      }
  }
}

module assembly() {
  // 1. 3D PCB Model (rendered first for clean OpenGL depth blending)
  if (show_pcb) {
    translate([0, 0, z_pcb_center - explode_distance])
      color("#2a6f4e")
        import(pcb_stl_file, convexity=10);

    // Show prototype top-mounted jacks sitting in their cutouts
    if (cut_top_jack_openings) {
      translate([0, 0, -explode_distance])
        TopJackModel3D();
    }
  }

  // 2. 3D Front Plate (without render() so OpenCSG alpha transparency works!)
  color(parse_color_with_alpha(panel_color, assembly_opacity))
    front_plate_3d();
}

module print_flat_top_down() {
  // Flipping the plate upside-down (top face on the print bed)
  // produces a breathtaking, silky-smooth finish on a textured PEI or glass build sheet!
  color(panel_color)
    translate([0, 0, z_plate_top])
      rotate([180, 0, 0])
        front_plate_3d();
}

module print_flat_top_up() {
  // Natural flat orientation on print bed
  color(panel_color)
    translate([0, 0, baffle_depth])
      front_plate_3d();
}

// ---------------------------------------------------------
// Main Render Dispatcher
// ---------------------------------------------------------
if (part_to_show == "assembly") {
  assembly();
} else if (part_to_show == "print_flat_top_down") {
  print_flat_top_down();
} else if (part_to_show == "print_flat_top_up") {
  print_flat_top_up();
} else if (part_to_show == "frontplate_only") {
  color(panel_color)
    front_plate_3d();
}

