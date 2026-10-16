#!/usr/bin/env python3
import pcbnew

def mm(v): return pcbnew.FromMM(v)

board = pcbnew.LoadBoard('hardware/ABK-20.kicad_pcb')
CX = 145.0
CY = 145.0

# 1. Clean up B.Cu passives: keep the matrix area (Y in [108, 144]) completely clear on both sides!
# Place all power passives (U3, C7, C8, D1, D2, D3, R17, R18) along the top edge or below matrix
# Let's place U3 at X=115, Y=106 (top-left corner of B.Cu, completely away from matrix)
fp_u3 = board.FindFootprintByReference("U3")
if fp_u3:
    fp_u3.SetPosition(pcbnew.VECTOR2I(mm(113.0), mm(106.0)))

pwr_passives = ["C7", "C8", "D1", "D2", "D3", "R17", "R18"]
for i, ref in enumerate(pwr_passives):
    fp = board.FindFootprintByReference(ref)
    if fp:
        px = 108.0 + (i % 4) * 5.5
        py = 113.0 + (i // 4) * 4.0
        fp.SetPosition(pcbnew.VECTOR2I(mm(px), mm(py)))

# Place ATtiny U1 at X=145.0, Y=152.0 (below matrix, above controls)
fp_u1 = board.FindFootprintByReference("U1")
if fp_u1:
    fp_u1.SetPosition(pcbnew.VECTOR2I(mm(145.0), mm(152.0)))

# MCU passives around U1 (Y in [157, 163])
mcu_passives = ["C1", "C2", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10", "R11", "R12", "R13", "R16", "R99"]
for i, ref in enumerate(mcu_passives):
    fp = board.FindFootprintByReference(ref)
    if fp:
        px = 112.0 + (i % 6) * 5.2
        py = 158.0 + (i // 6) * 3.8
        fp.SetPosition(pcbnew.VECTOR2I(mm(px), mm(py)))

# Place U2 (audio amp) at X=176.0, Y=152.0
fp_u2 = board.FindFootprintByReference("U2")
if fp_u2:
    fp_u2.SetPosition(pcbnew.VECTOR2I(mm(176.0), mm(152.0)))

aud_passives = ["C3", "C4", "C5", "C6", "R14", "R15"]
for i, ref in enumerate(aud_passives):
    fp = board.FindFootprintByReference(ref)
    if fp:
        px = 172.0 + (i % 2) * 5.5
        py = 158.0 + (i // 2) * 3.8
        fp.SetPosition(pcbnew.VECTOR2I(mm(px), mm(py)))

# Move RV1 (unused slide pot) and aux headers out of sight (e.g. at bottom margin Y=188 on B.Cu)
aux_comps = ["RV1", "POT3-Vol1", "Speaker1", "SW2", "SW4", "J1", "J2", "J3", "J4", "J6", "BT1", "BT2"]
for i, ref in enumerate(aux_comps):
    fp = board.FindFootprintByReference(ref)
    if fp:
        px = 110.0 + (i % 6) * 12.0
        py = 188.0 + (i // 6) * 6.0
        fp.SetPosition(pcbnew.VECTOR2I(mm(px), mm(py)))

# 2. Update silkscreen text positions
to_remove = []
for d in board.GetDrawings():
    if isinstance(d, pcbnew.PCB_TEXT) and d.GetLayer() == pcbnew.F_SilkS:
        to_remove.append(d)
for d in to_remove:
    board.Remove(d)

def add_text(text, x, y, size=1.5, layer=pcbnew.F_SilkS):
    t = pcbnew.PCB_TEXT(board)
    t.SetText(text)
    t.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
    t.SetTextSize(pcbnew.VECTOR2I(mm(size), mm(size)))
    t.SetTextThickness(mm(size * 0.15))
    t.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_CENTER)
    t.SetLayer(layer)
    board.Add(t)

add_text("8Bit Mixtape - ABK-20", 145.0, 105.0, size=1.6)
add_text("MODE", 122.0, 175.5, size=1.2)
add_text("PITCH / CV", 145.0, 175.5, size=1.2)
add_text("AUDIO / SYNC", 168.0, 175.5, size=1.2)
add_text("PWR", 169.0, 112.5, size=1.0)

board.Save('hardware/ABK-20.kicad_pcb')
print("Panel finalized successfully!")
