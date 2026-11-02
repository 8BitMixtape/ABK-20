// Parametric Laser Cut Case for 8Bit Mixtape ABK-20
// Top cover (ABK_frontplate_02) fits INSIDE the box walls.

/* [Case Dimensions (Eurorack)] */
// Width of the case in HP (1 HP = 5.08mm)
case_width_hp = 16; // [2:1:104]
// Extra width added to the internal box for clearance/tolerance
case_width_tolerance = 0.0; // [0:0.01:10]
// Depth of the case (Y) (ABK-20 panel height = 92.3mm)
case_depth = 92.3; // [50:0.1:200]
// Extra depth added to the internal box for clearance/tolerance
case_depth_tolerance = 0.0; // [0:0.01:10]
// Internal height of the case (Z).
case_internal_height = 32.0; // [10:1:100]
// Width of the support frame rims at top and bottom.
frame_rim_width = 6.0; // [5:1:30]
// Extend the side panels to overlap the main box (creates a lip and feet)
cheek_extension = 5.0; // [0:1:20]
// Top corner radius for the extended side panels
cheek_radius_top = 8.0; // [0:0.1:20]
// Bottom corner radius for the extended side panels
cheek_radius_bottom = 1.5; // [0:0.1:20]
// Keep the bottom of the cheeks flat / use custom bottom extension
cheek_flat_bottom = true;
// How much the bottom of the cheeks sticks out when cheek_flat_bottom is checked (0 = flush with the box)
cheek_bottom_extension = 2.0; // [0:0.1:20]

/* [Material & Laser] */
// Thickness of the main box panels (bottom, front, back, top strips, top cover)
thickness = 3.0; // [1:0.1:10]
// Thickness of the two side panels / cheeks (e.g. 5mm, 6mm, or 10mm for chunky wood cheeks)
thickness_sides = 5.0; // [1:0.1:20]
// Blind/pocket notches: hide finger joints from outside (engraved on inside of cheeks)
blind_side_notches = true;
// Depth of the blind notch pockets into the side cheeks (must be less than thickness_sides, e.g. 2mm)
side_pocket_depth = 2.0; // [0.5:0.1:10]
// Target length of the interlocking notches
notch_length = 25.0; // [5:1:50]
// Kerf compensation (positive values make notches tighter, e.g., 0.1)
kerf = 0.0; // [0:0.01:0.5]

/* [Eurorack Mounting] */
// Add Eurorack mounting holes to the support rims
add_eurorack_holes = true;
// Distance from the top/bottom edge to the center of the mounting hole (Eurorack standard is 3mm)
eurorack_hole_edge_margin = 3.0; // [0:0.1:10]
// Minimum distance from left/right edges to the outer edge of the hole
eurorack_hole_inset = 3.0; // [0:0.1:20]
// Distance between adjacent holes (1 HP)
eurorack_hp_width = 5.08; // [1:0.01:10]
// Diameter of the mounting holes
eurorack_hole_dia = 2.3; // [2:0.1:5]

/* [SVG Integration & Frontplate Mode] */
// Include the top panel in the layout and assembly
include_top_panel = true;
// Use external SVG files for the top panel (if false, generates 100% native parametric frontplate)
use_svg_for_top_panel = false;
// File name of the top panel outer border (used when use_svg_for_top_panel is true)
svg_border = "svgs/ABK_frontplate_02_border.svg";
// File name of the top panel internal cutouts/holes (used when use_svg_for_top_panel is true)
svg_holes = "svgs/ABK_frontplate_02_holes.svg";
// File name of the top panel engraving
svg_engraving = "svgs/dummy-15hp-engraving.svg";
// Shift the imported SVG or frontplate in X to align with the box edges
svg_shift_x = 0.0; // [-10:0.1:10]
// Shift the imported SVG or frontplate in Y to align with the box edges
svg_shift_y = 0.0; // [-10:0.1:10]
// Show the engraving layer on the 3D dummy? (Can be slow to render)
show_engraving = false;

/* [Parametric Frontplate & LED Matrix] */
// Outer corner radius of the frontplate
frontplate_corner_radius = 2.0; // [0:0.1:10]
// Eurorack mounting slot length on frontplate
frontplate_slot_length = 6.8; // [4:0.1:12]
// Eurorack mounting slot height on frontplate (3.2mm fits M3 screws)
frontplate_slot_height = 3.2; // [2:0.1:6]
// Inset from left/right edge to slot center (standard 16 HP = 7.44mm)
frontplate_slot_inset_x = 7.44; // [4:0.1:15]

// 5x4 NeoPixel Matrix cutout style
matrix_style = "grid"; // [grid:Open 5x4 Grid (20 cells), window:Open Window (Single aperture)]
// Thickness of dividing baffle ribs between LED pixels (grid mode)
matrix_grid_thickness = 0.8; // [0.3:0.05:3.0]
// Corner radius of each matrix cell (grid mode)
matrix_cell_corner_radius = 0.8; // [0:0.1:3.0]
// Extra clearance margin around the matrix (window mode)
matrix_window_margin = 0.8; // [0:0.1:4.0]
// Corner radius of the matrix window (window mode)
matrix_window_radius = 1.5; // [0:0.1:5.0]
// Add underside engraved recess around the matrix for an inset diffuser sheet
add_matrix_pocket = false;
// Extra ledge width for the diffuser sheet recess
matrix_pocket_margin = 1.5; // [0.5:0.1:5.0]

/* [LED Matrix Baffle Grid (Standalone Element)] */
// Add the matrix baffle grid to the main laser cut layout sheet
add_matrix_grid_to_layout = true;
// Match outer size of the baffle grid to the diffuser pocket recess
baffle_grid_match_pocket = false;
// Outer border margin around the 5x4 cells (when not matching pocket)
baffle_grid_margin = 2.0; // [0.5:0.1:10]
// Corner radius of the baffle grid outer border
baffle_grid_corner_radius = 1.0; // [0:0.1:5]
// Show the baffle grid in the 3D assembly view between PCB and frontplate
show_matrix_grid_3d = true;
// Material thickness of the matrix baffle grid (e.g. 2.0mm or 1.5mm)
matrix_grid_thickness_z = 2.0; // [0.5:0.1:6]

