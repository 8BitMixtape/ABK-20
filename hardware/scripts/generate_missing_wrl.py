#!/usr/bin/env python3
"""
Generate high-fidelity VRML 2.0 (.wrl) 3D models for:
1. PJ301M-12.wrl (WQP-PJ301M-12 / Thonkiconn 3.5mm vertical mono jack)
2. SW_SPST_Omron_B3FS-100xP.wrl (Omron B3FS 6x6mm SMD Tactile Switch)
"""
import math
import os

def format_vec(x, y, z):
    # KiCad VRML format: 1 unit = 2.54 mm
    return f"{x/2.54:.4f} {y/2.54:.4f} {z/2.54:.4f}"

def add_quad(faces, a, b, c, d):
    faces.append([a, b, c, d])
    faces.append([a, d, c, b])

def add_tri(faces, a, b, c):
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

# -------------------------------------------------------------
# 1. PJ301M-12 Thonkiconn Vertical 3.5mm Mono Jack
# -------------------------------------------------------------
def generate_pj301m(out_path):
    shapes = []

    # Main Plastic Housing (Translucent Blue / Eurorack Style)
    # Body: 8.5 x 6.0 mm, height 10.5 mm
    body_pts = []
    body_faces = []
    add_box(body_pts, body_faces, -4.25, 4.25, -3.0, 3.0, 0.0, 10.5)

    shapes.append({
        "name": "Body_BluePlastic",
        "pts": body_pts,
        "faces": body_faces,
        "diffuse": "0.15 0.45 0.85",
        "specular": "0.4 0.6 0.9",
        "shininess": "0.6",
        "transparency": "0.2"
    })

    # Threaded Bushing (Nickel / Silver Metal Collar) on top
    # Extends from Z = 10.5 to Z = 14.5 mm
    metal_pts = []
    metal_faces = []
    r_out = 3.0 # dia 6.0 mm
    r_in = 1.75 # dia 3.5 mm inner bore
    z_b = 10.5
    z_t = 14.5
    n_cyl = 32

    cyl_b = len(metal_pts)
    for i in range(n_cyl):
        ang = 2 * math.pi * i / n_cyl
        metal_pts.append((r_out * math.cos(ang), r_out * math.sin(ang), z_b))
    for i in range(n_cyl):
        ang = 2 * math.pi * i / n_cyl
        metal_pts.append((r_out * math.cos(ang), r_out * math.sin(ang), z_t))
    for i in range(n_cyl):
        ang = 2 * math.pi * i / n_cyl
        metal_pts.append((r_in * math.cos(ang), r_in * math.sin(ang), z_t))
    for i in range(n_cyl):
        ang = 2 * math.pi * i / n_cyl
        metal_pts.append((r_in * math.cos(ang), r_in * math.sin(ang), 2.0)) # inside bore
    metal_pts.append((0.0, 0.0, 2.0))
    c_bot = len(metal_pts) - 1

    for i in range(n_cyl):
        nxt = (i + 1) % n_cyl
        add_quad(metal_faces, cyl_b + i, cyl_b + nxt, cyl_b + n_cyl + nxt, cyl_b + n_cyl + i)
        add_quad(metal_faces, cyl_b + n_cyl + i, cyl_b + n_cyl + nxt, cyl_b + 2*n_cyl + nxt, cyl_b + 2*n_cyl + i)
        add_quad(metal_faces, cyl_b + 2*n_cyl + i, cyl_b + 2*n_cyl + nxt, cyl_b + 3*n_cyl + nxt, cyl_b + 3*n_cyl + i)
        add_tri(metal_faces, c_bot, cyl_b + 3*n_cyl + i, cyl_b + 3*n_cyl + nxt)

    # 3 DIP Pins (Ground, Tip, Switched Tip)
    for px, py in [(-2.5, 0.0), (0.0, -2.0), (2.5, 2.0)]:
        add_box(metal_pts, metal_faces, px - 0.25, px + 0.25, py - 0.35, py + 0.35, -3.2, 0.0)

    shapes.append({
        "name": "Metal_Bushing_Pins",
        "pts": metal_pts,
        "faces": metal_faces,
        "diffuse": "0.85 0.85 0.88",
        "specular": "0.95 0.95 0.95",
        "shininess": "0.85",
        "transparency": "0.0"
    })

    write_vrml(out_path, "PJ301M-12 3.5mm Mono Vertical Jack", shapes)

