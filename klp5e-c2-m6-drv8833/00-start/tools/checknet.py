#!/usr/bin/env python3
"""Read a KiCad netlist and assert what Module 6 draws on the capstone's sheet.

Course 2's copy of Volume 2's tools/checknet.py (M6 P2, 2026-10-28). One change: J3's two
pins may be in either order, as a pair. Module 6 wires J3 as the sheet reads (BOUT1 on pin 1,
L6.5) and re-pins it while routing bridge B (A6.1, worked in bonus B6.5); the book's checker
knows only the re-pinned order. Everything else is the book's, unchanged.

ERC is not proof. It reads clean while a pin sits a hair off grid and connects to
nothing, and it is entirely happy with a wire that connects the wrong two things
correctly. Chapter 8 tells the reader to export the netlist and read it at step 8
for exactly that reason, so the shipped project had better survive the check it
asks for.

`parse()` and `net_of()` are ch07's, unchanged, so a fix to the parser ports both
ways. Everything below them is this board.

Usage:
    checknet.py net.net                 # dump every net and its nodes
    checknet.py net.net --nets          # assert the whole of spec section 4
    checknet.py net.net --u1-pins       # assert all 17 U1 pins appear exactly once
    checknet.py net.net --classes       # assert the four netclass patterns resolved
"""
import re
import sys

# ---------------------------------------------------------------------------
# Spec section 4, transcribed. Local labels reach the netlist with a leading "/"
# because they live on the root sheet; power symbols do not, which is why GND is
# the one name here without one.
#
# Q1's drain is on the INCOMING side and its source on the board's VM rail. That
# is backwards from a load switch and it is the whole point of the part: see spec
# section 1.5. The spec's own net table had these two swapped until 2026-08-18.
#
# The two PWR_FLAGs are absent below, and so are the ground symbols. Both are
# virtual parts, marked by their leading "#", and KiCad leaves them out of the
# exported netlist entirely. They are on the sheet and they do their job for ERC;
# there is simply nothing of them to assert here.
# ---------------------------------------------------------------------------
NETS = {
    "/VM_IN":  {("J1", "1"), ("Q1", "2")},                       # Q1 pin 2 = D
    "/VM":     {("Q1", "3"), ("C1", "1"), ("C2", "1"), ("C3", "1"),
                ("R5", "1"), ("U1", "12")},                      # Q1 pin 3 = S
    "GND":     {("J1", "2"), ("C1", "2"), ("C2", "2"), ("C4", "2"), ("R4", "2"),
                ("D1", "1"), ("R2", "2"), ("R3", "2"), ("J4", "2"),
                ("U1", "13"), ("U1", "17")},
    "/AOUT1":  {("U1", "2"), ("J2", "1")},
    "/AOUT2":  {("U1", "4"), ("J2", "2")},
    # J3 as the sheet is first drawn (L6.5). Re-pinning it while routing bridge B (A6.1)
    # swaps the two; J3_REPINNED below is the other accepted state. J3 is NOT in
    # SYMMETRIC: the two pins must move together, never one alone.
    "/BOUT1":  {("U1", "7"), ("J3", "1")},
    "/BOUT2":  {("U1", "5"), ("J3", "2")},
    "/AISEN":  {("U1", "3"), ("R2", "1")},
    "/BISEN":  {("U1", "6"), ("R3", "1")},
    "/VCP":    {("U1", "11"), ("C3", "2")},
    "/VINT":   {("U1", "14"), ("C4", "1")},
    "/VLOGIC": {("J4", "1"), ("R1", "1")},
    "/nFAULT": {("U1", "8"), ("R1", "2"), ("J4", "4")},
    "/nSLEEP": {("U1", "1"), ("J4", "3")},
    "/AIN1":   {("U1", "16"), ("J4", "5")},
    "/AIN2":   {("U1", "15"), ("J4", "6")},
    "/BIN1":   {("U1", "9"), ("J4", "7")},
    "/BIN2":   {("U1", "10"), ("J4", "8")},
    "/GATE":   {("Q1", "1"), ("R4", "1")},                       # Q1 pin 1 = G
}

# J3 after the re-pin: both of bridge B's outputs change pins together.
J3_REPINNED = {
    "/BOUT1":  {("U1", "7"), ("J3", "2")},
    "/BOUT2":  {("U1", "5"), ("J3", "1")},
}

# The twentieth net. Deliberately unnamed: nothing refers to it, so KiCad's own
# name is the right one. Asserted by its nodes rather than by its name, because
# the name is KiCad's to choose.
UNNAMED = {("R5", "2"), ("D1", "2")}                             # D1 pin 2 = A

# Parts whose two pins are interchangeable, so the table above records one of two
# equally correct wirings and this checker must not care which it finds.
#
# It matters in practice: rotating or mirroring a resistor while rewiring swaps its
# pin numbers, and an earlier version of this file reported that as a connectivity
# failure on a board that was perfectly correct. A resistor has no polarity, both
# pads are the same pad, and the bill of materials cannot tell.
#
# C1 and D1 are deliberately absent. C1 is Device:C_Polarized and D1 is an LED, and
# for those two the pin numbers are the whole point.
SYMMETRIC = {"R1", "R2", "R3", "R4", "R5", "C2", "C3", "C4"}