/* [Control Cutouts (PCB-relative)] */
// Cut 1x4 pin socket headers (J1 Left & J2 Right)
cut_pin_headers = true;
header_cutout_w = 4.4; // [3:0.1:8]
header_cutout_h = 12.4; // [8:0.1:18]
// Cut top-left SMD pushbutton (SW4)
cut_sw4_hole = true;
sw4_hole_dia = 3.8; // [2:0.1:8]
// Cut bottom controls row (Toggle SW3, Center Pot POT2, Right Switch/Knob SW2)
cut_bottom_controls = true;
toggle_hole_dia = 6.2; // [4:0.1:10]
center_pot_hole_dia = 7.8; // [5:0.1:12]
sw2_hole_dia = 11.6; // [6:0.1:16]
// Cut slide potentiometer slot and screw holes (RV1)
cut_fader_slot = true;
fader_slot_w = 2.8; // [1.5:0.1:6]
fader_slot_l = 22.2; // [15:0.1:35]
fader_screw_dia = 2.4; // [1.5:0.1:4]
// Cut top-back button hole (SW1)
cut_sw1_hole = false;
sw1_hole_dia = 5.8; // [3:0.1:10]
// Cut ATtiny85 socket through-window (U1)
cut_attiny_window = false;

/* [3D PCB Model] */
// Show the 3D PCB + components in the 3D assembly view
show_pcb = true;
// STL file of the PCB with components
pcb_stl_file = "ABK-20_pcb.stl";
// PCB X position relative to top panel origin (40.92 aligns with frontplate holes)
pcb_offset_x = 40.92; // [-100:0.05:100]
// PCB Y position relative to top panel origin (46.14 aligns with frontplate holes)
pcb_offset_y = 46.14; // [-100:0.05:100]
// PCB Z offset below the underside of the top panel (negative = down inside case)
pcb_offset_z = -8.1; // [-50:0.1:20]
// Float the PCB together with the top panel when top_float_distance > 0
pcb_float_with_top = false;

/* [Component Clearance Pockets (Underside Carve)] */
// Carve underside clearance pockets for toggle switch (SW3) and ATtiny85 socket (U1)
add_component_pockets = true;
// Depth of the underside pocket carving into the top cover (e.g. 1.2mm into 3.0mm plate)
component_pocket_depth = 1.2; // [0.5:0.1:2.0]
// Width of the toggle switch (SW3) pocket
sw3_pocket_w = 9.5; // [6:0.1:16]
// Height of the toggle switch (SW3) pocket
sw3_pocket_h = 13.5; // [8:0.1:20]
// Toggle switch pocket center X (PCB coords)
sw3_pocket_x = -23.30; // [-50:0.1:50]
// Toggle switch pocket center Y (PCB coords)
sw3_pocket_y = -25.16; // [-50:0.1:50]
// Width of the ATtiny85 IC socket (U1) pocket
u1_pocket_w = 10.0; // [6:0.1:16]
// Height of the ATtiny85 IC socket (U1) pocket
u1_pocket_h = 12.5; // [8:0.1:20]
// ATtiny85 IC socket pocket center X (PCB coords)
u1_pocket_x = -30.00; // [-50:0.1:50]
// ATtiny85 IC socket pocket center Y (PCB coords)
u1_pocket_y = 10.35; // [-50:0.1:50]
// Mirror the 2D top panel and pockets horizontally so it can be cut/engraved from the backside
mirror_top_for_back_engrave = true;

/* [Wall Cutouts (Thumbwheel, Jacks, USB)] */
// Add cutout for the thumbwheel potentiometer on the side panel
add_thumbwheel_cutout = true;
// Cut the thumbwheel slot on both left and right panels (if false, only on right panel)
thumbwheel_both_sides = false;
// Length of the thumbwheel slot along the panel slope
thumbwheel_slot_length = 22.0; // [10:0.5:40]
// Height of the thumbwheel slot
thumbwheel_slot_height = 5.0; // [2:0.1:15]
// Corner radius of the thumbwheel slot
thumbwheel_slot_radius = 2.5; // [0:0.1:7.5]
// Thumbwheel center Y in PCB coordinates
thumbwheel_pcb_y = 8.90; // [-50:0.05:50]
// Thumbwheel center Z in PCB coordinates
thumbwheel_pcb_z = -3.50; // [-20:0.05:10]
// Add cutouts on the back wall for the two 3.5mm audio jacks
add_jack_cutouts = true;
// Diameter of the audio jack holes on the back wall
jack_hole_dia = 8.0; // [5:0.1:15]
// Left audio jack (Jack1) X in PCB coordinates
jack1_pcb_x = -30.10; // [-50:0.05:50]
// Right audio jack (Jack2) X in PCB coordinates
jack2_pcb_x = 30.02; // [-50:0.05:50]
// Audio jacks front barrel Y in PCB coordinates
jack_pcb_y = 42.67; // [0:0.05:60]
// Audio jacks barrel center Z in PCB coordinates
jack_pcb_z = -7.30; // [-20:0.05:10]
// Fine vertical offset for jack cutouts (moves holes down/up to center on angled barrels)
jack_z_offset = -1.2; // [-10:0.1:10]
// Add cutout on the back wall for the USB-C port
add_usb_cutout = true;
// Width of the USB-C cutout on the back wall
usb_slot_width = 11.0; // [8:0.1:20]
// Height of the USB-C cutout on the back wall
usb_slot_height = 5.5; // [3:0.1:15]
// Corner radius of the USB-C cutout
usb_slot_radius = 2.0; // [0:0.1:7.5]
// USB-C center X in PCB coordinates
usb_pcb_x = -0.34; // [-50:0.05:50]
// USB-C front Y in PCB coordinates
usb_pcb_y = 40.66; // [0:0.05:60]
// USB-C center Z in PCB coordinates
usb_pcb_z = -2.43; // [-20:0.05:10]
// Fine vertical offset for USB-C cutout (moves slot down/up to center on port)
usb_z_offset = -0.9; // [-10:0.1:10]

