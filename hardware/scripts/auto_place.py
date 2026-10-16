#!/usr/bin/env python3
import sys
import pcbnew

def mm(val):
    return pcbnew.FromMM(val)

def place_board(pcb_path):
    board = pcbnew.LoadBoard(pcb_path)
    
    # Coordinates origin: X: 100..190, Y: 100..190, Center = (145, 145)
    CX = 145.0
    CY = 145.0
    
    # 1. NeoPixel Matrix 5 cols x 4 rows
    # Col spacing: 8.0mm, Row spacing: 8.0mm
    # Cols: -16, -8, 0, +8, +16 -> X in [129, 137, 145, 153, 161]
    # Rows: -12, -4, +4, +12 relative to matrix center Y=126.0 -> Y in [114, 122, 130, 138]
    matrix_center_y = 126.0
    col_pitch = 8.0
    row_pitch = 8.0
    
    # Matrix mapping (5 cols, 4 rows):
    # Row 0: NEO1 .. NEO5
    # Row 1: NEO6 .. NEO10
    # Row 2: NEO11 .. NEO15
    # Row 3: NEO16 .. NEO20
    for r in range(4):
        for c in range(5):
            idx = r * 5 + c + 1
            ref = f"NEO{idx}"
            fp = board.FindFootprintByReference(ref)
            if fp:
                x = CX + (c - 2) * col_pitch
                y = matrix_center_y + (r - 1.5) * row_pitch
                fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
                fp.SetOrientationDegrees(0)
                print(f"Placed {ref} at ({x:.1f}, {y:.1f})")

    # 2. Power LED (D-POW1) - top-right next to matrix
    fp = board.FindFootprintByReference("D-POW1")
    if fp:
        x, y = 169.0, 116.0
        fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
        fp.SetOrientationDegrees(0)
        print(f"Placed D-POW1 at ({x:.1f}, {y:.1f})")

    # 3. Bottom Controls Row (Y = 168.0)
    # Left: Toggle switch SW3
    fp = board.FindFootprintByReference("SW3")
    if fp:
        x, y = 122.0, 168.0
        fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
        fp.SetOrientationDegrees(0)
        print(f"Placed SW3 at ({x:.1f}, {y:.1f})")

    # Center: Knob POT2-CV1
    fp = board.FindFootprintByReference("POT2-CV1")
    if fp:
        x, y = 145.0, 168.0
        fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
        fp.SetOrientationDegrees(180)
        print(f"Placed POT2-CV1 at ({x:.1f}, {y:.1f})")

    # Right: Audio Jack Jack1
    fp = board.FindFootprintByReference("Jack1")
    if fp:
        x, y = 168.0, 168.0
        fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
        fp.SetOrientationDegrees(270)
        print(f"Placed Jack1 at ({x:.1f}, {y:.1f})")

    # Jack2 (Sync / secondary jack) - placed next to Jack1 or top
    fp = board.FindFootprintByReference("Jack2")
    if fp:
        x, y = 168.0, 150.0
        fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
        fp.SetOrientationDegrees(270)
        print(f"Placed Jack2 at ({x:.1f}, {y:.1f})")

    # 4. Top Edge Connectors
    # USB-C J5 centered on top edge facing out
    fp = board.FindFootprintByReference("J5")
    if fp:
        x, y = 145.0, 101.5
        fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
        fp.SetOrientationDegrees(180)
        print(f"Placed J5 at ({x:.1f}, {y:.1f})")

    # Power switch SW1
    fp = board.FindFootprintByReference("SW1")
    if fp:
        x, y = 122.0, 104.0
        fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
        fp.SetOrientationDegrees(0)
        print(f"Placed SW1 at ({x:.1f}, {y:.1f})")

    # 5. Core ICs placed neatly on Bottom Layer (B.Cu)
    # ATtiny85 U1
    fp = board.FindFootprintByReference("U1")
    if fp:
        x, y = 145.0, 145.0
        fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
        fp.SetLayer(pcbnew.B_Cu)
        print(f"Placed U1 on B.Cu at ({x:.1f}, {y:.1f})")

    # PAM8002 U2
    fp = board.FindFootprintByReference("U2")
    if fp:
        x, y = 168.0, 135.0
        fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
        fp.SetLayer(pcbnew.B_Cu)
        print(f"Placed U2 on B.Cu at ({x:.1f}, {y:.1f})")

    # 7805 U3
    fp = board.FindFootprintByReference("U3")
    if fp:
        x, y = 125.0, 115.0
        fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
        fp.SetLayer(pcbnew.B_Cu)
        print(f"Placed U3 on B.Cu at ({x:.1f}, {y:.1f})")

    board.Save(pcb_path)
    print("Board saved successfully.")

if __name__ == '__main__':
    pcb_path = sys.argv[1] if len(sys.argv) > 1 else 'hardware/ABK-20.kicad_pcb'
    place_board(pcb_path)
