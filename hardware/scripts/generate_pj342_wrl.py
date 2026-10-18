#!/usr/bin/env python3
"""
Generate a high-fidelity VRML (.wrl) model for the PJ-342 3.5mm SMD audio jack.
Matches footprint: 3.5mm_jack_SMT_dusjagrnoSilk.kicad_mod
and physical component: PJ-342 6-pin SMD stereo phone jack with gold wrap-around shield.
"""

import math

def format_coords(points):
    # KiCad VRML standard format: 1 unit = 2.54 mm (0.1 inch), mirrored across Y
    return ", ".join(f"{p[0]/2.54:.4f} {-p[1]/2.54:.4f} {p[2]/2.54:.4f}" for p in points)

def format_indices(indices):
    chunks = []
    for face in indices:
        # Reverse winding order because Y was reflected
        chunks.append(",".join(str(i) for i in reversed(face)) + ",-1")
    return ",".join(chunks)

def make_box(x0, x1, y0, y1, z0, z1):
    pts = [
        (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), # bottom 0,1,2,3
        (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1), # top 4,5,6,7
    ]
    faces = [
        [0, 3, 2, 1], # bottom
        [4, 5, 6, 7], # top
        [0, 1, 5, 4], # -y side
        [2, 3, 7, 6], # +y side
        [0, 4, 7, 3], # -x face
        [1, 2, 6, 5], # +x face
    ]
    return pts, faces

def make_cylinder_x(x0, x1, y_c, z_c, radius, n_segs=24, r_inner=0.0):
    """Cylinder oriented along X-axis."""
    pts = []
    faces = []
    
    # Outer ring vertices
    for i in range(n_segs):
        ang = 2 * math.pi * i / n_segs
        y = y_c + radius * math.cos(ang)
        z = z_c + radius * math.sin(ang)
        pts.append((x0, y, z)) # ring 0: 0..n-1
    for i in range(n_segs):
        ang = 2 * math.pi * i / n_segs
        y = y_c + radius * math.cos(ang)
        z = z_c + radius * math.sin(ang)
        pts.append((x1, y, z)) # ring 1: n..2n-1

    # Side faces
    for i in range(n_segs):
        next_i = (i + 1) % n_segs
        p0 = i
        p1 = next_i
        p2 = n_segs + next_i
        p3 = n_segs + i
        faces.append([p0, p1, p2, p3])

    if r_inner > 0:
        # Inner ring vertices (hollow tube)
        base_inner = len(pts)
        for i in range(n_segs):
            ang = 2 * math.pi * i / n_segs
            y = y_c + r_inner * math.cos(ang)
            z = z_c + r_inner * math.sin(ang)
            pts.append((x0, y, z)) # base_inner + 0..n-1
        for i in range(n_segs):
            ang = 2 * math.pi * i / n_segs
            y = y_c + r_inner * math.cos(ang)
            z = z_c + r_inner * math.sin(ang)
            pts.append((x1, y, z)) # base_inner + n..2n-1

        # Inner side faces (normals inward)
        for i in range(n_segs):
            next_i = (i + 1) % n_segs
            p0 = base_inner + i
            p1 = base_inner + n_segs + i
            p2 = base_inner + n_segs + next_i
            p3 = base_inner + next_i
            faces.append([p0, p1, p2, p3])

        # End caps (annular)
        # x0 cap
        for i in range(n_segs):
            next_i = (i + 1) % n_segs
            faces.append([i, base_inner + i, base_inner + next_i, next_i])
        # x1 cap
        for i in range(n_segs):
            next_i = (i + 1) % n_segs
            faces.append([n_segs + i, n_segs + next_i, base_inner + n_segs + next_i, base_inner + n_segs + i])
    else:
        # Solid caps
        c0 = len(pts)
        pts.append((x0, y_c, z_c))
        c1 = len(pts)
        pts.append((x1, y_c, z_c))
        for i in range(n_segs):
            next_i = (i + 1) % n_segs
            faces.append([c0, (i + 1) % n_segs, i])
            faces.append([c1, n_segs + i, n_segs + next_i])

    return pts, faces