/* [Case Tilt] */
// Angle to tilt the top panel towards the user
panel_tilt = 12; // [0:1:45]

/* [Display Mode] */
// What to render
part_to_show = "assembly"; // [assembly:3D Assembly, layout:2D Layout (All), layout_main:2D Layout (Main Sheet), layout_sides:2D Layout (Sides Sheet), side_cuts:2D Cheek Through-Cuts, side_engrave:2D Cheek Mortise Engraving, top_pockets:2D Top Underside Clearance Pockets, matrix_grid:2D Matrix Baffle Grid, bottom:Bottom Panel, front:Front Panel, back:Back Panel, left:Left Panel, right:Right Panel, top_dummy:Top Cover (Dummy)]
// Distance to float the top panel above the case in the assembly view
top_float_distance = 0.0; // [0:1:200]
// Opacity of the 3D assembly models
assembly_opacity = 0.6; // [0.1:0.05:1.0]

// Effective penetration depth of the side tabs into the cheeks
tab_depth_sides = blind_side_notches ? min(side_pocket_depth, max(0.5, thickness_sides - 0.5)) : thickness_sides;

// Internal dimensions (fit the cover)
iw = case_width_hp * 5.08 + case_width_tolerance;
id = case_depth * cos(panel_tilt) + thickness * sin(panel_tilt) + case_depth_tolerance;

// Back height (extrapolated to perfectly match the continued slope of the top panel)
case_internal_height_back = case_internal_height + id * tan(panel_tilt);

// Outer dimensions
ow = iw + 2 * thickness_sides;
od = id + 2 * thickness;
actual_cheek_bottom_ext = (cheek_extension > 0) ? (cheek_flat_bottom ? cheek_bottom_extension : cheek_extension) : 0;

// Calculated number of notches per edge
num_notches_x = max(1, floor(iw / (2 * notch_length)));
num_notches_y = max(1, floor(od / (2 * notch_length)));
num_notches_z_front = max(1, floor(case_internal_height / (2 * notch_length)));
num_notches_z_back = max(1, floor(case_internal_height_back / (2 * notch_length)));

// Actual notch lengths (adjusted to fit exactly)
len_x = iw / (2 * num_notches_x + 1);
len_y = od / (2 * num_notches_y + 1);
len_z_front = case_internal_height / (2 * num_notches_z_front + 1);
len_z_back = case_internal_height_back / (2 * num_notches_z_back + 1);

// Tilted Tab Calculations
tab_len_front = thickness * (1 + 2 * sin(panel_tilt)) / cos(panel_tilt);
shift_back = thickness * tan(panel_tilt);
tab_len_back = thickness * (1 + sin(panel_tilt)) / cos(panel_tilt);

z_max_front = case_internal_height - thickness / cos(panel_tilt);
z_min_front = case_internal_height - 2 * thickness / cos(panel_tilt) - thickness * tan(panel_tilt);
slot_h_front = z_max_front - z_min_front;

z_max_back = case_internal_height - thickness / cos(panel_tilt) + (id + thickness) * tan(panel_tilt);
z_min_back = case_internal_height - 2 * thickness / cos(panel_tilt) + id * tan(panel_tilt);
slot_h_back = z_max_back - z_min_back;

module offset_kerf() {
  if (kerf > 0) {
    offset(delta=kerf / 2) children();
  } else {
    children();
  }
}

module offset_rounded(ext, rad) {
  if (rad > 0) {
    offset(r=rad, $fn=64)
      offset(delta=ext - rad)
        children();
  } else {
    offset(delta=ext)
      children();
  }
}

module rounded_slot(w, h, r) {
  actual_r = min(r, min(w, h) / 2);
  if (actual_r > 0) {
    offset(r=actual_r, $fn=48)
      square([max(0.01, w - 2 * actual_r), max(0.01, h - 2 * actual_r)], center=true);
  } else {
    square([w, h], center=true);
  }
}

// ---------------------------------------------------------
// Panels
// ---------------------------------------------------------
module bottom_panel() {
  offset_kerf() difference() {
    union() {
      // Main central floor between the cheeks
      translate([thickness_sides, 0])
        square([iw, od]);

      // Left tabs into left cheek
      for (i = [0:2 * num_notches_y]) {
        if (i % 2 == 1) {
          translate([thickness_sides - tab_depth_sides, i * len_y])
            square([tab_depth_sides + 0.1, len_y]);
        }
      }

      // Right tabs into right cheek
      for (i = [0:2 * num_notches_y]) {
        if (i % 2 == 1) {
          translate([thickness_sides + iw - 0.1, i * len_y])
            square([tab_depth_sides + 0.1, len_y]);
        }
      }
    }

    // Slots for Front wall tabs (Y=0..thickness)
    for (i = [0:2 * num_notches_x]) {
      if (i % 2 == 0) {
        translate([thickness_sides + i * len_x, -0.1])
          square([len_x, thickness + 0.2]);
      }
    }

    // Slots for Back wall tabs (Y=od-thickness..od)
    for (i = [0:2 * num_notches_x]) {
      if (i % 2 == 0) {
        translate([thickness_sides + i * len_x, od - thickness - 0.1])
          square([len_x, thickness + 0.2]);
      }
    }
  }
}

