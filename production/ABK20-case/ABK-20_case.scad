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
// Thickness of the material
thickness = 3.0; // [1:0.1:10]
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

/* [SVG Integration] */
// Include the top panel in the layout and assembly
include_top_panel = true;
// Use the SVG files for the top panel (if false, generates a simple blank panel with holes)
use_svg_for_top_panel = true;
// File name of the top panel outer border
svg_border = "svgs/ABK_frontplate_02_border.svg";
// File name of the top panel internal cutouts/holes
svg_holes = "svgs/ABK_frontplate_02_holes.svg";
// File name of the top panel engraving
svg_engraving = "svgs/dummy-15hp-engraving.svg";
// Shift the imported SVG in X to align with the box edges
svg_shift_x = 0.0; // [-10:0.1:10]
// Shift the imported SVG in Y to align with the box edges
svg_shift_y = 0.0; // [-10:0.1:10]
// Show the engraving layer on the 3D dummy? (Can be slow to render)
show_engraving = false;

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
jack1_pcb_x = -30.24; // [-50:0.05:50]
// Right audio jack (Jack2) X in PCB coordinates
jack2_pcb_x = 30.60; // [-50:0.05:50]
// Audio jacks front barrel Y in PCB coordinates
jack_pcb_y = 42.67; // [0:0.05:60]
// Audio jacks barrel center Z in PCB coordinates
jack_pcb_z = -7.30; // [-20:0.05:10]
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

/* [Case Tilt] */
// Angle to tilt the top panel towards the user
panel_tilt = 12; // [0:1:45]

/* [Display Mode] */
// What to render
part_to_show = "assembly"; // [assembly:3D Assembly, layout:2D Layout, bottom:Bottom Panel, front:Front Panel, back:Back Panel, left:Left Panel, right:Right Panel, top_dummy:Top Cover (Dummy)]
// Distance to float the top panel above the case in the assembly view
top_float_distance = 0.0; // [0:1:200]
// Opacity of the 3D assembly models
assembly_opacity = 0.6; // [0.1:0.05:1.0]

// Internal dimensions (fit the cover)
iw = case_width_hp * 5.08 + case_width_tolerance;
id = case_depth * cos(panel_tilt) + thickness * sin(panel_tilt) + case_depth_tolerance;

// Back height (extrapolated to perfectly match the continued slope of the top panel)
case_internal_height_back = case_internal_height + id * tan(panel_tilt);