def canon(nodes):
    """Nodes with symmetric parts' pin numbers flattened, counted not setted.

    A Counter rather than a set, so two pins of the same resistor landing on one net
    still reads as different from one pin: flattening the numbers must not also
    flatten a genuine short.
    """
    from collections import Counter
    return Counter((r, "*" if r in SYMMETRIC else p) for r, p in nodes)

# What the four assignment patterns in the .kicad_pro have to produce. KiCad
# prints every class a net resolved to in the netlist's `class` field, so this is
# provable headlessly rather than by looking at the Board Setup dialogue.
CLASSES = {
    "/VM": "Power", "/VM_IN": "Power", "GND": "Power",
    "/AOUT1": "Power", "/AOUT2": "Power", "/BOUT1": "Power", "/BOUT2": "Power",
    "/AISEN": "Sense", "/BISEN": "Sense",
    "/VCP": "Default", "/VINT": "Default", "/VLOGIC": "Default",
    "/nFAULT": "Default", "/nSLEEP": "Default", "/GATE": "Default",
    "/AIN1": "Default", "/AIN2": "Default", "/BIN1": "Default", "/BIN2": "Default",
}

U1_PINS = [str(n) for n in range(1, 18)]      # the PowerPAD is pin 17


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


def parse_classes(path):
    """{net name: [class, ...]} from the netlist's own class field."""
    s = open(path, encoding="utf-8").read()
    out = {}
    for m in re.finditer(r'\(name "([^"]*)"\)\s*\n\s*\(class "([^"]*)"\)', s):
        out[m.group(1)] = m.group(2).split(",")
    return out


def check_nets(nets):
    """Every net in spec section 4, node for node, plus the unnamed twentieth.

    Compared through canon(), so which way round a resistor happens to be wired is
    not treated as a defect. Everything else is compared exactly.
    """
    ok = True
    table = dict(NETS)
    if all(canon(nets.get(n, set())) == canon(w) for n, w in J3_REPINNED.items()):
        table.update(J3_REPINNED)
    for name, want in sorted(table.items()):
        got = nets.get(name)
        if got is None:
            ok = False
            print(f"  FAIL net {name!r} does not exist. Nets present: {sorted(nets)}")
        elif canon(got) != canon(want):
            ok = False
            cw, cg = canon(want), canon(got)
            missing = sorted((cw - cg).elements())
            extra = sorted((cg - cw).elements())
            print(f"  FAIL net {name!r}: missing {missing}, unexpected {extra}")
    # Anchored on the LED's anode rather than on R5, because D1 has a polarity and
    # R5 does not: R5's pin numbers are free to swap and D1's are not.
    name, got = net_of(nets, "D1", "2")
    if canon(got) != canon(UNNAMED):
        ok = False
        print(f"  FAIL the R5-to-D1 node is net {name!r} = {sorted(got)}, "
              f"expected exactly {sorted(UNNAMED)}")
    # VM_IN and VM must not have merged: a stray wire across the FET shorts out the
    # protection, and this is the only check on the board that would notice.
    if net_of(nets, "Q1", "2")[0] == net_of(nets, "Q1", "3")[0]:
        ok = False
        print("  FAIL Q1's drain and source are on the same net: the protection FET "
              "is shorted out and the board has no reverse-polarity protection")
    extra = set(nets) - set(NETS) - {name}
    if extra:
        ok = False
        print(f"  FAIL unexpected nets on the sheet: {sorted(extra)}")
    print(("  OK   " if ok else "  BAD  ") +
          f"{len(NETS)} named nets + 1 auto-named, exactly the nets step 5 names")
    return ok


def check_u1_pins(nets):
    """All seventeen pins of the driver appear on exactly one net each.

    Pin 17 is the exposed pad. It is the pin readers leave unwired, it is the only
    path the heat has out of the package, and a board whose pad carries no net looks
    perfect on the drawing.
    """
    ok = True
    for pin in U1_PINS:
        homes = [n for n, nodes in nets.items() if ("U1", pin) in nodes]
        if len(homes) != 1:
            ok = False
            where = "no net" if not homes else f"{len(homes)} nets {sorted(homes)}"
            print(f"  FAIL U1 pin {pin} appears on {where}")
        elif homes[0].startswith("unconnected-"):
            ok = False
            print(f"  FAIL U1 pin {pin} is unconnected ({homes[0]})")
    if ok and net_of(nets, "U1", "17")[0] != "GND":
        ok = False
        print("  FAIL U1 pin 17 (the exposed pad) is not on GND")
    print(("  OK   " if ok else "  BAD  ") +
          "all 17 U1 pins wired exactly once, pad included")
    return ok


def check_classes(path):
    """The four netclass patterns put every net where the chapter says they do."""
    got = parse_classes(path)
    ok = True
    for name, want in sorted(CLASSES.items()):
        have = got.get(name)
        if have is None:
            ok = False
            print(f"  FAIL net {name!r} is not in the netlist")
        elif want not in have:
            ok = False
            print(f"  FAIL net {name!r} resolved to {have}, expected to include {want!r}")
    print(("  OK   " if ok else "  BAD  ") +
          "*VM* / *GND / *OUT* / *ISEN resolved every net to its intended class")
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
    for a in args:
        if a == "--nets":
            good &= check_nets(nets)
        elif a == "--u1-pins":
            good &= check_u1_pins(nets)
        elif a == "--classes":
            good &= check_classes(path)
        else:
            print(f"  unknown option {a!r}")
            sys.exit(2)
    sys.exit(0 if good else 1)
