#!/usr/bin/env python3
"""
diy_net_continuity_checker.py
=============================
Rigorous physical connectivity verification for DIY etched boards without plated-through holes (non-PTH).

Physical constraints:
1. SMD pads connect only to their own layer.
2. Vias 1..5 connect F.Cu and B.Cu (dedicated wire bridges).
3. THT parts on F.Cu connect to the circuit ONLY via B.Cu copper.
4. THT parts on B.Cu connect to the circuit ONLY via F.Cu copper (except J5 shield tabs accessible both sides).
5. All pads on a net must be connected together in the resulting physical graph!
"""

import pcbnew
import sys
from collections import defaultdict, deque

def check_diy_continuity(pcb_path):
    board = pcbnew.LoadBoard(pcb_path)
    print("=" * 80)
    print(f"DIY NON-PTH FULL BOARD CONTINUITY AUDIT: {pcb_path}")
    print("=" * 80)

    # 1. Identify all nets with at least 2 connected pads
    net_map = board.GetNetsByName()
    
    # We will test all active nets
    broken_nets = {}
    ok_nets = []

    for netname, net_obj in sorted(net_map.items(), key=lambda x: str(x[0])):
        net_code = net_obj.GetNetCode()
        if net_code == 0:  # unconnected
            continue

        # Collect all functional pins for this net
        functional_pins = []
        for fp in board.GetFootprints():
            ref = fp.GetReference()
            fp_layer = board.GetLayerName(fp.GetLayer())
            for p in fp.Pads():
                if p.GetNetCode() == net_code:
                    ptype = 'THT' if p.GetAttribute() == pcbnew.PAD_ATTRIB_PTH else 'SMD'
                    # Determine where this pad is physically soldered in DIY
                    if ptype == 'SMD':
                        solder_layers = [fp_layer]
                    else:
                        # THT
                        if ref == 'J5' and p.GetNumber() == 'S1':
                            solder_layers = ['F.Cu', 'B.Cu']
                        elif fp_layer == 'F.Cu':
                            solder_layers = ['B.Cu']  # soldered on bottom
                        else:
                            solder_layers = ['F.Cu']  # soldered on top
                    
                    functional_pins.append({
                        'ref': ref,
                        'pin': p.GetNumber(),
                        'name': f"{ref}.{p.GetNumber()}",
                        'pad_obj': p,
                        'fp_layer': fp_layer,
                        'solder_layers': solder_layers,
                        'ptype': ptype
                    })

        if len(functional_pins) < 2:
            continue

        # Now build the physical copper graph for this net across F.Cu and B.Cu
        # Nodes:
        # - functional_pins (identified by pin['name'])
        # - tracks on F.Cu and B.Cu
        # - zone polygons on F.Cu and B.Cu
        # - dedicated vias (connecting F.Cu and B.Cu)

        # Collect tracks
        tracks = []
        vias = []
        for t in board.GetTracks():
            if t.GetNetCode() == net_code:
                if t.GetClass() == 'PCB_VIA':
                    vias.append(t)
                else:
                    tracks.append(t)

        # Collect zone polygons
        zone_polys = []
        for z in board.Zones():
            if z.GetNetCode() == net_code:
                for layer_id in [pcbnew.F_Cu, pcbnew.B_Cu]:
                    if z.IsOnLayer(layer_id):
                        filled = z.GetFilledPolysList(layer_id)
                        for i in range(filled.OutlineCount()):
                            poly = filled.Outline(i)
                            s_zp = pcbnew.SHAPE_POLY_SET()
                            s_zp.AddOutline(poly)
                            zone_polys.append({
                                'id': f"Zone_{board.GetLayerName(layer_id)}_{len(zone_polys)}",
                                'layer_id': layer_id,
                                'layer_name': board.GetLayerName(layer_id),
                                'poly': poly,
                                'poly_set': s_zp,
                                'bbox': poly.BBox()
                            })

        adj = defaultdict(set)

        # Connect functional pins to copper
        for p in functional_pins:
            for s_layer in p['solder_layers']:
                l_id = pcbnew.F_Cu if s_layer == 'F.Cu' else pcbnew.B_Cu
                p_poly = p['pad_obj'].GetEffectivePolygon(l_id)
                s_p = pcbnew.SHAPE_POLY_SET()
                s_p.AddOutline(p_poly.Outline(0))
                p_bbox = p_poly.BBox()

                # check tracks on this layer
                for idx, t in enumerate(tracks):
                    if t.GetLayer() == l_id:
                        if p_bbox.Contains(t.GetStart()) or p_bbox.Contains(t.GetEnd()):
                            if p_poly.PointInside(t.GetStart()) or p_poly.PointInside(t.GetEnd()):
                                adj[p['name']].add(f"Track_{idx}")
                                adj[f"Track_{idx}"].add(p['name'])

                # check zone polys on this layer
                for zp in zone_polys:
                    if zp['layer_id'] == l_id:
                        if zp['bbox'].Intersects(p_bbox):
                            if zp['poly_set'].Collide(s_p):
                                adj[p['name']].add(zp['id'])
                                adj[zp['id']].add(p['name'])

        # Connect tracks on same layer
        for i in range(len(tracks)):
            t1 = tracks[i]
            l1 = t1.GetLayer()
            for j in range(i + 1, len(tracks)):
                t2 = tracks[j]
                if l1 == t2.GetLayer():
                    tol = (t1.GetWidth() + t2.GetWidth()) / 2
                    d1 = (t1.GetStart() - t2.GetStart()).EuclideanNorm()
                    d2 = (t1.GetStart() - t2.GetEnd()).EuclideanNorm()
                    d3 = (t1.GetEnd() - t2.GetStart()).EuclideanNorm()
                    d4 = (t1.GetEnd() - t2.GetEnd()).EuclideanNorm()
                    if min(d1, d2, d3, d4) <= tol:
                        adj[f"Track_{i}"].add(f"Track_{j}")
                        adj[f"Track_{j}"].add(f"Track_{i}")

        # Connect tracks to zones on same layer
        for idx, t in enumerate(tracks):
            l_id = t.GetLayer()
            for zp in zone_polys:
                if zp['layer_id'] == l_id:
                    for frac in [0.0, 0.25, 0.5, 0.75, 1.0]:
                        dx = int((t.GetEnd().x - t.GetStart().x) * frac)
                        dy = int((t.GetEnd().y - t.GetStart().y) * frac)
                        pt = pcbnew.VECTOR2I(t.GetStart().x + dx, t.GetStart().y + dy)
                        if zp['bbox'].Contains(pt) and zp['poly'].PointInside(pt):
                            adj[f"Track_{idx}"].add(zp['id'])
                            adj[zp['id']].add(f"Track_{idx}")
                            break

        # Dedicated Vias: connect F.Cu copper and B.Cu copper touching the via
        for v_idx, v in enumerate(vias):
            via_node = f"Via_{v_idx}"
            v_pt = v.GetPosition()
            v_rad = v.GetWidth(pcbnew.F_Cu) / 2

            # Tracks touching via on either layer
            for t_idx, t in enumerate(tracks):
                d1 = (t.GetStart() - v_pt).EuclideanNorm()
                d2 = (t.GetEnd() - v_pt).EuclideanNorm()
                if min(d1, d2) <= (v_rad + t.GetWidth() / 2):
                    adj[via_node].add(f"Track_{t_idx}")
                    adj[f"Track_{t_idx}"].add(via_node)

            # Zones touching via on either layer
            for zp in zone_polys:
                if zp['bbox'].Contains(v_pt) and zp['poly'].PointInside(v_pt):
                    adj[via_node].add(zp['id'])
                    adj[zp['id']].add(via_node)

        # Now test connectivity among functional_pins
        pin_names = [p['name'] for p in functional_pins]
        visited_nodes = set()
        pin_islands = []

        for p_name in pin_names:
            if p_name not in visited_nodes:
                island = []
                queue = deque([p_name])
                visited_nodes.add(p_name)
                while queue:
                    curr = queue.popleft()
                    if curr in pin_names:
                        island.append(curr)
                    for nbr in adj[curr]:
                        if nbr not in visited_nodes:
                            visited_nodes.add(nbr)
                            queue.append(nbr)
                pin_islands.append(island)

        if len(pin_islands) > 1:
            broken_nets[netname] = pin_islands
        else:
            ok_nets.append(netname)

    print(f"\n[+] CONTINUITY AUDIT RESULTS:")
    print(f"    Total Nets Checked: {len(ok_nets) + len(broken_nets)}")
    print(f"    Fully Connected Nets (DIY OK): {len(ok_nets)}")
    print(f"    DISCONNECTED NETS ON DIY BOARD: {len(broken_nets)}")

    if broken_nets:
        print("\n" + "!" * 80)
        print("CRITICAL DEFECTS FOUND: The following nets will FAIL on DIY etched boards:")
        print("!" * 80)
        for net, islands in sorted(broken_nets.items(), key=lambda x: str(x[0])):
            print(f"\n[-] NET: '{net}' has {len(islands)} isolated islands:")
            for i, isl in enumerate(islands):
                print(f"    Island {i+1} ({len(isl)} pins): {', '.join(sorted(isl))}")
    else:
        print("\nALL NETS ARE 100% CONTINUOUS UNDER DIY NON-PTH CONSTRAINTS!")

if __name__ == '__main__':
    pcb = sys.argv[1] if len(sys.argv) > 1 else 'hardware/ABK-20.kicad_pcb'
    check_diy_continuity(pcb)
