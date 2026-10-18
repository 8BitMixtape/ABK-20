#!/usr/bin/env python3
"""
Generate high-fidelity VRML 2.0 (.wrl) 3D model for 6x6mm SMD Tactile Switch (Metal Dome).
Matches user photo media_1792332393492_d557429d.png:
- Black plastic base (6.0 x 6.0 mm) with 4 bottom corner standoff feet and side lead cutouts
- Polished stainless steel top plate with rounded corners
- 4 melted black plastic round rivet studs on the 4 corners
- Cylindrical round black plastic button plunger in center (dia 3.3mm, H = 5.0mm)
- 4 gull-wing SMD solder leads on the sides (span ~9.0mm)
"""
import math
import os

def format_vec(x, y, z):
    # KiCad VRML standard format: 1 unit = 2.54 mm
    return f"{x/2.54:.4f} {y/2.54:.4f} {z/2.54:.4f}"

def add_quad(faces, a, b, c, d):
    # Double-sided quad
    faces.append([a, b, c, d])
    faces.append([a, d, c, b])

def add_tri(faces, a, b, c):
    # Double-sided triangle
    faces.append([a, b, c])
    faces.append([a, c, b])

def add_box(pts, faces, xmin, xmax, ymin, ymax, zmin, zmax):
    base = len(pts)
    pts.extend([
        (xmin, ymin, zmin), (xmax, ymin, zmin), (xmax, ymax, zmin), (xmin, ymax, zmin),
        (xmin, ymin, zmax), (xmax, ymin, zmax), (xmax, ymax, zmax), (xmin, ymax, zmax),
    ])
    add_quad(faces, base+0, base+3, base+2, base+1)
    add_quad(faces, base+4, base+5, base+6, base+7)
    add_quad(faces, base+0, base+4, base+7, base+3)
    add_quad(faces, base+1, base+2, base+6, base+5)
    add_quad(faces, base+0, base+1, base+5, base+4)
    add_quad(faces, base+3, base+7, base+6, base+2)
    return base

def add_dome(pts, faces, cx, cy, cz, r, h, n_lat=6, n_lon=12):
    """Add a smooth half-dome / rivet stud."""
    dome_base = len(pts)
    for i in range(n_lat + 1):
        theta = (math.pi / 2) * (i / n_lat)
        z = cz + h * math.sin(theta)
        cur_r = r * math.cos(theta)
        for j in range(n_lon):
            phi = 2 * math.pi * j / n_lon
            x = cx + cur_r * math.cos(phi)
            y = cy + cur_r * math.sin(phi)
            pts.append((x, y, z))

    for i in range(n_lat):
        for j in range(n_lon):
            nxt_j = (j + 1) % n_lon
            p1 = dome_base + i * n_lon + j
            p2 = dome_base + i * n_lon + nxt_j
            p3 = dome_base + (i + 1) * n_lon + nxt_j
            p4 = dome_base + (i + 1) * n_lon + j
            add_quad(faces, p1, p2, p3, p4)

