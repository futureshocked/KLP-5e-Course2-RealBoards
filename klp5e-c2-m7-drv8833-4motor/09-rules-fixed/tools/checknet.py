#!/usr/bin/env python3
"""Read a KiCad netlist and assert what Module 7 draws on the four-motor sheet.

Course 2's copy of Volume 2's ch09 tools/checknet.py (M7 P2, 2026-11-02, KiCad 10.0.8).
One change, carried from Module 6's copy: J3's two pins may be in either order, as a
pair, and so may J6's, which the design block copies from J3. Everything else is the
book's, unchanged, so its printed lines are the ones Chapter 9 shows.


This is `../ch08-drv8833/tools/checknet.py` carried forward to two stages. ERC is
still not proof, and on this sheet it is weaker than it was on Chapter 8's: twelve
labels arrive duplicated from the design block, ERC reports five of them, and the
seven it stays silent about are the ones that tie the two chips together. A netlist
is the only artefact that shows a rename left half done.

`parse()`, `net_of()`, `parse_classes()` and `canon()` are ch07's and ch08's,
unchanged, so a fix to the parser ports all three ways.

ONE COMMAND, TWO SHEETS. The chapter asks for this check twice, at two different
points in the build, and prints the same command both times. The two sheets differ
only in the header: `{#sec:c09-second-stage}` ends with Chapter 8's eight-pin `J4`
still fitted and the four new direction inputs dangling, and `{#sec:c09-control}`
ends with a 2 x 6 and all twelve wired. So the stage is read off the netlist rather
than passed in on the command line: count `J4`'s pins, and the file says which of
the two sheets it came from. A reader who runs the check at the wrong moment gets
the right answer for the sheet they have, not a wall of failures.

Usage:
    checknet.py net.net                 # dump every net and its nodes
    checknet.py net.net --nets          # assert every net, and the J4 pin map
    checknet.py net.net --u1-pins       # assert all 17 U1 pins appear exactly once
    checknet.py net.net --u2-pins       # the same for the second chip
    checknet.py net.net --classes       # assert the four netclass patterns resolved
"""
import re
import sys

# ---------------------------------------------------------------------------
# Everything on the sheet that does not depend on which header is fitted. Local
# labels reach the netlist with a leading "/" because they live on the root sheet;
# power symbols do not, which is why GND is the one name here without one.
#
# The J4 nodes are NOT here. They are in HEADERS below, one map per stage, and
# get added to these nets before the comparison runs.
#
# Read the two halves against each other. Stage one is Chapter 8's, unchanged
# except that VM and GND now carry the second chip's pins too. Stage two is what
# the design block stamped down, with the twelve renames of {#sec:c09-second-stage}
# applied: A and B became C and D, and VCP and VINT gained a 2.
# ---------------------------------------------------------------------------
BASE = {
    "/VM_IN":  {("J1", "1"), ("Q1", "2")},                       # Q1 pin 2 = D
    # One rail, both stages. The second chip's bypass pair (C5, C6) hangs off it
    # alongside the first's, which is the whole architecture in one net.
    "/VM":     {("Q1", "3"), ("C1", "1"), ("C2", "1"), ("C3", "1"), ("C5", "1"),
                ("C6", "1"), ("R5", "1"), ("U1", "12"), ("U2", "12")},
    "GND":     {("J1", "2"), ("C1", "2"), ("C2", "2"), ("C4", "2"), ("C5", "2"),
                ("C7", "2"), ("R4", "2"), ("D1", "1"), ("R2", "2"), ("R3", "2"),
                ("R6", "2"), ("R7", "2"),
                ("U1", "13"), ("U1", "17"), ("U2", "13"), ("U2", "17")},
    "/GATE":   {("Q1", "1"), ("R4", "1")},                       # Q1 pin 1 = G

    # Stage one. Four bridge outputs, two sense returns, the two pins the chip
    # drives itself. Every one of these must hold U1 and nothing of U2's: a pin
    # of the second chip on any of them is a rename that did not happen.
    "/AOUT1":  {("U1", "2"), ("J2", "1")},
    "/AOUT2":  {("U1", "4"), ("J2", "2")},
    # J3's two pins were reversed on 2026-08-24 while routing Chapter 8's board,
    # so that channel B's outputs stop crossing on the way to the connector. J3 is
    # NOT in SYMMETRIC below: which motor lead lands on which terminal is the point.
    "/BOUT1":  {("U1", "7"), ("J3", "2")},
    "/BOUT2":  {("U1", "5"), ("J3", "1")},
    "/AISEN":  {("U1", "3"), ("R2", "1")},
    "/BISEN":  {("U1", "6"), ("R3", "1")},
    "/VCP":    {("U1", "11"), ("C3", "2")},
    "/VINT":   {("U1", "14"), ("C4", "1")},

    # Stage two, the same eight nets under their new names. J6 carries J3's
    # reversal because the block copied the wiring along with the parts.
    "/COUT1":  {("U2", "2"), ("J5", "1")},
    "/COUT2":  {("U2", "4"), ("J5", "2")},
    "/DOUT1":  {("U2", "7"), ("J6", "2")},
    "/DOUT2":  {("U2", "5"), ("J6", "1")},
    "/CISEN":  {("U2", "3"), ("R6", "1")},
    "/DISEN":  {("U2", "6"), ("R7", "1")},
    "/VCP2":   {("U2", "11"), ("C6", "2")},
    "/VINT2":  {("U2", "14"), ("C7", "1")},

    # Shared by decision rather than by necessity, so both chips appear on each.
    "/nSLEEP": {("U1", "1"), ("U2", "1")},
    "/nFAULT": {("U1", "8"), ("U2", "8"), ("R1", "2")},
    "/VLOGIC": {("R1", "1")},

    # The eight direction inputs. Each is one chip pin here and picks up its
    # header pin from HEADERS below.
    "/AIN1":   {("U1", "16")},
    "/AIN2":   {("U1", "15")},
    "/BIN1":   {("U1", "9")},
    "/BIN2":   {("U1", "10")},
    "/CIN1":   {("U2", "16")},
    "/CIN2":   {("U2", "15")},
    "/DIN1":   {("U2", "9")},
    "/DIN2":   {("U2", "10")},
}