module top_strip_front() {
  offset_kerf() difference() {
    union() {
      square([iw, frame_rim_width]);

      // Tabs pointing FRONT into front_panel
      for (i = [0:2 * num_notches_x]) {
        if (i % 2 == 1) {
          translate([i * len_x, -tab_len_front])
            square([len_x, tab_len_front + 0.1]);
        }
      }

      // Tabs pointing LEFT into left_panel (X = -tab_depth_sides)
      translate([-tab_depth_sides, 0])
        square([tab_depth_sides + 0.1, frame_rim_width]);

      // Tabs pointing RIGHT into right_panel (X = iw)
      translate([iw - 0.1, 0])
        square([tab_depth_sides + 0.1, frame_rim_width]);
    }

    if (add_eurorack_holes) {
      num_hp = floor((iw - 2 * eurorack_hole_inset - eurorack_hole_dia) / eurorack_hp_width);
      start_x = (iw - num_hp * eurorack_hp_width) / 2;
      hole_y_front = eurorack_hole_edge_margin;
      for (i = [0:num_hp]) {
        translate([start_x + i * eurorack_hp_width, hole_y_front])
          circle(d=eurorack_hole_dia, $fn=30);
      }
    }
  }
}

module top_strip_back() {
  offset_kerf() difference() {
    union() {
      square([iw, frame_rim_width]);

      // Tabs pointing BACK into back_panel
      for (i = [0:2 * num_notches_x]) {
        if (i % 2 == 1) {
          translate([i * len_x, frame_rim_width - 0.1])
            square([len_x, tab_len_back + 0.1]);
        }
      }

      // Tabs pointing LEFT into left_panel (X = -tab_depth_sides)
      translate([-tab_depth_sides, 0])
        square([tab_depth_sides + 0.1, frame_rim_width]);

      // Tabs pointing RIGHT into right_panel (X = iw)
      translate([iw - 0.1, 0])
        square([tab_depth_sides + 0.1, frame_rim_width]);
    }

    if (add_eurorack_holes) {
      num_hp = floor((iw - 2 * eurorack_hole_inset - eurorack_hole_dia) / eurorack_hp_width);
      start_x = (iw - num_hp * eurorack_hp_width) / 2;
      hole_y_back = frame_rim_width - eurorack_hole_edge_margin + shift_back;
      for (i = [0:num_hp]) {
        translate([start_x + i * eurorack_hp_width, hole_y_back])
          circle(d=eurorack_hole_dia, $fn=30);
      }
    }
  }
}

module side_panel_profile() {
  if (cheek_extension > 0) {
    intersection() {
      // Top and side profile with top corner radius
      offset_rounded(cheek_extension, cheek_radius_top)
        polygon([
          [0, -thickness - actual_cheek_bottom_ext - cheek_radius_top - 10], 
          [od, -thickness - actual_cheek_bottom_ext - cheek_radius_top - 10], 
          [od, case_internal_height_back], 
          [od - thickness, case_internal_height_back], 
          [thickness, case_internal_height], 
          [0, case_internal_height]
        ]);
      // Bottom and side profile with bottom extension and bottom corner radius
      offset_rounded(cheek_extension, cheek_radius_bottom)
        translate([0, -thickness - actual_cheek_bottom_ext + cheek_extension])
          square([od, case_internal_height_back + actual_cheek_bottom_ext + cheek_extension + 2 * cheek_radius_bottom + 40]);
    }
  } else {
    polygon([
      [0, 0], 
      [od, 0], 
      [od, case_internal_height_back], 
      [od - thickness, case_internal_height_back], 
      [thickness, case_internal_height], 
      [0, case_internal_height]
    ]);
  }
}

module side_panel_notches() {
  // Holes for front panel tabs (at Y_box=0..thickness, meaning X_panel=0..thickness)
  for (i = [0:2 * num_notches_z_front]) {
    if (i % 2 == 0) {
      translate([-0.1, i * len_z_front])
        square([thickness + 0.2, len_z_front]);
    }
  }
  // Holes for back panel tabs (at Y_box=od-thickness..od)
  for (i = [0:2 * num_notches_z_back]) {
    if (i % 2 == 0) {
      translate([od - thickness - 0.1, i * len_z_back])
        square([thickness + 0.2, len_z_back]);
    }
  }

  // Slot for top_strip_front
  translate([thickness, case_internal_height])
    rotate([0, 0, panel_tilt])
    translate([0, -2 * thickness])
    square([frame_rim_width, thickness]);

  // Slot for top_strip_back
  translate([thickness, case_internal_height])
    rotate([0, 0, panel_tilt])
    translate([case_depth - shift_back - frame_rim_width, -2 * thickness])
    square([frame_rim_width, thickness]);

  // Holes for bottom panel tabs
  if (cheek_extension > 0) {
    for (i = [0:2 * num_notches_y]) {
      if (i % 2 == 1) {
        translate([i * len_y, -thickness - 0.1])
          square([len_y, thickness + 0.2]);
      }
    }
  }
}

module side_panel_thumbwheel() {
  translate([thickness, case_internal_height])
    rotate([0, 0, panel_tilt])
    translate([svg_shift_y + pcb_offset_y + thumbwheel_pcb_y, -thickness + pcb_offset_z + thumbwheel_pcb_z])
    rounded_slot(thumbwheel_slot_length, thumbwheel_slot_height, thumbwheel_slot_radius);
}

module side_panel_cuts(has_thumbwheel = false) {
  offset_kerf() difference() {
    side_panel_profile();
    if (!blind_side_notches) {
      side_panel_notches();
    }
    if (has_thumbwheel && add_thumbwheel_cutout) {
      side_panel_thumbwheel();
    }
  }
}

