# A7.1: Swap the header and route the control side

Both stages are on the board and both rules fit. What is left is the connector they share, and it is
yours. `J4` has eight pins; the four-motor board needs twelve. Swap it, wire it to the pin map below,
prove it, place it and route the control side, and fill in `record-sheet.md` as you go. Allow about
30 minutes.

This folder also holds `slides.html`, the lecture's slide deck, to open in a browser.

## What you start from

Download stage `09-rules-fixed` from `github.com/futureshocked/KLP-5e-Course2-RealBoards`: it is the folder
`klp5e-c2-m7-drv8833-4motor/09-rules-fixed`. Close KiCad, copy the stage folder somewhere you will keep it,
then open its `klp5e-c2-m7-drv8833-4motor.kicad_pro` from the KiCad project manager.

## The task

The board has to bring twelve signals to its edge: `VLOGIC`, `GND`, `nSLEEP` and `nFAULT`, and eight
direction inputs, four per chip (`AIN1`, `AIN2`, `BIN1`, `BIN2`, `CIN1`, `CIN2`, `DIN1`, `DIN2`).

## The part

One row of twelve is 31.48 mm long; two rows of six are 16.24 mm and take a keyed ribbon socket. Use
`Conn_02x06_Odd_Even` (library `Connector_Generic`) on `PinHeader_2x06_P2.54mm_Vertical`. Odd-even is the
numbering a ribbon cable expects: pins 1 and 2 side by side, 3 and 4 below them, and so on.

## The pin map

| Row | Odd pin | Signal | Even pin | Signal |
|---|---|---|---|---|
| 1 | 1 | `GND` | 2 | `VLOGIC` |
| 2 | 3 | `nSLEEP` | 4 | `nFAULT` |
| 3 | 5 | `CIN1` | 6 | `CIN2` |
| 4 | 7 | `DIN1` | 8 | `DIN2` |
| 5 | 9 | `AIN1` | 10 | `AIN2` |
| 6 | 11 | `BIN1` | 12 | `BIN2` |

Each row is a pair that belongs together. With pin 1 at the bottom, the header reads from the top: motors
A and B, motors C and D, the two shared lines, then the logic supply and its ground.

## The order of work

1. **Change Symbol, never delete.** Deleting the header takes its labels with it; Change Symbol keeps them.
   Double-click `J4` to open Symbol Properties, press "Change Symbol…", choose "Change selected symbol(s)",
   and as the "New library identifier:" enter `Connector_Generic:Conn_02x06_Odd_Even`.
2. **Check every field the swap leaves.** Read every field of `J4` afterwards: the swap leaves two of them
   describing the old part. Find them and set them right.
3. **Wire to the map.** Draw the wires and labels so that each pin carries the signal in the table. `R1`
   goes back between the two pins it joins, `nFAULT` and `VLOGIC`.
4. **ERC and the checker.** Run the ERC, then, from the project folder:

   ```
   kicad-cli sch export netlist -o net.net klp5e-c2-m7-drv8833-4motor.kicad_sch
   python3 tools/checknet.py net.net --nets --u2-pins --classes
   ```

5. **Update PCB** from the schematic.
6. **Place `J4`** against the right-hand board edge, pin 1 at the bottom. The footprint's anchor is pin 1,
   not its middle, so it will not land centred.
7. **Route the control side** at 0.25 mm (the `Default` class), vias allowed. `R1` sits between the two
   `J4` pads it joins. The four direction inputs of `U1` have to get past stage two. There are two clear
   `B.Cu` corridors: above stage two, y 79 to 83, and under it, y 99 to 103 (the board's top-left corner,
   its grid origin, is at x 120, y 70).

## Done when

Tick every line.

- [ ] ERC reports 0.
- [ ] `checknet.py` prints its three `OK` lines, and the count is 32 nets.
- [ ] Update PCB reports no error.
- [ ] `J4` is on the right-hand edge, pin 1 at the bottom.
- [ ] DRC (refill zones, parity on): no errors and no unconnected items.
- [ ] The record sheet is filled in.

Then compare with the worked solution in bonus B7.4.

## If you get stuck

1. **"Update PCB" reports "no pad found" for pins 9 to 12.** A field of `J4` still names the eight-pin part.
2. **The BOM says `Conn_01x08`.** Another field of `J4` still reads the old part.
3. **None of the old wires reaches a pin after the swap.** Delete them and redraw; the ERC's "Unconnected
   wire endpoint" finds them. Don't drag them onto a pin: they can land on the wrong one.
4. **`checknet.py` prints FAIL on two nets.** Two labels are on the wrong pins; read the FAIL line, it
   names both.
5. **The 2 x 6 lands off-centre.** Its anchor is pin 1.