def make_gullwing_lead(x_c, y_body, y_pad, z_body=1.0, width=0.8, thickness=0.25):
    """Create SMD gullwing lead with notched swallowtail foot."""
    # Lead steps:
    # 1. Comes out horizontally from y_body to y_bend1
    # 2. Slopes down to z=thickness
    # 3. Runs horizontally on PCB to y_pad_outer
    w2 = width / 2.0
    x_min = x_c - w2
    x_max = x_c + w2
    
    sign_y = 1.0 if y_pad > 0 else -1.0
    y_bend1 = y_body + sign_y * 0.35
    y_bend2 = y_body + sign_y * 0.75
    y_tip = y_pad + sign_y * 0.85
    y_notch = y_tip - sign_y * 0.35
    
    # Vertices
    # Top profile points at (y, z)
    # Bottom profile points at (y, z - thickness)
    prof = [
        (y_body, z_body),
        (y_bend1, z_body),
        (y_bend2, thickness),
        (y_notch, thickness),
        (y_tip, thickness),
    ]
    
    # Build 3D mesh for the foot
    # Simple box extrusion with notched tip
    # Segment 1: from y_body to y_bend1 (horizontal stub)
    pts1, faces1 = make_box(x_min, x_max, min(y_body, y_bend1), max(y_body, y_bend1), z_body - thickness, z_body)
    
    # Segment 2: down slope
    pts2, faces2 = make_box(x_min, x_max, min(y_bend1, y_bend2), max(y_bend1, y_bend2), 0.0, z_body)
    
    # Segment 3: horizontal foot with swallowtail notch
    pts3 = [
        (x_min, y_bend2, 0.0), (x_max, y_bend2, 0.0), # 0, 1
        (x_max, y_tip, 0.0), (x_c + w2*0.3, y_tip, 0.0), # 2, 3
        (x_c, y_notch, 0.0), # 4 (notch center)
        (x_c - w2*0.3, y_tip, 0.0), (x_min, y_tip, 0.0), # 5, 6
        # top vertices (+ thickness)
        (x_min, y_bend2, thickness), (x_max, y_bend2, thickness), # 7, 8
        (x_max, y_tip, thickness), (x_c + w2*0.3, y_tip, thickness), # 9, 10
        (x_c, y_notch, thickness), # 11
        (x_c - w2*0.3, y_tip, thickness), (x_min, y_tip, thickness), # 12, 13
    ]
    if sign_y < 0:
        # reverse winding for negative side
        faces3 = [
            [0, 1, 2, 3, 4, 5, 6], # bottom
            [13, 12, 11, 10, 9, 8, 7], # top
            [0, 7, 8, 1], # inner end
            [1, 8, 9, 2], # side 1
            [2, 9, 10, 3], # tip 1
            [3, 10, 11, 4], # notch 1
            [4, 11, 12, 5], # notch 2
            [5, 12, 13, 6], # tip 2
            [6, 13, 7, 0], # side 2
        ]
    else:
        faces3 = [
            [6, 5, 4, 3, 2, 1, 0], # bottom
            [7, 8, 9, 10, 11, 12, 13], # top
            [1, 8, 7, 0], # inner end
            [2, 9, 8, 1], # side 1
            [3, 10, 9, 2], # tip 1
            [4, 11, 10, 3], # notch 1
            [5, 12, 11, 4], # notch 2
            [6, 13, 12, 5], # tip 2
            [0, 7, 13, 6], # side 2
        ]
        
    return [(pts1, faces1), (pts2, faces2), (pts3, faces3)]

def combine_meshes(mesh_list):
    all_pts = []
    all_faces = []
    offset = 0
    for pts, faces in mesh_list:
        all_pts.extend(pts)
        for f in faces:
            all_faces.append([i + offset for i in f])
        offset += len(pts)
    return all_pts, all_faces

def shape_vrml(pts, faces, material_use):
    s = "Shape {\n"
    s += "  geometry IndexedFaceSet {\n"
    s += "    creaseAngle 0.5\n"
    s += "    coord Coordinate { point [" + format_coords(pts) + "] }\n"
    s += "    coordIndex [" + format_indices(faces) + "]\n"
    s += "  }\n"
    s += f"  appearance Appearance {{ material {material_use} }}\n"
    s += "}\n"
    return s