module side_panel(has_thumbwheel = false) {
  if (blind_side_notches) {
    // Through-cuts (outer border + thumbwheel slot)
    side_panel_cuts(has_thumbwheel);

    // Pocket mortise engraving (inside face)
    color("blue")
      offset_kerf() side_panel_notches();
  } else {
    side_panel_cuts(has_thumbwheel);
  }
}

module cheek_3d(has_thumbwheel = false, is_right = false) {
  if (blind_side_notches) {
    difference() {
      // Solid outer cheek with only through-cuts (e.g. thumbwheel slot)
      linear_extrude(thickness_sides)
        side_panel_cuts(has_thumbwheel);

      // Carve out mortise pockets on the INSIDE face
      if (is_right) {
        // Right cheek: local Z=0 is inside face (facing -X toward box)
        translate([0, 0, -0.05])
          linear_extrude(tab_depth_sides + 0.05)
            offset_kerf() side_panel_notches();
      } else {
        // Left cheek: local Z=thickness_sides is inside face (facing +X toward box)
        translate([0, 0, thickness_sides - tab_depth_sides])
          linear_extrude(tab_depth_sides + 0.1)
            offset_kerf() side_panel_notches();
      }
    }
  } else {
    linear_extrude(thickness_sides)
      side_panel(has_thumbwheel);
  }
}

module left_panel() {
  side_panel(has_thumbwheel = thumbwheel_both_sides);
}

module right_panel() {
  side_panel(has_thumbwheel = true);
}

module front_panel() {
  // X_panel maps to X_box (thickness to ow-thickness = iw)
  // Y_panel maps to Z_box
  offset_kerf() {
    difference() {
      square([iw, case_internal_height]);

      // Oversized slots for top_strip_front
      for (i = [0:2 * num_notches_x]) {
        if (i % 2 == 1) {
          translate([i * len_x, z_min_front])
            square([len_x, slot_h_front]);
        }
      }
    }

    // Tabs into left panel
    for (i = [0:2 * num_notches_z_front]) {
      if (i % 2 == 0) {
        translate([-tab_depth_sides, i * len_z_front])
          square([tab_depth_sides + 0.1, len_z_front]);
      }
    }

    // Tabs into right panel
    for (i = [0:2 * num_notches_z_front]) {
      if (i % 2 == 0) {
        translate([iw - 0.1, i * len_z_front])
          square([tab_depth_sides + 0.1, len_z_front]);
      }
    }

    // Tabs into bottom panel
    for (i = [0:2 * num_notches_x]) {
      if (i % 2 == 0) {
        translate([i * len_x, -thickness])
          square([len_x, thickness + 0.1]);
      }
    }
  }
}

module back_panel() {
  offset_kerf() {
    difference() {
      square([iw, case_internal_height_back]);

      // Oversized slots for top_strip_back
      for (i = [0:2 * num_notches_x]) {
        if (i % 2 == 1) {
          translate([i * len_x, z_min_back])
            square([len_x, slot_h_back]);
        }
      }

      // Cutouts for 3.5mm audio jacks (Jack1 & Jack2)
      if (add_jack_cutouts) {
        jack_ty = svg_shift_y + pcb_offset_y + jack_pcb_y;
        jack_tz = -thickness + pcb_offset_z + jack_pcb_z;
        jack_y_back = case_internal_height + jack_ty * sin(panel_tilt) + jack_tz * cos(panel_tilt) + jack_z_offset;
        translate([svg_shift_x + pcb_offset_x + jack1_pcb_x, jack_y_back])
          circle(d=jack_hole_dia, $fn=48);
        translate([svg_shift_x + pcb_offset_x + jack2_pcb_x, jack_y_back])
          circle(d=jack_hole_dia, $fn=48);
      }

      // Cutout for USB-C port (J5)
      if (add_usb_cutout) {
        usb_ty = svg_shift_y + pcb_offset_y + usb_pcb_y;
        usb_tz = -thickness + pcb_offset_z + usb_pcb_z;
        usb_y_back = case_internal_height + usb_ty * sin(panel_tilt) + usb_tz * cos(panel_tilt) + usb_z_offset;
        translate([svg_shift_x + pcb_offset_x + usb_pcb_x, usb_y_back])
          rounded_slot(usb_slot_width, usb_slot_height, usb_slot_radius);
      }
    }

    // Tabs into left panel
    for (i = [0:2 * num_notches_z_back]) {
      if (i % 2 == 0) {
        translate([-tab_depth_sides, i * len_z_back])
          square([tab_depth_sides + 0.1, len_z_back]);
      }
    }

    // Tabs into right panel
    for (i = [0:2 * num_notches_z_back]) {
      if (i % 2 == 0) {
        translate([iw - 0.1, i * len_z_back])
          square([tab_depth_sides + 0.1, len_z_back]);
      }
    }

    // Tabs into bottom panel
    for (i = [0:2 * num_notches_x]) {
      if (i % 2 == 0) {
        translate([i * len_x, -thickness])
          square([len_x, thickness + 0.1]);
      }
    }
  }
}

// 5x4 NeoPixel Matrix Constants (extracted from ABK-20.kicad_pcb)
led_cols = 5;
led_rows = 4;
led_pitch_x = 8.922;
led_pitch_y = 7.959;
led_start_x = -17.621; // NEO16 (col 0, row 0) X relative to PCB center
led_start_y = -2.075;  // NEO16 (col 0, row 0) Y relative to PCB center
led_grid_center_x = led_start_x + (led_cols - 1) * led_pitch_x / 2; // 0.223
led_grid_center_y = led_start_y + (led_rows - 1) * led_pitch_y / 2; // 9.863
cell_w = led_pitch_x - matrix_grid_thickness;
cell_h = led_pitch_y - matrix_grid_thickness;

