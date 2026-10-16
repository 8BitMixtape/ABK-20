#!/usr/bin/env python3
import re
import sys
import pcbnew

def parse_and_route(ses_path, pcb_path):
    board = pcbnew.LoadBoard(pcb_path)
    
    # Map net names to net info
    net_map = {}
    netinfo = board.GetNetInfo()
    for netcode in range(netinfo.GetNetCount()):
        ni = netinfo.GetNetItem(netcode)
        if ni:
            net_map[ni.GetNetname()] = ni

    with open(ses_path, 'r') as f:
        content = f.read()

    # Find network_out section
    net_section_match = re.search(r'\(network_out\s+(.*)\)\s*\)\s*\)\s*$', content, re.DOTALL)
    if not net_section_match:
        print("Could not find network_out section")
        return False

    network_out = net_section_match.group(1)
    
    # Split by net blocks: (net <netname> ...
    net_blocks = re.findall(r'\(net\s+([^\s\)]+)(.*?)(?=\(net|\Z)', network_out, re.DOTALL)
    print(f"Found {len(net_blocks)} net blocks in SES file.")

    layer_map = {
        'F.Cu': pcbnew.F_Cu,
        'B.Cu': pcbnew.B_Cu
    }

    # Clear existing tracks and vias first
    tracks_to_remove = [t for t in board.GetTracks()]
    for t in tracks_to_remove:
        board.Remove(t)
    print(f"Cleared {len(tracks_to_remove)} old tracks/vias.")

    total_segments = 0
    total_vias = 0

    for netname, body in net_blocks:
        net_item = net_map.get(netname)
        if not net_item:
            # try stripping quotes or slash
            net_item = net_map.get(f"/{netname}") or net_map.get(netname.strip('"'))
        net_code = net_item.GetNetCode() if net_item else 0

        # 1. Parse wires
        # (wire (path <layer> <width> <x1> <y1> <x2> <y2> ... ))
        wires = re.findall(r'\(wire\s+\(path\s+([^\s]+)\s+([^\s]+)\s+([^\)]+)\)\s*\)', body, re.DOTALL)
        for layer_str, width_str, pts_str in wires:
            layer = layer_map.get(layer_str, pcbnew.F_Cu)
            width = int(width_str) * 100  # resolution 10 um -> nm (KiCad internal unit)
            coords = [int(c) for c in pts_str.split()]
            pts = [(coords[i] * 100, -coords[i+1] * 100) for i in range(0, len(coords), 2)]
            
            for i in range(len(pts) - 1):
                track = pcbnew.PCB_TRACK(board)
                track.SetStart(pcbnew.VECTOR2I(pts[i][0], pts[i][1]))
                track.SetEnd(pcbnew.VECTOR2I(pts[i+1][0], pts[i+1][1]))
                track.SetWidth(width)
                track.SetLayer(layer)
                track.SetNetCode(net_code)
                board.Add(track)
                total_segments += 1

        # 2. Parse vias
        # (via "<padstack>" <x> <y>)
        vias = re.findall(r'\(via\s+\"[^\"]*\"\s+([^\s]+)\s+([^\s\)]+)\s*\)', body)
        for vx_str, vy_str in vias:
            vx = int(vx_str) * 100
            vy = -int(vy_str) * 100
            via = pcbnew.PCB_VIA(board)
            via.SetPosition(pcbnew.VECTOR2I(vx, vy))
            via.SetWidth(pcbnew.FromMM(0.6))
            via.SetDrill(pcbnew.FromMM(0.3))
            via.SetNetCode(net_code)
            board.Add(via)
            total_vias += 1

    print(f"Successfully imported {total_segments} track segments and {total_vias} vias!")
    board.Save(pcb_path)
    print("Board saved with all routed connections!")
    return True

if __name__ == '__main__':
    parse_and_route('/tmp/abk20.ses', 'hardware/ABK-20.kicad_pcb')