// Outer dimensions
ow = iw + 2 * thickness;
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
      square([ow, od]);

      // Holes for Left wall (X=0..thickness)
      for (i = [0:2 * num_notches_y]) {
        if (i % 2 == 0) {
          // slots
          translate([-0.1, i * len_y])
            square([thickness + 0.2, len_y]);
        }
      }
      // Holes for Right wall (X=ow-thickness..ow)
      for (i = [0:2 * num_notches_y]) {
        if (i % 2 == 0) {
          // slots
          translate([ow - thickness - 0.1, i * len_y])
            square([thickness + 0.2, len_y]);
        }
      }
      // Holes for Front wall (Y=0..thickness)
      for (i = [0:2 * num_notches_x]) {
        if (i % 2 == 0) {
          // slots
          translate([thickness + i * len_x, -0.1])
            square([len_x, thickness + 0.2]);
        }
      }
      // Holes for Back wall (Y=od-thickness..od)
      for (i = [0:2 * num_notches_x]) {
        if (i % 2 == 0) {
          // slots
          translate([thickness + i * len_x, od - thickness - 0.1])
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

      // Tabs pointing LEFT into left_panel (X = -thickness)
      translate([-thickness, 0])
        square([thickness + 0.1, frame_rim_width]);

      // Tabs pointing RIGHT into right_panel (X = iw)
      translate([iw - 0.1, 0])
        square([thickness + 0.1, frame_rim_width]);
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

      // Tabs pointing LEFT into left_panel (X = -thickness)
      translate([-thickness, 0])
        square([thickness + 0.1, frame_rim_width]);

      // Tabs pointing RIGHT into right_panel (X = iw)
      translate([iw - 0.1, 0])
        square([thickness + 0.1, frame_rim_width]);
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

module side_panel(has_thumbwheel = false) {
  // X_panel maps to Y_box (0 to od), Y_panel maps to Z_box (0 to case_internal_height)
  offset_kerf() {
    difference() {
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

      // Rounded slot for thumbwheel potentiometer (aligned with tilted PCB)
      if (has_thumbwheel && add_thumbwheel_cutout) {
        translate([thickness, case_internal_height])
          rotate([0, 0, panel_tilt])
          translate([svg_shift_y + pcb_offset_y + thumbwheel_pcb_y, -thickness + pcb_offset_z + thumbwheel_pcb_z])
          rounded_slot(thumbwheel_slot_length, thumbwheel_slot_height, thumbwheel_slot_radius);
      }

      if (cheek_extension > 0) {
        // Holes for bottom panel tabs
        for (i = [0:2 * num_notches_y]) {
          if (i % 2 == 1) {
            translate([i * len_y, -thickness - 0.1])
              square([len_y, thickness + 0.2]);
          }
        }
      }
    }
    
    if (cheek_extension == 0) {
      // Bottom tabs (into Bottom panel)
      for (i = [0:2 * num_notches_y]) {
        if (i % 2 == 0) {
          translate([i * len_y, -thickness])
            square([len_y, thickness + 0.1]);
        }
      }
    }
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
        translate([-thickness, i * len_z_front])
          square([thickness + 0.1, len_z_front]);
      }
    }

    // Tabs into right panel
    for (i = [0:2 * num_notches_z_front]) {
      if (i % 2 == 0) {
        translate([iw - 0.1, i * len_z_front])
          square([thickness + 0.1, len_z_front]);
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
        jack_y_back = case_internal_height + jack_ty * sin(panel_tilt) + jack_tz * cos(panel_tilt);
        for (jx = [jack1_pcb_x, jack2_pcb_x]) {
          translate([svg_shift_x + pcb_offset_x + jx, jack_y_back])
            circle(d=jack_hole_dia, $fn=48);
        }
      }

      // Cutout for USB-C port (J5)
      if (add_usb_cutout) {
        usb_ty = svg_shift_y + pcb_offset_y + usb_pcb_y;
        usb_tz = -thickness + pcb_offset_z + usb_pcb_z;
        usb_y_back = case_internal_height + usb_ty * sin(panel_tilt) + usb_tz * cos(panel_tilt);
        translate([svg_shift_x + pcb_offset_x + usb_pcb_x, usb_y_back])
          rounded_slot(usb_slot_width, usb_slot_height, usb_slot_radius);
      }
    }

    // Tabs into left panel
    for (i = [0:2 * num_notches_z_back]) {
      if (i % 2 == 0) {
        translate([-thickness, i * len_z_back])
          square([thickness + 0.1, len_z_back]);
      }
    }

    // Tabs into right panel
    for (i = [0:2 * num_notches_z_back]) {
      if (i % 2 == 0) {
        translate([iw - 0.1, i * len_z_back])
          square([thickness + 0.1, len_z_back]);
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
    difference() {
      square([iw, case_depth]);
      if (add_eurorack_holes) {
        hole_y_front = eurorack_hole_edge_margin;
        hole_y_back = case_depth - eurorack_hole_edge_margin;
        slot_w = 7.2;
        slot_h = 3.0;
        slot_x_positions = (iw >= 40) ? [7.44, iw - 7.44] : [iw / 2];
        for (x = slot_x_positions) {
          translate([x, hole_y_front]) hull() {
            translate([-(slot_w - slot_h)/2, 0]) circle(d=slot_h, $fn=30);
            translate([(slot_w - slot_h)/2, 0]) circle(d=slot_h, $fn=30);
          }
          translate([x, hole_y_back]) hull() {
            translate([-(slot_w - slot_h)/2, 0]) circle(d=slot_h, $fn=30);
            translate([(slot_w - slot_h)/2, 0]) circle(d=slot_h, $fn=30);
          }
        }
      }
    }
  }
}

module top_engraving() {
  if (use_svg_for_top_panel) {
    translate([svg_shift_x, svg_shift_y]) {
      import(svg_engraving);
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
    translate([thickness, thickness, case_internal_height + thickness + pcb_float_z]) {
      rotate([panel_tilt, 0, 0]) {
        translate([svg_shift_x + pcb_offset_x, svg_shift_y + pcb_offset_y, -thickness + pcb_offset_z]) {
          color("#2a6f4e")
            import(pcb_stl_file, convexity=10);
        }
      }
    }
  }

  // Bottom frame (now solid)
  color("#8b5a2b", assembly_opacity)
    linear_extrude(thickness) bottom_panel();

  // Top front strip
  color("#8b5a2b", assembly_opacity)
    translate([thickness, thickness, case_internal_height + thickness])
      rotate([panel_tilt, 0, 0])
      translate([0, 0, -2 * thickness])
      linear_extrude(thickness) top_strip_front();

  // Top back strip
  color("#8b5a2b", assembly_opacity)
    translate([thickness, thickness, case_internal_height + thickness])
      rotate([panel_tilt, 0, 0])
      translate([0, case_depth - shift_back - frame_rim_width, -2 * thickness])
      linear_extrude(thickness) top_strip_back();

  // Top cover visualized floating above
  if (include_top_panel) {
    translate([thickness, thickness, case_internal_height + thickness + top_float_distance]) {
      rotate([panel_tilt, 0, 0]) {
        translate([0, 0, -thickness]) {
          color("#faedcd", assembly_opacity)
            linear_extrude(thickness) top_panel();
            
          if (show_engraving) {
            color("#5c4033", assembly_opacity)
              translate([0, 0, thickness + 0.01])
                linear_extrude(0.1) top_engraving();
          }
        }
      }
    }
  }

  // Left
  color("#a0522d", assembly_opacity)
    translate([0, 0, thickness])
      rotate([90, 0, 90])
        linear_extrude(thickness) left_panel();

  // Right
  color("#cd853f", assembly_opacity)
    translate([ow - thickness, 0, thickness])
      rotate([90, 0, 90])
        linear_extrude(thickness) right_panel();

  // Front
  color("#deb887", assembly_opacity)
    translate([thickness, thickness, thickness])
      rotate([90, 0, 0])
        linear_extrude(thickness) front_panel();

  // Back
  color("#d2b48c", assembly_opacity)
    translate([thickness, od, thickness])
      rotate([90, 0, 0])
        linear_extrude(thickness) back_panel();
}

module layout() {
  spacing = 5;
  tab = thickness;

  // Row 1: Bottom panel and Top cover
  translate([tab, tab]) bottom_panel();
  
  translate([tab + ow + spacing, 0]) {
    if (include_top_panel) {
      top_panel();
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
}

// ---------------------------------------------------------
// Main Render Logic
// ---------------------------------------------------------
if (part_to_show == "assembly") {
  assembly();
} else if (part_to_show == "layout") {
  layout();
} else if (part_to_show == "top_dummy" || part_to_show == "top") {
  top_panel();
  if (show_engraving) {
    color("black") top_engraving();
  }
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