// 2D PCB-relative cutouts for all controls and LED matrix
module top_panel_cutouts_pcb() {
  // 1. 5x4 NeoPixel Matrix Apertures
  if (matrix_style == "window") {
    win_w = (led_cols - 1) * led_pitch_x + cell_w + 2 * matrix_window_margin;
    win_h = (led_rows - 1) * led_pitch_y + cell_h + 2 * matrix_window_margin;
    translate([led_grid_center_x, led_grid_center_y])
      rounded_slot(win_w, win_h, matrix_window_radius);
  } else {
    // "grid" style: 20 individual light cells
    for (col = [0 : led_cols - 1]) {
      for (row = [0 : led_rows - 1]) {
        cx = led_start_x + col * led_pitch_x;
        cy = led_start_y + row * led_pitch_y;
        translate([cx, cy])
          rounded_slot(cell_w, cell_h, matrix_cell_corner_radius);
      }
    }
  }

  // 2. Slide Potentiometer (RV1) Slot & Screw Holes
  if (cut_fader_slot) {
    translate([29.06, 8.78])
      rounded_slot(fader_slot_w, fader_slot_l, fader_slot_w / 2);
    translate([29.08, 24.27])
      circle(d=fader_screw_dia, $fn=32);
    translate([29.08, -6.71])
      circle(d=fader_screw_dia, $fn=32);
  }

  // 3. Bottom Row Controls: Toggle (SW3), Center Pot (POT2), Right Switch/Knob (SW2)
  if (cut_bottom_controls) {
    // Toggle Switch (SW3)
    translate([-23.30, -25.16])
      circle(d=toggle_hole_dia, $fn=48);
    // Center Potentiometer (POT2-CV1)
    translate([-0.03, -24.80])
      circle(d=center_pot_hole_dia, $fn=48);
    // Right Switch / Knob (SW2)
    translate([22.17, -25.09])
      circle(d=sw2_hole_dia, $fn=48);
  }

  // 4. Top-Left SMD Pushbutton (SW4)
  if (cut_sw4_hole) {
    translate([-30.47, 21.68])
      circle(d=sw4_hole_dia, $fn=36);
  }

  // 5. Vertical 1x4 Pin Socket Headers (J1 Left & J2 Right)
  if (cut_pin_headers) {
    translate([-32.69, -32.70])
      rounded_slot(header_cutout_w, header_cutout_h, 0.6);
    translate([33.24, -32.70])
      rounded_slot(header_cutout_w, header_cutout_h, 0.6);
  }

  // 6. Optional Top-Back Button Hole (SW1)
  if (cut_sw1_hole) {
    translate([-14.72, 34.27])
      circle(d=sw1_hole_dia, $fn=36);
  }

  // 7. Optional ATtiny85 Socket Through-Window (U1)
  if (cut_attiny_window) {
    translate([u1_pocket_x, u1_pocket_y])
      rounded_slot(u1_pocket_w, u1_pocket_h, 1.0);
  }
}

// 2D Parametric Frontplate (100% native OpenSCAD math aligned to PCB)
module top_panel_parametric() {
  difference() {
    // Outer perimeter plate
    translate([iw / 2, case_depth / 2])
      rounded_slot(iw, case_depth, frontplate_corner_radius);

    // Eurorack mounting slots (top & bottom edges)
    if (add_eurorack_holes) {
      slot_y_bot = eurorack_hole_edge_margin;
      slot_y_top = case_depth - eurorack_hole_edge_margin;
      slot_x_positions = (iw >= 40) ? [frontplate_slot_inset_x, iw - frontplate_slot_inset_x] : [iw / 2];
      for (x = slot_x_positions) {
        translate([x, slot_y_bot])
          rounded_slot(frontplate_slot_length, frontplate_slot_height, frontplate_slot_height / 2);
        translate([x, slot_y_top])
          rounded_slot(frontplate_slot_length, frontplate_slot_height, frontplate_slot_height / 2);
      }
    }

    // All control & LED matrix cutouts placed in PCB coordinates
    translate([svg_shift_x + pcb_offset_x, svg_shift_y + pcb_offset_y])
      top_panel_cutouts_pcb();
  }
}

// 2D Top Cover
module top_panel() {
  if (use_svg_for_top_panel) {
    translate([svg_shift_x, svg_shift_y]) {
      difference() {
        import(svg_border);
        import(svg_holes);
      }
    }
  } else {
    top_panel_parametric();
  }
}

module top_engraving() {
  if (use_svg_for_top_panel) {
    translate([svg_shift_x, svg_shift_y]) {
      import(svg_engraving);
    }
  }
}

module top_panel_pockets() {
  translate([svg_shift_x + pcb_offset_x, svg_shift_y + pcb_offset_y]) {
    // Toggle switch pocket (thins plate so switch bushing threads nicely to front nut)
    translate([sw3_pocket_x, sw3_pocket_y])
      rounded_slot(sw3_pocket_w, sw3_pocket_h, 1.0);

    // ATtiny85 IC socket pocket (gives chip & socket extra headroom under the front plate)
    translate([u1_pocket_x, u1_pocket_y])
      rounded_slot(u1_pocket_w, u1_pocket_h, 1.0);

    // Optional LED matrix diffuser recess pocket (for inset acrylic window)
    if (add_matrix_pocket) {
      win_w = (led_cols - 1) * led_pitch_x + cell_w + 2 * matrix_window_margin;
      win_h = (led_rows - 1) * led_pitch_y + cell_h + 2 * matrix_window_margin;
      pock_w = win_w + 2 * matrix_pocket_margin;
      pock_h = win_h + 2 * matrix_pocket_margin;
      translate([led_grid_center_x, led_grid_center_y])
        rounded_slot(pock_w, pock_h, matrix_window_radius);
    }
  }
}

module top_cover_3d() {
  if (add_component_pockets) {
    difference() {
      linear_extrude(thickness) top_panel();
      // Carve underside clearance pockets
      translate([0, 0, -0.01])
        linear_extrude(component_pocket_depth + 0.01)
          top_panel_pockets();
    }
  } else {
    linear_extrude(thickness) top_panel();
  }
}

