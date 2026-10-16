#!/usr/bin/env python3
import pcbnew

def mm(v): return pcbnew.FromMM(v)

board = pcbnew.LoadBoard('hardware/ABK-20.kicad_pcb')

# 1. Add shaft hole for Potentiometer (NPTH dia 7.2mm)
href = "H-POT"
fp = board.FindFootprintByReference(href)
if not fp:
    fp = pcbnew.FOOTPRINT(board)
    pad = pcbnew.PAD(fp)
    pad.SetNumber("1")
    pad.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
    pad.SetAttribute(pcbnew.PAD_ATTRIB_NPTH)
    pad.SetSize(pcbnew.VECTOR2I(mm(7.2), mm(7.2)))
    pad.SetDrillSize(pcbnew.VECTOR2I(mm(7.2), mm(7.2)))
    h1 = board.FindFootprintByReference('H1')
    if h1 and len(h1.Pads()) > 0:
        pad.SetLayerSet(h1.Pads()[0].GetLayerSet())
    fp.Add(pad)
    fp.SetReference(href)
    board.Add(fp)
fp.SetPosition(pcbnew.VECTOR2I(mm(145.0), mm(168.0)))

# 2. Add Display Bezel on F.SilkS (around 5x4 matrix)
to_remove = []
for d in board.GetDrawings():
    if isinstance(d, pcbnew.PCB_SHAPE) and d.GetLayer() == pcbnew.F_SilkS:
        to_remove.append(d)
    elif isinstance(d, pcbnew.PCB_TEXT) and d.GetLayer() == pcbnew.F_SilkS:
        to_remove.append(d)
for d in to_remove:
    board.Remove(d)

def add_rect(x1, y1, x2, y2, layer, width):
    corners = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
    for i in range(4):
        s = pcbnew.PCB_SHAPE(board)
        s.SetShape(pcbnew.SHAPE_T_SEGMENT)
        s.SetStart(pcbnew.VECTOR2I(mm(corners[i][0]), mm(corners[i][1])))
        s.SetEnd(pcbnew.VECTOR2I(mm(corners[(i+1)%4][0]), mm(corners[(i+1)%4][1])))
        s.SetWidth(mm(width))
        s.SetLayer(layer)
        board.Add(s)

# Matrix Bezel frame
add_rect(123.5, 108.5, 166.5, 143.5, pcbnew.F_SilkS, 0.4)
add_rect(124.2, 109.2, 165.8, 142.8, pcbnew.F_SilkS, 0.15)

# 3. Add text labels on F.SilkS
def add_text(text, x, y, size=1.5, layer=pcbnew.F_SilkS):
    t = pcbnew.PCB_TEXT(board)
    t.SetText(text)
    t.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
    t.SetTextSize(pcbnew.VECTOR2I(mm(size), mm(size)))
    t.SetTextThickness(mm(size * 0.15))
    t.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_CENTER)
    t.SetLayer(layer)
    board.Add(t)

add_text("ABK-20", 145.0, 105.5, size=2.0)
add_text("8Bit Mixtape", 145.0, 148.0, size=1.5)
add_text("MODE", 122.0, 175.5, size=1.2)
add_text("PITCH / CV", 145.0, 175.5, size=1.2)
add_text("AUDIO / SYNC", 168.0, 175.5, size=1.2)
add_text("PWR", 169.0, 112.5, size=1.0)

board.Save('hardware/ABK-20.kicad_pcb')
print("Details added successfully!")