def generate_tactile_switch_wrl(out_path):
    shapes = []

    # -------------------------------------------------------------
    # 1. Black Plastic Housing Base
    # -------------------------------------------------------------
    base_pts = []
    base_faces = []

    # Main body block: 6.0 x 6.0 mm, Z from 0.4 to 3.5 mm
    add_box(base_pts, base_faces, -3.0, 3.0, -3.0, 3.0, 0.4, 3.5)

    # 4 Corner Standoff Feet: Z from 0.0 to 0.4 mm
    # In the photo, the body rests on 4 square corner pads
    foot_w = 0.9
    for fx in [-3.0, 3.0 - foot_w]:
        for fy in [-3.0, 3.0 - foot_w]:
            add_box(base_pts, base_faces, fx, fx + foot_w, fy, fy + foot_w, 0.0, 0.4)

    # 4 Corner Heat-Stake Rivet Studs on the top plate (Z = 3.65 to 4.05 mm)
    # At (±2.2, ±2.2) mm
    rivet_r = 0.45
    rivet_h = 0.35
    for rx in [-2.15, 2.15]:
        for ry in [-2.15, 2.15]:
            add_dome(base_pts, base_faces, rx, ry, 3.65, rivet_r, rivet_h, n_lat=5, n_lon=12)

    # Round Button Plunger (Center Actuator)
    # In the photo: cylindrical black button, dia 3.3mm, flat top with slight bevel
    # Extends up to Z = 5.0 mm (height 5.0 mm above PCB)
    r_btn = 1.65 # dia 3.3 mm
    r_top = 1.50 # slight top bevel
    z_btn_b = 3.4
    z_btn_m = 4.85
    z_btn_t = 5.0
    n_cyl = 32

    cyl_b = len(base_pts)
    # Bottom ring
    for i in range(n_cyl):
        ang = 2 * math.pi * i / n_cyl
        base_pts.append((r_btn * math.cos(ang), r_btn * math.sin(ang), z_btn_b))
    # Mid-top ring (where bevel starts)
    for i in range(n_cyl):
        ang = 2 * math.pi * i / n_cyl
        base_pts.append((r_btn * math.cos(ang), r_btn * math.sin(ang), z_btn_m))
    # Top rim
    for i in range(n_cyl):
        ang = 2 * math.pi * i / n_cyl
        base_pts.append((r_top * math.cos(ang), r_top * math.sin(ang), z_btn_t))
    # Top center point
    base_pts.append((0.0, 0.0, z_btn_t))
    c_top = len(base_pts) - 1

    for i in range(n_cyl):
        nxt = (i + 1) % n_cyl
        # Main cylinder wall
        add_quad(base_faces, cyl_b + i, cyl_b + nxt, cyl_b + n_cyl + nxt, cyl_b + n_cyl + i)
        # Beveled upper rim
        add_quad(base_faces, cyl_b + n_cyl + i, cyl_b + n_cyl + nxt, cyl_b + 2*n_cyl + nxt, cyl_b + 2*n_cyl + i)
        # Flat top disc
        add_tri(base_faces, c_top, cyl_b + 2*n_cyl + i, cyl_b + 2*n_cyl + nxt)

    shapes.append({
        "name": "Base_Plunger_BlackPlastic",
        "pts": base_pts,
        "faces": base_faces,
        "diffuse": "0.14 0.14 0.15",
        "specular": "0.32 0.32 0.34",
        "shininess": "0.35",
        "transparency": "0.0"
    })

    # -------------------------------------------------------------
    # 2. Polished Stainless Steel Top Plate
    # -------------------------------------------------------------
    # In the photo: square metal plate 5.9 x 5.9 mm with rounded corners and center round hole
    metal_pts = []
    metal_faces = []

    z_pl_b = 3.50
    z_pl_t = 3.65 # thickness 0.15 mm
    r_hole = 1.85 # inner hole dia 3.7 mm

    # We model the plate as an outer beveled square with an inner circular cutout
    # Outer 16-point rounded square contour:
    plate_outer = []
    w_half = 2.95
    c_rad = 0.55 # corner rounding radius
    corners = [
        (w_half - c_rad, w_half - c_rad, 0),      # Top-right
        (-w_half + c_rad, w_half - c_rad, 90),   # Top-left
        (-w_half + c_rad, -w_half + c_rad, 180), # Bottom-left
        (w_half - c_rad, -w_half + c_rad, 270)   # Bottom-right
    ]
    n_corner = 4
    for cx_c, cy_c, start_deg in corners:
        for k in range(n_corner):
            ang = math.radians(start_deg + (90 * k / n_corner))
            plate_outer.append((cx_c + c_rad * math.cos(ang), cy_c + c_rad * math.sin(ang)))

    n_out = len(plate_outer) # 16 points

    # Inner circular hole points (n_out points)
    plate_inner = []
    for i in range(n_out):
        ang = 2 * math.pi * i / n_out
        plate_inner.append((r_hole * math.cos(ang), r_hole * math.sin(ang)))

    p_base = len(metal_pts)
    # Outer bottom & top rings
    for px, py in plate_outer:
        metal_pts.append((px, py, z_pl_b))
    for px, py in plate_outer:
        metal_pts.append((px, py, z_pl_t))
    # Inner bottom & top rings
    for px, py in plate_inner:
        metal_pts.append((px, py, z_pl_b))
    for px, py in plate_inner:
        metal_pts.append((px, py, z_pl_t))

    # Top surface annulus quads (between outer and inner)
    for i in range(n_out):
        nxt = (i + 1) % n_out
        f_out1 = p_base + n_out + i
        f_out2 = p_base + n_out + nxt
        f_in2 = p_base + 3 * n_out + nxt
        f_in1 = p_base + 3 * n_out + i
        add_quad(metal_faces, f_out1, f_out2, f_in2, f_in1)

    # Outer vertical rim
    for i in range(n_out):
        nxt = (i + 1) % n_out
        add_quad(metal_faces, p_base + i, p_base + nxt, p_base + n_out + nxt, p_base + n_out + i)

    # Inner hole vertical rim
    for i in range(n_out):
        nxt = (i + 1) % n_out
        add_quad(metal_faces, p_base + 2*n_out + i, p_base + 2*n_out + nxt, p_base + 3*n_out + nxt, p_base + 3*n_out + i)

    # 4 Gull-wing SMD Solder Leads (Silver / Tin Plated Metal)
    # In the photo:
    # 2 on left side (Y = -3.0), 2 on right side (Y = +3.0)
    # Pins emerge at X = ±2.25 mm, curve downwards to PCB and extend flat to |Y| = 4.5 mm
    lead_w = 0.65 # lead width in X (0.65 mm)
    lead_t = 0.20 # thickness 0.2 mm

    for px in [-2.25, 2.25]:
        for y_sign in [-1, 1]:
            l_base = len(metal_pts)
            # Profile along Y:
            # Point 1: inside plastic wall at Y = 2.8, Z = 1.0
            # Point 2: exit wall at Y = 3.2, Z = 0.9
            # Point 3: slope down at Y = 3.6, Z = 0.15
            # Point 4: flat foot tip at Y = 4.5, Z = 0.0
            y1 = y_sign * 2.8
            y2 = y_sign * 3.3
            y3 = y_sign * 3.7
            y4 = y_sign * 4.6

            hx1, hx2 = px - lead_w/2, px + lead_w/2

            metal_pts.extend([
                # Segment 1 (Y1, Z 0.9 -> 1.1)
                (hx1, y1, 0.9), (hx2, y1, 0.9), (hx2, y1, 1.1), (hx1, y1, 1.1),
                # Segment 2 (Y2, Z 0.8 -> 1.0)
                (hx1, y2, 0.8), (hx2, y2, 0.8), (hx2, y2, 1.0), (hx1, y2, 1.0),
                # Segment 3 (Y3, Z 0.0 -> 0.2)
                (hx1, y3, 0.0), (hx2, y3, 0.0), (hx2, y3, 0.2), (hx1, y3, 0.2),
                # Segment 4 (Y4, Z 0.0 -> 0.2)
                (hx1, y4, 0.0), (hx2, y4, 0.0), (hx2, y4, 0.2), (hx1, y4, 0.2),
            ])

            for s in range(3):
                s1 = l_base + s * 4
                s2 = l_base + (s + 1) * 4
                for k in range(4):
                    nxt = (k + 1) % 4
                    add_quad(metal_faces, s1 + k, s1 + nxt, s2 + nxt, s2 + k)
            # Foot end cap
            add_quad(metal_faces, l_base + 12, l_base + 13, l_base + 14, l_base + 15)

    shapes.append({
        "name": "Metal_Plate_and_Leads",
        "pts": metal_pts,
        "faces": metal_faces,
        "diffuse": "0.92 0.92 0.94",
        "specular": "0.98 0.98 0.98",
        "shininess": "0.92",
        "transparency": "0.0"
    })

    # -------------------------------------------------------------
    # Write VRML File
    # -------------------------------------------------------------
    with open(out_path, "w") as f:
        f.write("#VRML V2.0 utf8\n")
        f.write("# 6x6mm SMD Tactile Switch (Metal Dome Cover, Black Plunger, 4 Gullwing SMD Leads)\n")
        f.write("# Height: 5.0mm, Base: 6.0x6.0mm\n\n")

        for s in shapes:
            f.write(f"# Shape: {s['name']}\n")
            f.write("Shape {\n")
            f.write("  geometry IndexedFaceSet {\n")
            f.write("    solid FALSE\n")
            f.write("    creaseAngle 0.5\n")
            f.write("    coord Coordinate {\n")
            f.write("      point [\n")
            pt_strs = [format_vec(x, y, z) for x, y, z in s['pts']]
            f.write("        " + ", ".join(pt_strs) + "\n")
            f.write("      ]\n")
            f.write("    }\n")
            f.write("    coordIndex [\n")
            face_strs = [" ".join(str(idx) for idx in face) + " -1" for face in s['faces']]
            f.write("      " + ", ".join(face_strs) + "\n")
            f.write("    ]\n")
            f.write("  }\n")
            f.write("  appearance Appearance {\n")
            f.write("    material Material {\n")
            f.write(f"      diffuseColor {s['diffuse']}\n")
            f.write(f"      specularColor {s['specular']}\n")
            f.write("      emissiveColor 0 0 0\n")
            f.write("      ambientIntensity 0.35\n")
            f.write(f"      shininess {s['shininess']}\n")
            f.write(f"      transparency {s['transparency']}\n")
            f.write("    }\n")
            f.write("  }\n")
            f.write("}\n\n")

if __name__ == "__main__":
    out1 = "hardware/3d_models/SW_PUSH_6mm_H13mm.wrl"
    generate_tactile_switch_wrl(out1)
    print(f"Generated {out1} successfully!")

    out2 = "hardware/3d_models/SW_SPST_Omron_B3FS-100xP.wrl"
    generate_tactile_switch_wrl(out2)
    print(f"Generated {out2} successfully!")

