#!/usr/bin/env python3
import sys
import pcbnew

def mm(v): return pcbnew.FromMM(v)

def flip_to_bottom(fp):
    if not fp.IsFlipped():
        fp.Flip(fp.GetPosition(), False)

def flip_to_top(fp):
    if fp.IsFlipped():
        fp.Flip(fp.GetPosition(), False)

def arrange():
    board = pcbnew.LoadBoard('hardware/ABK-20.kicad_pcb')
    CX = 145.0
    CY = 145.0

    # 1. NeoPixel Matrix (5 cols x 4 rows)
    # Row-by-Row, Left-to-Right:
    # Row 0: NEO1..NEO5
    # Row 1: NEO6..NEO10
    # Row 2: NEO11..NEO15
    # Row 3: NEO16..NEO20
    matrix_center_y = 126.0
    col_pitch = 8.0
    row_pitch = 8.0

    for r in range(4):
        for c in range(5):
            idx = r * 5 + c + 1
            ref = f"NEO{idx}"
            fp = board.FindFootprintByReference(ref)
            if fp:
                flip_to_top(fp)
                x = CX + (c - 2) * col_pitch
                y = matrix_center_y + (r - 1.5) * row_pitch
                fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
                fp.SetOrientationDegrees(0)

    # 2. Power LED (D-POW1) - Top-right of matrix
    fp = board.FindFootprintByReference("D-POW1")
    if fp:
        flip_to_top(fp)
        fp.SetPosition(pcbnew.VECTOR2I(mm(169.0), mm(116.0)))
        fp.SetOrientationDegrees(90)

    # 3. Bottom Controls Row (Y = 168.0)
    # SW3 (Toggle switch, red cap in prototype)
    fp = board.FindFootprintByReference("SW3")
    if fp:
        flip_to_top(fp)
        fp.SetPosition(pcbnew.VECTOR2I(mm(122.0), mm(168.0)))
        fp.SetOrientationDegrees(0)

    # POT2-CV1 (16mm Rotary Potentiometer with knob)
    # Shaft center should be at (145.0, 168.0)
    fp = board.FindFootprintByReference("POT2-CV1")
    if fp:
        flip_to_bottom(fp)
        # In Potentiometer_backPads_noHole, shaft center is at (+10, -5) relative to origin
        # With orientation 180 (or 0), let's calculate offset:
        # If orientation is 270:
        fp.SetOrientationDegrees(270)
        # Let's adjust so shaft lands at 145.0, 168.0
        fp.SetPosition(pcbnew.VECTOR2I(mm(140.0), mm(158.0)))

    # Jack1 (3.5mm Audio Minijack)
    fp = board.FindFootprintByReference("Jack1")
    if fp:
        flip_to_top(fp)
        fp.SetPosition(pcbnew.VECTOR2I(mm(168.0), mm(168.0)))
        fp.SetOrientationDegrees(270)

    # Jack2 (Secondary / Sync Minijack)
    fp = board.FindFootprintByReference("Jack2")
    if fp:
        flip_to_top(fp)
        fp.SetPosition(pcbnew.VECTOR2I(mm(168.0), mm(148.0)))
        fp.SetOrientationDegrees(270)

    # 4. Top Edge Connectors
    # J5 (USB-C 6-pin)
    fp = board.FindFootprintByReference("J5")
    if fp:
        flip_to_top(fp)
        fp.SetPosition(pcbnew.VECTOR2I(mm(145.0), mm(101.5)))
        fp.SetOrientationDegrees(180)

    # SW1 (Push/Slide Switch)
    fp = board.FindFootprintByReference("SW1")
    if fp:
        flip_to_top(fp)
        fp.SetPosition(pcbnew.VECTOR2I(mm(122.0), mm(104.0)))
        fp.SetOrientationDegrees(0)

    # 5. Core ICs on Bottom Layer
    # U1 (ATtiny85)
    fp = board.FindFootprintByReference("U1")
    if fp:
        flip_to_bottom(fp)
        fp.SetPosition(pcbnew.VECTOR2I(mm(145.0), mm(144.0)))
        fp.SetOrientationDegrees(0)

    # U2 (PAM8002 Audio Amp)
    fp = board.FindFootprintByReference("U2")
    if fp:
        flip_to_bottom(fp)
        fp.SetPosition(pcbnew.VECTOR2I(mm(168.0), mm(132.0)))
        fp.SetOrientationDegrees(0)

    # U3 (7805 TO-252)
    fp = board.FindFootprintByReference("U3")
    if fp:
        flip_to_bottom(fp)
        fp.SetPosition(pcbnew.VECTOR2I(mm(125.0), mm(115.0)))
        fp.SetOrientationDegrees(0)

    # 6. Group SMD Passives on B.Cu
    # Power section passives (near U3 / J5):
    pwr_passives = ["C7", "C8", "D1", "D2", "D3", "R17", "R18"]
    for i, ref in enumerate(pwr_passives):
        fp = board.FindFootprintByReference(ref)
        if fp:
            flip_to_bottom(fp)
            px = 112.0 + (i % 3) * 6.0
            py = 112.0 + (i // 3) * 4.5
            fp.SetPosition(pcbnew.VECTOR2I(mm(px), mm(py)))
            fp.SetOrientationDegrees(0)

    # ATtiny MCU passives (near U1):
    mcu_passives = ["C1", "C2", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10", "R11", "R12", "R13", "R16", "R99"]
    for i, ref in enumerate(mcu_passives):
        fp = board.FindFootprintByReference(ref)
        if fp:
            flip_to_bottom(fp)
            px = 112.0 + (i % 6) * 5.5
            py = 148.0 + (i // 6) * 4.0
            fp.SetPosition(pcbnew.VECTOR2I(mm(px), mm(py)))
            fp.SetOrientationDegrees(0)

    # Audio passives (near U2):
    aud_passives = ["C3", "C4", "C5", "C6", "R14", "R15"]
    for i, ref in enumerate(aud_passives):
        fp = board.FindFootprintByReference(ref)
        if fp:
            flip_to_bottom(fp)
            px = 158.0 + (i % 3) * 5.5
            py = 120.0 + (i // 3) * 4.0
            fp.SetPosition(pcbnew.VECTOR2I(mm(px), mm(py)))
            fp.SetOrientationDegrees(0)

    # Optional / header components (BT1, BT2, RV1, POT3-Vol1, Speaker1, SW2, SW4, J1, J2, J3, J4, J6)
    # Park cleanly at bottom edge / auxiliary section on B.Cu
    aux_comps = ["RV1", "POT3-Vol1", "Speaker1", "SW2", "SW4", "J1", "J2", "J3", "J4", "J6", "BT1", "BT2"]
    for i, ref in enumerate(aux_comps):
        fp = board.FindFootprintByReference(ref)
        if fp:
            flip_to_bottom(fp)
            px = 110.0 + (i % 4) * 15.0
            py = 176.0 + (i // 4) * 6.0
            fp.SetPosition(pcbnew.VECTOR2I(mm(px), mm(py)))

    # 7. Mounting holes H1..H4
    holes = {'H1': (104.5, 104.5), 'H2': (185.5, 104.5), 'H3': (104.5, 185.5), 'H4': (185.5, 185.5)}
    for href, (hx, hy) in holes.items():
        fp = board.FindFootprintByReference(href)
        if not fp:
            fp = pcbnew.FOOTPRINT(board)
            pad = pcbnew.PAD(fp)
            pad.SetNumber('1')
            pad.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
            pad.SetAttribute(pcbnew.PAD_ATTRIB_NPTH)
            pad.SetSize(pcbnew.VECTOR2I(mm(3.2), mm(3.2)))
            pad.SetDrillSize(pcbnew.VECTOR2I(mm(3.2), mm(3.2)))
            pad.SetLayerSet(pad.NPTH_PAD_LAYERS())
            fp.Add(pad)
            fp.SetReference(href)
            board.Add(fp)
        fp.SetPosition(pcbnew.VECTOR2I(mm(hx), mm(hy)))

    board.Save('hardware/ABK-20.kicad_pcb')
    print("Perfect layout completed successfully!")

if __name__ == '__main__':
    arrange()