module top_panel_with_pockets() {
  top_panel();
  if (add_component_pockets) {
    color("blue") top_panel_pockets();
  }
}

module top_panel_layout() {
  if (mirror_top_for_back_engrave) {
    translate([iw, 0]) mirror([1, 0]) top_panel();
  } else {
    top_panel();
  }
}

module top_panel_pockets_layout() {
  if (mirror_top_for_back_engrave) {
    translate([iw, 0]) mirror([1, 0]) top_panel_pockets();
  } else {
    top_panel_pockets();
  }
}

// 2D Standalone Matrix Baffle Grid (Light isolation spacer between PCB and frontplate)
module matrix_baffle_grid() {
  outer_w = (baffle_grid_match_pocket && add_matrix_pocket) ? 
            ((led_cols - 1) * led_pitch_x + cell_w + 2 * matrix_window_margin + 2 * matrix_pocket_margin) :
            ((led_cols - 1) * led_pitch_x + cell_w + 2 * baffle_grid_margin);
  outer_h = (baffle_grid_match_pocket && add_matrix_pocket) ? 
            ((led_rows - 1) * led_pitch_y + cell_h + 2 * matrix_window_margin + 2 * matrix_pocket_margin) :
            ((led_rows - 1) * led_pitch_y + cell_h + 2 * baffle_grid_margin);
  outer_r = (baffle_grid_match_pocket && add_matrix_pocket) ? matrix_window_radius : baffle_grid_corner_radius;

  offset_kerf() difference() {
    // Outer perimeter
    rounded_slot(outer_w, outer_h, outer_r);

    // 20 Individual LED Cell Light Chambers
    for (col = [0 : led_cols - 1]) {
      for (row = [0 : led_rows - 1]) {
        cx = (col - (led_cols - 1) / 2) * led_pitch_x;
        cy = (row - (led_rows - 1) / 2) * led_pitch_y;
        translate([cx, cy])
          rounded_slot(cell_w, cell_h, matrix_cell_corner_radius);
      }
    }
  }
}

// ---------------------------------------------------------
// Assembly and Layout
// ---------------------------------------------------------
module assembly() {
  // 3D PCB + components (drawn first so it remains visible through all transparent panels)
  if (show_pcb) {
    pcb_float_z = pcb_float_with_top ? top_float_distance : 0;
    translate([thickness_sides, thickness, case_internal_height + thickness + pcb_float_z]) {
      rotate([panel_tilt, 0, 0]) {
        translate([svg_shift_x + pcb_offset_x, svg_shift_y + pcb_offset_y, -thickness + pcb_offset_z]) {
          color("#2a6f4e")
            import(pcb_stl_file, convexity=10);
        }
      }
    }
  }

  // Baffle grid spacer between PCB and frontplate
  if (show_matrix_grid_3d) {
    translate([thickness_sides, thickness, case_internal_height + thickness + top_float_distance]) {
      rotate([panel_tilt, 0, 0]) {
        translate([svg_shift_x + pcb_offset_x + led_grid_center_x, svg_shift_y + pcb_offset_y + led_grid_center_y, -thickness - matrix_grid_thickness_z]) {
          color("#202020", 0.95)
            linear_extrude(matrix_grid_thickness_z)
              matrix_baffle_grid();
        }
      }
    }
  }

  // Bottom frame (now solid)
  color("#8b5a2b", assembly_opacity)
    linear_extrude(thickness) bottom_panel();

  // Top front strip
  color("#8b5a2b", assembly_opacity)
    translate([thickness_sides, thickness, case_internal_height + thickness])
      rotate([panel_tilt, 0, 0])
      translate([0, 0, -2 * thickness])
      linear_extrude(thickness) top_strip_front();

  // Top back strip
  color("#8b5a2b", assembly_opacity)
    translate([thickness_sides, thickness, case_internal_height + thickness])
      rotate([panel_tilt, 0, 0])
      translate([0, case_depth - shift_back - frame_rim_width, -2 * thickness])
      linear_extrude(thickness) top_strip_back();

  // Top cover visualized floating above
  if (include_top_panel) {
    translate([thickness_sides, thickness, case_internal_height + thickness + top_float_distance]) {
      rotate([panel_tilt, 0, 0]) {
        translate([0, 0, -thickness]) {
          color("#faedcd", assembly_opacity)
            top_cover_3d();
            
          if (show_engraving) {
            color("#5c4033", assembly_opacity)
              translate([0, 0, thickness + 0.01])
                linear_extrude(0.1) top_engraving();
          }
        }
      }
    }
  }

  // Left cheek
  color("#a0522d", assembly_opacity)
    translate([0, 0, thickness])
      rotate([90, 0, 90])
        cheek_3d(has_thumbwheel = thumbwheel_both_sides, is_right = false);

  // Right cheek
  color("#cd853f", assembly_opacity)
    translate([ow - thickness_sides, 0, thickness])
      rotate([90, 0, 90])
        cheek_3d(has_thumbwheel = true, is_right = true);

  // Front
  color("#deb887", assembly_opacity)
    translate([thickness_sides, thickness, thickness])
      rotate([90, 0, 0])
        linear_extrude(thickness) front_panel();

  // Back
  color("#d2b48c", assembly_opacity)
    translate([thickness_sides, od, thickness])
      rotate([90, 0, 0])
        linear_extrude(thickness) back_panel();
}

module layout_main() {
  spacing = 5;
  tab = thickness;

  // Row 1: Bottom panel and Top cover
  translate([tab, tab]) bottom_panel();
  
  translate([tab + ow + spacing, 0]) {
    if (include_top_panel) {
      top_panel_layout();
      if (show_engraving) {
        color("black") top_engraving();
      }
    }
  }