# The thirty-second net. Deliberately unnamed: nothing refers to it, so KiCad's own
# name is the right one. Asserted by its nodes rather than by its name.
UNNAMED = {("R5", "2"), ("D1", "2")}                             # D1 pin 2 = A

# The two headers this sheet wears, keyed by pin count so the netlist itself picks.
#
# 8 is Chapter 8's Conn_01x08_Pin, still fitted when {#sec:c09-second-stage} ends.
# CIN1, CIN2, DIN1 and DIN2 are absent from it on purpose: those four nets run from
# a label to one pin and stop, which is the eight ERC items that section finishes on.
#
# 12 is the Conn_02x06_Odd_Even of {#sec:c09-control}, and this map IS that section's
# table. It is the assertion worth having, because a label on the wrong header pin is
# the one failure that passes ERC in silence.
HEADERS = {
    8: {"/VLOGIC": "1", "GND": "2", "/nSLEEP": "3", "/nFAULT": "4",
        "/AIN1": "5", "/AIN2": "6", "/BIN1": "7", "/BIN2": "8"},
    12: {"GND": "1", "/VLOGIC": "2", "/nSLEEP": "3", "/nFAULT": "4",
         "/CIN1": "5", "/CIN2": "6", "/DIN1": "7", "/DIN2": "8",
         "/AIN1": "9", "/AIN2": "10", "/BIN1": "11", "/BIN2": "12"},
}

STAGE = {
    8: "J4 is Chapter 8's 8-pin header, so the four C and D inputs have nowhere "
       "to go yet",
    12: "J4 is the 2 x 6, so the twelve-row pin map is the one checked",
}

# Parts whose two pins are interchangeable, so the table above records one of two
# equally correct wirings and this checker must not care which it finds.
#
# It matters in practice: rotating or mirroring a resistor while rewiring swaps its
# pin numbers, and an earlier version of Chapter 8's file reported that as a
# connectivity failure on a board that was perfectly correct.
#
# C1 and D1 are deliberately absent. C1 is Device:C_Polarized and D1 is an LED, and
# for those two the pin numbers are the whole point.
SYMMETRIC = {"R1", "R2", "R3", "R4", "R5", "R6", "R7",
             "C2", "C3", "C4", "C5", "C6", "C7"}

# What the four assignment patterns in the .kicad_pro have to produce. They were
# written as patterns rather than as lists of names in Chapter 8, which is why the
# twelve new names need no Board Setup work at all: *OUT* catches COUT1 exactly as
# it caught AOUT1. This table is the proof of that claim.
CLASSES = {
    "/VM": "Power", "/VM_IN": "Power", "GND": "Power",
    "/AOUT1": "Power", "/AOUT2": "Power", "/BOUT1": "Power", "/BOUT2": "Power",
    "/COUT1": "Power", "/COUT2": "Power", "/DOUT1": "Power", "/DOUT2": "Power",
    "/AISEN": "Sense", "/BISEN": "Sense", "/CISEN": "Sense", "/DISEN": "Sense",
    "/VCP": "Default", "/VINT": "Default", "/VCP2": "Default", "/VINT2": "Default",
    "/VLOGIC": "Default", "/nFAULT": "Default", "/nSLEEP": "Default",
    "/GATE": "Default",
    "/AIN1": "Default", "/AIN2": "Default", "/BIN1": "Default", "/BIN2": "Default",
    "/CIN1": "Default", "/CIN2": "Default", "/DIN1": "Default", "/DIN2": "Default",
}