def generate_pj342():
    # Materials
    header = """#VRML V2.0 utf8
#kicad StepUp wrl exported

Shape {
    appearance Appearance {material DEF PIN-GOLD Material {
        ambientIntensity 0.38
        diffuseColor 0.88 0.76 0.28
        specularColor 0.95 0.88 0.45
        emissiveColor 0.0 0.0 0.0
        shininess 0.75
        transparency 0.0
        }
    }
}
Shape {
    appearance Appearance {material DEF BODY-BLACK Material {
        ambientIntensity 0.15
        diffuseColor 0.14 0.14 0.14
        specularColor 0.22 0.22 0.22
        emissiveColor 0.0 0.0 0.0
        shininess 0.25
        transparency 0.0
        }
    }
}
Shape {
    appearance Appearance {material DEF SHIELD-GOLD Material {
        ambientIntensity 0.42
        diffuseColor 0.90 0.78 0.32
        specularColor 0.98 0.90 0.50
        emissiveColor 0.0 0.0 0.0
        shininess 0.85
        transparency 0.0
        }
    }
}
"""

    black_parts = []
    gold_parts = []

    # 1. Main Black Body
    # X from -6.0 to 6.0, Y from -3.0 to 3.0, Z from 0.0 to 5.0
    pts_main, f_main = make_box(-6.0, 6.0, -3.0, 3.0, 0.0, 5.0)
    black_parts.append((pts_main, f_main))

    # Rear flange step (X from 6.0 to 6.4, Y from -2.8 to 2.8, Z from 0.0 to 4.8)
    pts_rear, f_rear = make_box(6.0, 6.4, -2.8, 2.8, 0.0, 4.8)
    black_parts.append((pts_rear, f_rear))

    # Front barrel collar flange (X from -6.3 to -6.0, Y from -2.9 to 2.9, Z from 0.0 to 5.0)
    pts_col, f_col = make_box(-6.3, -6.0, -2.9, 2.9, 0.0, 5.0)
    black_parts.append((pts_col, f_col))

    # Front cylindrical barrel (X from -8.0 to -6.3, Y center 0, Z center 2.5, R=2.5, R_inner=1.75)
    pts_cyl, f_cyl = make_cylinder_x(-8.0, -6.3, 0.0, 2.5, radius=2.5, n_segs=32, r_inner=1.75)
    black_parts.append((pts_cyl, f_cyl))

    # Internal bore depth inside body (hollow opening from -6.3 to 4.0, R=1.75)
    # Inner gold tip & ring contact leaves visible through aperture
    pts_contact, f_contact = make_box(-3.0, 2.0, -0.8, -0.6, 2.2, 2.8)
    gold_parts.append((pts_contact, f_contact))
    pts_contact2, f_contact2 = make_box(0.0, 4.0, 0.6, 0.8, 2.2, 2.8)
    gold_parts.append((pts_contact2, f_contact2))

    # Bottom alignment nubs (X = -1.5 and +2.5, Y = 0, D = 1.3, height 0.4 below Z=0)
    # Keeping them shallow so they don't clip through boards without holes
    pts_nub1, f_nub1 = make_box(-2.1, -0.9, -0.6, 0.6, -0.4, 0.0)
    black_parts.append((pts_nub1, f_nub1))
    pts_nub2, f_nub2 = make_box(1.9, 3.1, -0.6, 0.6, -0.4, 0.0)
    black_parts.append((pts_nub2, f_nub2))

    # Top recess detail on black body (recess in the middle)
    pts_rec, f_rec = make_box(-0.5, 3.5, -2.0, 2.0, 4.9, 5.02)
    # Just a subtle visual step

    # 2. Gold Wrap-Around Front Shield (look at user photo!)
    # Wraps over top (Z: 4.95 to 5.08), sides (Y: -3.08 to -2.95 and 2.95 to 3.08)
    # From X = -5.8 to X = -3.2
    # Top plate
    pts_sh_top, f_sh_top = make_box(-5.8, -3.2, -3.06, 3.06, 4.96, 5.08)
    gold_parts.append((pts_sh_top, f_sh_top))
    # +Y side plate (with rectangular latch cutout)
    # Upper strip
    pts_sh_yp1, f_sh_yp1 = make_box(-5.8, -3.2, 2.96, 3.08, 3.8, 4.96)
    gold_parts.append((pts_sh_yp1, f_sh_yp1))
    # Lower strip
    pts_sh_yp2, f_sh_yp2 = make_box(-5.8, -3.2, 2.96, 3.08, 0.2, 1.8)
    gold_parts.append((pts_sh_yp2, f_sh_yp2))
    # Front pillar
    pts_sh_yp3, f_sh_yp3 = make_box(-5.8, -4.8, 2.96, 3.08, 1.8, 3.8)
    gold_parts.append((pts_sh_yp3, f_sh_yp3))
    # Rear pillar
    pts_sh_yp4, f_sh_yp4 = make_box(-3.8, -3.2, 2.96, 3.08, 1.8, 3.8)
    gold_parts.append((pts_sh_yp4, f_sh_yp4))

    # -Y side plate (with rectangular latch cutout)
    pts_sh_yn1, f_sh_yn1 = make_box(-5.8, -3.2, -3.08, -2.96, 3.8, 4.96)
    gold_parts.append((pts_sh_yn1, f_sh_yn1))
    pts_sh_yn2, f_sh_yn2 = make_box(-5.8, -3.2, -3.08, -2.96, 0.2, 1.8)
    gold_parts.append((pts_sh_yn2, f_sh_yn2))
    pts_sh_yn3, f_sh_yn3 = make_box(-5.8, -4.8, -3.08, -2.96, 1.8, 3.8)
    gold_parts.append((pts_sh_yn3, f_sh_yn3))
    pts_sh_yn4, f_sh_yn4 = make_box(-3.8, -3.2, -3.08, -2.96, 1.8, 3.8)
    gold_parts.append((pts_sh_yn4, f_sh_yn4))

    # Front wrapping lip (flanks of the barrel)
    pts_sh_fl1, f_sh_fl1 = make_box(-6.05, -5.8, 2.0, 3.06, 1.0, 4.5)
    gold_parts.append((pts_sh_fl1, f_sh_fl1))
    pts_sh_fl2, f_sh_fl2 = make_box(-6.05, -5.8, -3.06, -2.0, 1.0, 4.5)
    gold_parts.append((pts_sh_fl2, f_sh_fl2))

    # 3. Exactly 6 SMD Gullwing Leads matching footprint pads:
    # Pad 1: at (-3.913, +3.624)
    # Pad 2: at (+3.371, -3.624)
    # Pad 3: at (-0.508, +3.624)
    # Pad 4: at (-3.913, -3.5605)
    # Pad 5: at (+5.842, -3.6315)
    # Pad 6: at (+5.207, +3.624)
    pad_list = [
        (-3.913, +3.624, 0.95),  # Pad 1 (front left, part of shield)
        (+3.371, -3.624, 0.90),  # Pad 2 (middle right)
        (-0.508, +3.624, 0.90),  # Pad 3 (middle left)
        (-3.913, -3.5605, 0.95), # Pad 4 (front right, part of shield)
        (+5.842, -3.6315, 0.90), # Pad 5 (rear right)
        (+5.207, +3.624, 0.90),  # Pad 6 (rear left)
    ]

    for x_c, y_pad, w in pad_list:
        sign = 1.0 if y_pad > 0 else -1.0
        lead_meshes = make_gullwing_lead(x_c, sign * 3.0, y_pad, z_body=1.0, width=w, thickness=0.22)
        for pts, faces in lead_meshes:
            gold_parts.append((pts, faces))

    # Combine into VRML shapes
    b_pts, b_faces = combine_meshes(black_parts)
    g_pts, g_faces = combine_meshes(gold_parts)

    out = header
    out += shape_vrml(b_pts, b_faces, "USE BODY-BLACK")
    out += shape_vrml(g_pts, g_faces, "USE SHIELD-GOLD")
    return out

if __name__ == '__main__':
    wrl_content = generate_pj342()
    out_file = 'hardware/3d_models/AudioJack_3.5mm_PJ-342.wrl'
    with open(out_file, 'w') as f:
        f.write(wrl_content)
    print(f"Generated {out_file} ({len(wrl_content)} bytes)")