  // Row 2: Front, Back, and Strips
  row2_y = max(od + tab, case_depth) + spacing + tab;
  
  translate([tab, row2_y]) front_panel();
  translate([tab * 3 + iw + spacing, row2_y]) back_panel();
  
  strip_x = tab * 5 + iw * 2 + spacing * 2;
  translate([strip_x, row2_y + tab_len_front]) top_strip_front();
  translate([strip_x, row2_y + tab_len_front + frame_rim_width + spacing + tab]) top_strip_back();

  // Optional Standalone Matrix Baffle Grid (fits in Row 1 below the support strips)
  if (add_matrix_grid_to_layout) {
    baffle_outer_w = (baffle_grid_match_pocket && add_matrix_pocket) ? 
              ((led_cols - 1) * led_pitch_x + cell_w + 2 * matrix_window_margin + 2 * matrix_pocket_margin) :
              ((led_cols - 1) * led_pitch_x + cell_w + 2 * baffle_grid_margin);
    baffle_outer_h = (baffle_grid_match_pocket && add_matrix_pocket) ? 
              ((led_rows - 1) * led_pitch_y + cell_h + 2 * matrix_window_margin + 2 * matrix_pocket_margin) :
              ((led_rows - 1) * led_pitch_y + cell_h + 2 * baffle_grid_margin);
    
    grid_pos_x = strip_x + baffle_outer_w / 2;
    grid_pos_y = tab + baffle_outer_h / 2;
    translate([grid_pos_x, grid_pos_y])
      matrix_baffle_grid();
  }
}

module layout_sides() {
  spacing = 5;
  translate([cheek_extension, 0]) side_panel_cuts(has_thumbwheel = thumbwheel_both_sides);
  translate([2 * od + cheek_extension * 3 + spacing, 0]) mirror([1, 0]) side_panel_cuts(has_thumbwheel = true);
}

module layout_sides_pockets() {
  spacing = 5;
  translate([cheek_extension, 0]) side_panel_notches();
  translate([2 * od + cheek_extension * 3 + spacing, 0]) mirror([1, 0]) side_panel_notches();
}

module layout_main_pockets() {
  spacing = 5;
  tab = thickness;
  translate([tab + ow + spacing, 0]) {
    if (include_top_panel && add_component_pockets) {
      top_panel_pockets_layout();
    }
  }
}

module layout() {
  spacing = 5;
  tab = thickness;

  // Row 1: Bottom panel and Top cover
  translate([tab, tab]) bottom_panel();
  
  translate([tab + ow + spacing, 0]) {
    if (include_top_panel) {
      top_panel_layout();
      if (show_engraving) {
        color("black") top_engraving();
      }
    }
  }

  // Row 2: Left and Right Panels
  row2_y = max(od + tab, case_depth) + spacing + max(cheek_extension, actual_cheek_bottom_ext) + tab;
  
  translate([cheek_extension, row2_y]) left_panel();
  translate([2 * od + cheek_extension * 3 + spacing, row2_y]) mirror([1, 0]) right_panel();

  // Row 3: Front, Back, and Strips
  row3_y = row2_y + case_internal_height_back + cheek_extension + spacing + tab;
  
  translate([tab, row3_y]) front_panel();
  translate([tab * 3 + iw + spacing, row3_y]) back_panel();
  
  strip_x = tab * 5 + iw * 2 + spacing * 2;
  translate([strip_x, row3_y + tab_len_front]) top_strip_front();
  translate([strip_x, row3_y + tab_len_front + frame_rim_width + spacing + tab]) top_strip_back();

  // Optional Standalone Matrix Baffle Grid (fits in Row 1 below the support strips)
  if (add_matrix_grid_to_layout) {
    baffle_outer_w = (baffle_grid_match_pocket && add_matrix_pocket) ? 
              ((led_cols - 1) * led_pitch_x + cell_w + 2 * matrix_window_margin + 2 * matrix_pocket_margin) :
              ((led_cols - 1) * led_pitch_x + cell_w + 2 * baffle_grid_margin);
    baffle_outer_h = (baffle_grid_match_pocket && add_matrix_pocket) ? 
              ((led_rows - 1) * led_pitch_y + cell_h + 2 * matrix_window_margin + 2 * matrix_pocket_margin) :
              ((led_rows - 1) * led_pitch_y + cell_h + 2 * baffle_grid_margin);
    
    grid_pos_x = strip_x + baffle_outer_w / 2;
    grid_pos_y = tab + baffle_outer_h / 2;
    translate([grid_pos_x, grid_pos_y])
      matrix_baffle_grid();
  }
}

// ---------------------------------------------------------
// Main Render Logic
// ---------------------------------------------------------
if (part_to_show == "assembly") {
  assembly();
} else if (part_to_show == "layout") {
  layout();
} else if (part_to_show == "layout_main") {
  layout_main();
} else if (part_to_show == "layout_main_pockets") {
  layout_main_pockets();
} else if (part_to_show == "layout_sides") {
  layout_sides();
} else if (part_to_show == "layout_sides_pockets") {
  layout_sides_pockets();
} else if (part_to_show == "matrix_grid") {
  matrix_baffle_grid();
} else if (part_to_show == "top_dummy" || part_to_show == "top") {
  top_panel_layout();
  if (show_engraving) {
    color("black") top_engraving();
  }
} else if (part_to_show == "top_pockets") {
  top_panel_pockets_layout();
} else if (part_to_show == "side_cuts") {
  side_panel_cuts(true);
} else if (part_to_show == "side_engrave") {
  side_panel_notches();
} else if (part_to_show == "bottom") {
  bottom_panel();
} else if (part_to_show == "left") {
  left_panel();
} else if (part_to_show == "right") {
  mirror([1, 0]) right_panel();
} else if (part_to_show == "front") {
  front_panel();
} else if (part_to_show == "back") {
  back_panel();
}