# -------------------------------------------------------------
# 2. Omron B3FS-100xP 6x6mm SMD Tactile Switch
# -------------------------------------------------------------
def generate_b3fs(out_path):
    shapes = []

    # Black Plastic Base: 6.0 x 6.0 mm, height 2.5 mm
    base_pts = []
    base_faces = []
    add_box(base_pts, base_faces, -3.0, 3.0, -3.0, 3.0, 0.0, 2.4)

    shapes.append({
        "name": "Base_BlackPlastic",
        "pts": base_pts,
        "faces": base_faces,
        "diffuse": "0.15 0.15 0.16",
        "specular": "0.25 0.25 0.26",
        "shininess": "0.3",
        "transparency": "0.0"
    })

    # Stainless Steel Top Plate: 5.8 x 5.8 mm, height from 2.4 to 2.6 mm
    metal_pts = []
    metal_faces = []
    add_box(metal_pts, metal_faces, -2.9, 2.9, -2.9, 2.9, 2.4, 2.6)

    # 4 SMD Gullwing Leads (extending in Y)
    # Pitch ~ 4.5 mm in X, span ~ 8.0 mm in Y
    for px in [-2.25, 2.25]:
        for py_dir in [-1, 1]:
            y1 = py_dir * 3.0
            y2 = py_dir * 4.0
            add_box(metal_pts, metal_faces, px - 0.4, px + 0.4, min(y1, y2), max(y1, y2), 0.0, 0.3)

    shapes.append({
        "name": "Metal_Cover_Leads",
        "pts": metal_pts,
        "faces": metal_faces,
        "diffuse": "0.88 0.88 0.90",
        "specular": "0.95 0.95 0.95",
        "shininess": "0.9",
        "transparency": "0.0"
    })

    # Center Actuator Plunger Button: dia 3.5 mm, height from 2.6 to 3.1 mm
    btn_pts = []
    btn_faces = []
    r_btn = 1.75
    z_btn_b = 2.6
    z_btn_t = 3.1
    n_seg = 24
    b_base = len(btn_pts)
    for i in range(n_seg):
        ang = 2 * math.pi * i / n_seg
        btn_pts.append((r_btn * math.cos(ang), r_btn * math.sin(ang), z_btn_b))
    for i in range(n_seg):
        ang = 2 * math.pi * i / n_seg
        btn_pts.append((r_btn * math.cos(ang), r_btn * math.sin(ang), z_btn_t))
    btn_pts.append((0.0, 0.0, z_btn_t))
    c_top = len(btn_pts) - 1

    for i in range(n_seg):
        nxt = (i + 1) % n_seg
        add_quad(btn_faces, b_base + i, b_base + nxt, b_base + n_seg + nxt, b_base + n_seg + i)
        add_tri(btn_faces, c_top, b_base + n_seg + i, b_base + n_seg + nxt)

    shapes.append({
        "name": "Button_Actuator_Ivory",
        "pts": btn_pts,
        "faces": btn_faces,
        "diffuse": "0.92 0.88 0.78",
        "specular": "0.5 0.5 0.4",
        "shininess": "0.4",
        "transparency": "0.0"
    })

    write_vrml(out_path, "Omron B3FS-100xP 6x6mm SMD Tactile Switch", shapes)

def write_vrml(out_path, desc, shapes):
    with open(out_path, "w") as f:
        f.write("#VRML V2.0 utf8\n")
        f.write(f"# {desc}\n\n")
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
    generate_pj301m("hardware/3d_models/PJ301M-12.wrl")
    print("Generated PJ301M-12.wrl successfully!")
    generate_b3fs("hardware/3d_models/SW_SPST_Omron_B3FS-100xP.wrl")
    print("Generated SW_SPST_Omron_B3FS-100xP.wrl successfully!")

