import bpy
import bmesh
import math

def build_ptl_quads(travel=20, output_obj="/tmp/ptl20_v2.obj", lever_h=10.0):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    if travel == 20:
        casing_len = 35.0
        slit_len_half = 10.0 # 20mm travel (footprint lines -10 to +10)
        hole_x = 15.5
        pin_x = 15.0
        tab_xs = [-12.0, -4.0, 4.0, 12.0]
    else: # 30mm
        casing_len = 45.0
        slit_len_half = 18.5 # 37mm travel opening (footprint lines -18.5 to +18.5)
        hole_x = 20.5
        pin_x = 20.0
        tab_xs = [-16.0, -5.5, 5.5, 16.0]
        
    casing_w = 9.0 # Footprint & datasheet width
    casing_h = 7.0 # Height from PCB
    half_l = casing_len / 2.0
    half_w = casing_w / 2.0
    slit_w_half = 0.8 # 1.6mm wide slot
    slit_depth = 1.0 # slit depth below top face
    floor_z = casing_h - slit_depth # Z = 6.0mm
    
    # --- 1. METAL CASING (SilverMetal) ---
    mesh_casing = bpy.data.meshes.new("Metal_Casing_Mesh")
    obj_casing = bpy.data.objects.new("Metal_Casing", mesh_casing)
    bpy.context.collection.objects.link(obj_casing)
    
    bm = bmesh.new()
    
    # Helper to add a quad
    def add_quad(p1, p2, p3, p4):
        v1 = bm.verts.new(p1)
        v2 = bm.verts.new(p2)
        v3 = bm.verts.new(p3)
        v4 = bm.verts.new(p4)
        return bm.faces.new([v1, v2, v3, v4])

    # 4 Outer side walls:
    # South wall: Y = -half_w
    add_quad((-half_l, -half_w, 0), ( half_l, -half_w, 0), ( half_l, -half_w, casing_h), (-half_l, -half_w, casing_h))
    # East wall: X = +half_l
    add_quad(( half_l, -half_w, 0), ( half_l,  half_w, 0), ( half_l,  half_w, casing_h), ( half_l, -half_w, casing_h))
    # North wall: Y = +half_w
    add_quad(( half_l,  half_w, 0), (-half_l,  half_w, 0), (-half_l,  half_w, casing_h), ( half_l,  half_w, casing_h))
    # West wall: X = -half_l
    add_quad((-half_l,  half_w, 0), (-half_l, -half_w, 0), (-half_l, -half_w, casing_h), (-half_l,  half_w, casing_h))
    
    # Top face 4 clean rectangles surrounding the slit:
    # 1. South strip: X in [-half_l, half_l], Y in [-half_w, -slit_w_half]
    add_quad((-half_l, -half_w, casing_h), (half_l, -half_w, casing_h), (half_l, -slit_w_half, casing_h), (-half_l, -slit_w_half, casing_h))
    # 2. North strip: X in [-half_l, half_l], Y in [slit_w_half, half_w]
    add_quad((-half_l, slit_w_half, casing_h), (half_l, slit_w_half, casing_h), (half_l, half_w, casing_h), (-half_l, half_w, casing_h))
    # 3. West cap: X in [-half_l, -slit_len_half], Y in [-slit_w_half, slit_w_half]
    add_quad((-half_l, -slit_w_half, casing_h), (-slit_len_half, -slit_w_half, casing_h), (-slit_len_half, slit_w_half, casing_h), (-half_l, slit_w_half, casing_h))
    # 4. East cap: X in [slit_len_half, half_l], Y in [-slit_w_half, slit_w_half]
    add_quad((slit_len_half, -slit_w_half, casing_h), (half_l, -slit_w_half, casing_h), (half_l, slit_w_half, casing_h), (slit_len_half, slit_w_half, casing_h))

    # Inner vertical walls of the slit (dropping down to floor_z):
    # South slit wall: at Y = -slit_w_half, from -slit_len_half to +slit_len_half
    add_quad((-slit_len_half, -slit_w_half, casing_h), ( slit_len_half, -slit_w_half, casing_h), ( slit_len_half, -slit_w_half, floor_z), (-slit_len_half, -slit_w_half, floor_z))
    # North slit wall: at Y = +slit_w_half, from +slit_len_half to -slit_len_half
    add_quad(( slit_len_half,  slit_w_half, casing_h), (-slit_len_half,  slit_w_half, casing_h), (-slit_len_half,  slit_w_half, floor_z), ( slit_len_half,  slit_w_half, floor_z))
    # West slit wall: at X = -slit_len_half, from +slit_w_half to -slit_w_half
    add_quad((-slit_len_half,  slit_w_half, casing_h), (-slit_len_half, -slit_w_half, casing_h), (-slit_len_half, -slit_w_half, floor_z), (-slit_len_half,  slit_w_half, floor_z))
    # East slit wall: at X = +slit_len_half, from -slit_w_half to +slit_w_half
    add_quad(( slit_len_half, -slit_w_half, casing_h), ( slit_len_half,  slit_w_half, casing_h), ( slit_len_half,  slit_w_half, floor_z), ( slit_len_half, -slit_w_half, floor_z))
    
    bm.to_mesh(mesh_casing)
    bm.free()
    
    # Side Crimp Tabs along bottom (Y = ±(half_w + 0.15))
    crimp_tabs = []
    tab_thickness = 0.35
    tab_w = 2.0
    tab_h = 1.8
    for sign_y in [-1, 1]:
        y_pos = sign_y * (half_w + tab_thickness/2.0)
        for tx in tab_xs:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=(tx, y_pos, tab_h/2.0))
            tab = bpy.context.active_object
            tab.scale = (tab_w, tab_thickness, tab_h)
            crimp_tabs.append(tab)
            
    # Solder Pins extending down to Z = -3.5mm
    pins = []
    pin_locs = [
        (-pin_x, -3.75), (-pin_x, -1.25), (-pin_x, 1.25), (-pin_x, 3.75),
        (pin_x, -1.25), (pin_x, 3.75) # +2.5mm shift
    ]
    for px, py in pin_locs:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(px, py, -1.75))
        pin = bpy.context.active_object
        pin.scale = (0.5, 0.9, 3.5)
        pins.append(pin)
        
    # Join metal casing parts
    bpy.ops.object.select_all(action='DESELECT')
    for obj in [obj_casing] + crimp_tabs + pins:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = obj_casing
    bpy.ops.object.join()
    metal_case = bpy.context.active_object
    metal_case.name = "Metal_Casing"
    
    mat_metal = bpy.data.materials.new(name="SilverMetal")
    mat_metal.diffuse_color = (0.82, 0.82, 0.85, 1.0)
    metal_case.data.materials.append(mat_metal)
    
    # --- 2. DARK INTERIOR (Slit Floor & Screw Hole Insets) ---
    # Slit floor:
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(0, 0, floor_z - 0.05)
    )
    slit_floor = bpy.context.active_object
    slit_floor.scale = (slit_len_half * 2.0, slit_w_half * 2.0, 0.1)
    
    # M2 Mounting Holes (circular dark insets at X = ±hole_x, Y = 0, Z = casing_h)
    hole_objs = []
    for hx in [-hole_x, hole_x]:
        bpy.ops.mesh.primitive_cylinder_add(
            radius=1.0, depth=0.3,
            location=(hx, 0, casing_h - 0.1)
        )
        cyl = bpy.context.active_object
        hole_objs.append(cyl)
        
    # Join dark interior parts
    bpy.ops.object.select_all(action='DESELECT')
    for obj in [slit_floor] + hole_objs:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = slit_floor
    bpy.ops.object.join()
    dark_parts = bpy.context.active_object
    dark_parts.name = "Dark_Interior"
    
    mat_dark = bpy.data.materials.new(name="DarkInterior")
    mat_dark.diffuse_color = (0.05, 0.05, 0.05, 1.0)
    dark_parts.data.materials.append(mat_dark)
    
    # --- 3. BLACK SLIDER LEVER ---
    lever_top = casing_h + lever_h # 17.0mm
    stem_bottom = floor_z # starts right at the slit floor
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(0, 0, (stem_bottom + lever_top) / 2.0)
    )
    lever_stem = bpy.context.active_object
    lever_stem.scale = (3.0, 1.3, lever_top - stem_bottom)
    
    # Internal carriage block inside casing (beneath the slit)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 5.0))
    carriage = bpy.context.active_object
    carriage.scale = (6.0, 3.5, 1.6)
    
    bpy.ops.object.select_all(action='DESELECT')
    lever_stem.select_set(True)
    carriage.select_set(True)
    bpy.context.view_layer.objects.active = lever_stem
    bpy.ops.object.join()
    black_lever = bpy.context.active_object
    black_lever.name = "Black_Lever"
    
    mat_black = bpy.data.materials.new(name="BlackPlastic")
    mat_black.diffuse_color = (0.12, 0.12, 0.12, 1.0)
    black_lever.data.materials.append(mat_black)
    
    # --- 4. ORANGE ILLUMINATED LED DIFFUSER ---
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(0, 0, lever_top - 1.0)
    )
    window = bpy.context.active_object
    window.scale = (2.2, 1.4, 2.0)
    window.name = "LED_Window"
    
    mat_orange = bpy.data.materials.new(name="OrangeLED")
    mat_orange.diffuse_color = (1.0, 0.50, 0.0, 0.9)
    window.data.materials.append(mat_orange)
    
    # Export OBJ
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.export_scene.obj(
        filepath=output_obj,
        use_selection=True,
        use_materials=True,
        axis_forward='Y',
        axis_up='Z'
    )
    print(f"Generated {output_obj}")

build_ptl_quads(20, "/tmp/ptl20_v2.obj", 10.0)
build_ptl_quads(30, "/tmp/ptl30_v2.obj", 10.0)
