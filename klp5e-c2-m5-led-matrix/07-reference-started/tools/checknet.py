#!/usr/bin/env python3
"""Read a KiCad netlist and report what is actually connected to what.

ERC is not proof. It reads clean while a pin sits a hair off grid and connects to
nothing, which is precisely the failure mode for the sixteen SEG/DIG nets in a
cell. The netlist is ground truth: it lists the pins each net really contains.

Usage:
    checknet.py net.net              # dump every net and its nodes
    checknet.py net.net --cell 1     # assert cell N's SEG->COL / DIG->ROW mapping
    checknet.py net.net --cascade 4  # assert the DOUT->DIN chain over N cells
"""
import re
import sys

# from PART-NOTES.md: TA08 is column anode
COL_PINS = [13, 3, 4, 10, 6, 11, 15, 16]   # <- MAX7219 SEG_A..SEG_DP
ROW_PINS = [9, 14, 8, 12, 1, 7, 2, 5]      # <- MAX7219 DIG_0..DIG_7
SEG_PINS = [14, 16, 20, 23, 21, 15, 17, 22]
DIG_PINS = [2, 11, 6, 7, 3, 10, 5, 8]


def parse(path):
    s = open(path, encoding="utf-8").read()
    nets = {}
    for m in re.finditer(r'\(net\s*\n\s*\(code "(\d+)"\)\s*\n\s*\(name "([^"]*)"\)', s):
        start = m.start()
        depth, started, end = 0, False, start
        for k in range(start, len(s)):
            if s[k] == '(':
                depth += 1
                started = True
            elif s[k] == ')':
                depth -= 1
                if started and depth == 0:
                    end = k + 1
                    break
        body = s[start:end]
        nodes = set()
        for n in re.finditer(r'\(ref "([^"]+)"\)\s*\n\s*\(pin "([^"]+)"\)', body):
            nodes.add((n.group(1), n.group(2)))
        nets[m.group(2)] = nodes
    return nets


def net_of(nets, ref, pin):
    for name, nodes in nets.items():
        if (ref, str(pin)) in nodes:
            return name, nodes
    return None, set()


def check_cell(nets, n):
    """Assert cell n's driver drives its own matrix, and only its own."""
    u, ds = f"U{n}", f"DS{n}"
    ok = True
    for i in range(8):
        for label, spin, mpin in (("SEG", SEG_PINS[i], COL_PINS[i]),
                                  ("DIG", DIG_PINS[i], ROW_PINS[i])):
            name, nodes = net_of(nets, u, spin)
            want = {(u, str(spin)), (ds, str(mpin))}
            if nodes != want:
                ok = False
                print(f"  FAIL {label}_{i} : {u}.{spin} net {name!r} = "
                      f"{sorted(nodes)}, expected {sorted(want)}")
    # both grounds
    gname, gnodes = net_of(nets, u, 4)
    if (u, "9") not in gnodes:
        ok = False
        print(f"  FAIL {u} pins 4 and 9 are not on the same net ({gname})")
    print(("  OK   " if ok else "  BAD  ") +
          f"cell {n}: 16 SEG/DIG nets exclusive to {u}<->{ds}, both grounds tied")
    return ok


def check_cascade(nets, count):
    ok = True
    for n in range(1, count):
        a, b = f"U{n}", f"U{n+1}"
        name, nodes = net_of(nets, a, 24)          # DOUT
        want = {(a, "24"), (b, "1")}               # -> next DIN
        if nodes != want:
            ok = False
            print(f"  FAIL {a}.DOUT net {name!r} = {sorted(nodes)}, expected {sorted(want)}")
    for pin, label in ((13, "CLK"), (12, "LOAD")):
        name, nodes = net_of(nets, "U1", pin)
        drivers = {r for r, p in nodes if r.startswith("U")}
        if len(drivers) != count:
            ok = False
            print(f"  FAIL {label} net {name!r} reaches {sorted(drivers)}, "
                  f"expected all {count} drivers")
    # the failure this project's net-naming rule exists to prevent
    dins = {net_of(nets, f"U{n}", 1)[0] for n in range(1, count + 1)}
    if len(dins) != count:
        ok = False
        print(f"  FAIL the {count} DIN nets collapsed into {len(dins)}: {sorted(dins)} "
              "-- the drivers are wired in parallel, not cascaded")
    print(("  OK   " if ok else "  BAD  ") +
          f"cascade: DOUT->DIN chain over {count} cells, CLK/LOAD shared, DINs distinct")
    return ok


if __name__ == "__main__":
    path = sys.argv[1]
    nets = parse(path)
    args = sys.argv[2:]
    if not args:
        for name in sorted(nets):
            nodes = ", ".join(f"{r}.{p}" for r, p in sorted(nets[name]))
            print(f"  {name:34} {nodes}")
        sys.exit(0)
    good = True
    i = 0
    while i < len(args):
        if args[i] == "--cell":
            good &= check_cell(nets, int(args[i + 1])); i += 2
        elif args[i] == "--cascade":
            good &= check_cascade(nets, int(args[i + 1])); i += 2
        else:
            i += 1
    sys.exit(0 if good else 1)
