#!/usr/bin/env bash
# Export KiCad PCB with full 3D models to centered STL for OpenSCAD enclosure design
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PCB_FILE="$REPO_ROOT/hardware/ABK-20.kicad_pcb"
OUTPUT_STL="$SCRIPT_DIR/ABK-20_pcb.stl"
TMP_WRL="/tmp/ABK-20_export.wrl"

echo "[1/2] Exporting VRML with centered user origin (114.71185x68.66405mm)..."
kicad-cli pcb export vrml --units mm --user-origin 114.71185x68.66405mm -o "$TMP_WRL" "$PCB_FILE"

echo "[2/2] Converting VRML to centered STL via Blender..."
blender -b --python-expr "
import bpy
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.x3d(filepath='$TMP_WRL', axis_forward='Y', axis_up='Z')
bpy.ops.export_mesh.stl(filepath='$OUTPUT_STL')
"

rm -f "$TMP_WRL"
echo "[+] Successfully exported: $OUTPUT_STL"