PINS = [str(n) for n in range(1, 18)]          # 16 signal pins, and 17 is the PowerPAD


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


def canon(nodes):
    """Nodes with symmetric parts' pin numbers flattened, counted not setted.

    A Counter rather than a set, so two pins of the same resistor landing on one net
    still reads as different from one pin: flattening the numbers must not also
    flatten a genuine short.
    """
    from collections import Counter
    return Counter((r, "*" if r in SYMMETRIC else p) for r, p in nodes)


def which_header(nets):
    """The stage, read off J4's pin count. None if it is neither of the two."""
    pins = {p for nodes in nets.values() for r, p in nodes if r == "J4"}
    return len(pins) if len(pins) in HEADERS else None


def expected(header):
    """BASE with the stage's J4 nodes folded in."""
    nets = {name: set(nodes) for name, nodes in BASE.items()}
    for name, pin in HEADERS[header].items():
        nets[name].add(("J4", pin))
    return nets


# J3 as first drawn in Module 6 (L6.5), before A6.1's re-pin; J6 is its copy. Either
# state of each terminal is accepted, as a pair: the two pins must move together.
PAIR_SWAPS = [
    {"/BOUT1": {("U1", "7"), ("J3", "1")}, "/BOUT2": {("U1", "5"), ("J3", "2")}},
    {"/DOUT1": {("U2", "7"), ("J6", "1")}, "/DOUT2": {("U2", "5"), ("J6", "2")}},
]


def accept_swaps(nets, want_all):
    """Swap in the other wiring of J3 or J6 where the netlist holds exactly that."""
    for alt in PAIR_SWAPS:
        if all(canon(nets.get(n, set())) == canon(v) for n, v in alt.items()):
            want_all.update({n: set(v) for n, v in alt.items()})
    return want_all


def check_nets(nets, header):
    """Every net node for node, the J4 pin map included, plus the unnamed one.

    Compared through canon(), so which way round a resistor happens to be wired is
    not treated as a defect. Everything else is compared exactly.
    """
    want_all = accept_swaps(nets, expected(header))
    ok = True
    for name, want in sorted(want_all.items()):
        got = nets.get(name)
        if got is None:
            # On this sheet a missing net almost always means a merged one: the
            # file holds 31 names because a rename did not happen, not because a
            # net vanished. So say the count rather than dumping thirty names.
            ok = False
            print(f"  FAIL net {name!r} does not exist. The file holds "
                  f"{len(nets)} nets, so something has swallowed it")
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
    # A rename left undone shows up here rather than as a missing net: the two
    # stages' nets merge, and the sheet comes back one or more nets short.
    extra = set(nets) - set(want_all) - {name}
    if extra:
        ok = False
        print(f"  FAIL unexpected nets on the sheet: {sorted(extra)}")
    print(("  OK   " if ok else "  BAD  ") +
          f"{len(want_all)} named nets + 1 auto-named, 32 in all, "
          f"and every J4 pin carries the signal the table gives it")
    return ok


def check_pins(nets, ref):
    """All seventeen pins of one driver appear on exactly one net each.

    Pin 17 is the exposed pad. It is the pin readers leave unwired, it is the only
    path the heat has out of the package, and a board whose pad carries no net looks
    perfect on the drawing. This board has two of them.
    """
    ok = True
    for pin in PINS:
        homes = [n for n, nodes in nets.items() if (ref, pin) in nodes]
        if len(homes) != 1:
            ok = False
            where = "no net" if not homes else f"{len(homes)} nets {sorted(homes)}"
            print(f"  FAIL {ref} pin {pin} appears on {where}")
        elif homes[0].startswith("unconnected-"):
            ok = False
            print(f"  FAIL {ref} pin {pin} is unconnected ({homes[0]})")
    if ok and net_of(nets, ref, "17")[0] != "GND":
        ok = False
        print(f"  FAIL {ref} pin 17 (the exposed pad) is not on GND")
    print(("  OK   " if ok else "  BAD  ") +
          f"all 17 {ref} pins wired exactly once, pad included")
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
          "*VM* / *GND / *OUT* / *ISEN resolved all 32 nets, the twelve new ones included")
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
    header = which_header(nets)
    if header is None:
        print("  FAIL J4 has neither 8 pins nor 12, so this netlist is from neither "
              "of the two sheets Chapter 9 checks")
        sys.exit(2)
    print(f"  --   {STAGE[header]}")
    good = True
    for a in args:
        if a == "--nets":
            good &= check_nets(nets, header)
        elif a == "--u1-pins":
            good &= check_pins(nets, "U1")
        elif a == "--u2-pins":
            good &= check_pins(nets, "U2")
        elif a == "--classes":
            good &= check_classes(path)
        else:
            print(f"  unknown option {a!r}")
            sys.exit(2)
    sys.exit(0 if good else 1)
