// Showcase of Classic Acoustic Speaker Grill Designs for ABK-20
$fn = 64;

module rounded_rect_center(w, d, r) {
  actual_r = min(r, min(w, d) / 2);
  if (actual_r > 0) {
    offset(r=actual_r)
      square([max(0.05, w - 2 * actual_r), max(0.05, d - 2 * actual_r)], center=true);
  } else {
    square([w, d], center=true);
  }
}

module SpeakerGrillCutouts2D(grill_style="slots", slot_w=1.4, slot_l=6.4, slot_pitch=3.4) {
  if (grill_style == "slots" || grill_style == "vert_slots") {
    // Style 1: Classic Synth 5 Vertical Rounded Slots
    for (i = [-2 : 1 : 2]) {
      translate([i * slot_pitch, 0])
        rounded_rect_center(slot_w, slot_l, slot_w / 2);
    }
  } else if (grill_style == "horiz_slots") {
    // Style 2: Classic Braun / Dieter Rams Horizontal Slits (3 tiered slots following stadium curve)
    rounded_rect_center(18.0, 1.4, 0.7);
    translate([0,  2.3]) rounded_rect_center(15.2, 1.4, 0.7);
    translate([0, -2.3]) rounded_rect_center(15.2, 1.4, 0.7);
  } else if (grill_style == "horiz_4slots") {
    // Style 2b: 4 Thin Horizontal Slits (Retro Hi-Fi cassette deck style)
    for (y = [-3.15, -1.05, 1.05, 3.15]) {
      w_slit = (abs(y) > 2.0) ? 14.5 : 18.0;
      translate([0, y])
        rounded_rect_center(w_slit, 1.2, 0.6);
    }
  } else if (grill_style == "soundwave") {
    // Style 3: Audio Waveform / Graphic EQ Slits (7 vertical bars with graduated heights)
    pit = 2.4;
    w_bar = 1.3;
    heights = [2.8, 4.4, 5.8, 6.8, 5.8, 4.4, 2.8];
    for (i = [0 : 6]) {
      translate([(i - 3) * pit, 0])
        rounded_rect_center(w_bar, heights[i], w_bar / 2);
    }
  } else if (grill_style == "braun_dots" || grill_style == "mesh") {
    // Style 4: Dieter Rams / Braun T3 Staggered Precision Dot Matrix (19 holes)
    d_hole = 1.4;
    // Row 0 (center): 7 holes
    for (x = [-7.5 : 2.5 : 7.5]) {
      translate([x, 0]) circle(d=d_hole);
    }
    // Rows +1 and -1 (staggered): 6 holes each
    for (x = [-6.25 : 2.5 : 6.25]) {
      translate([x,  2.2]) circle(d=d_hole);
      translate([x, -2.2]) circle(d=d_hole);
    }
  } else if (grill_style == "chevron" || grill_style == "slanted") {
    // Style 5: 80s Japanese Synth / Walkman 45-degree Angled Slits
    intersection() {
      rounded_rect_center(19.5, 7.2, 2.8);
      for (i = [-5 : 1 : 5]) {
        translate([i * 3.2, 0])
          rotate([0, 0, 45])
            rounded_rect_center(1.3, 16.0, 0.65);
      }
    }
  } else if (grill_style == "radial") {
    // Style 6: 1950s Transistor Radio Radial Dial Spoke Aperture
    intersection() {
      rounded_rect_center(19.5, 7.2, 2.8);
      union() {
        circle(d=2.6);
        for (a = [0 : 30 : 150]) {
          rotate([0, 0, a])
            rounded_rect_center(1.3, 18.0, 0.65);
        }
      }
    }
  } else if (grill_style == "aperture") {
    // Style 7: Open Framed Aperture for Custom Fabric or Metal Mesh
    rounded_rect_center(20.0, 7.5, 3.2);
  }
}

// Render sample faceplate tile with chimney underneath
module SampleTile(style_name, label_text) {
  difference() {
    // Front faceplate tile
    color("#ff69b4")
      linear_extrude(2.5)
        rounded_rect_center(26.0, 15.0, 2.0);

    // Grill cutout
    translate([0, 0, -1])
      linear_extrude(4.5)
        SpeakerGrillCutouts2D(style_name);
  }

  // Label below tile
  color("#222222")
    translate([0, -10.5, 0])
      linear_extrude(0.6)
        text(label_text, size=1.8, halign="center", valign="center", font="Liberation Sans:style=Bold");
}

// 8 Styles in a clean 2x4 grid layout
styles = [
  ["horiz_slots",  "HORIZ SLITS (BRAUN)"],
  ["vert_slots",   "VERT SLOTS (SYNTH)"],
  ["soundwave",    "SOUNDWAVE (EQ)"],
  ["braun_dots",   "DOT MATRIX (T3)"],
  ["horiz_4slots", "4 THIN SLITS (HIFI)"],
  ["chevron",      "CHEVRON (80s)"],
  ["radial",       "RADIAL (VINTAGE)"],
  ["aperture",     "OPEN APERTURE"]
];

for (i = [0 : 7]) {
  col = i % 4;
  row = floor(i / 4);
  translate([(col - 1.5) * 32.0, (0.5 - row) * 26.0, 0])
    SampleTile(styles[i][0], styles[i][1]);
}
