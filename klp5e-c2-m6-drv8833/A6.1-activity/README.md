# A6.1: Route bridge B

Bridge A is routed. Bridge B is the mirror image of it, and it is yours. Route its three nets
`BOUT2`, `BISEN` and `BOUT1` on the front, the way bridge A was routed, with the same widths and the
same necks, and fill in `record-sheet.md` as you go. Allow about 15 minutes.
This folder also holds `slides.html`, the lecture's slide deck, to open in a browser.

## What you start from

Download stage `09-bridge-a` from `github.com/futureshocked/KLP-5e-Course2-RealBoards`: it is the folder
`klp5e-c2-m6-drv8833/09-bridge-a`. Close KiCad, copy the stage folder somewhere you will keep it, then
open its `klp5e-c2-m6-drv8833.kicad_pro` from the KiCad project manager and open the PCB editor from
there.

The supply and bridge A are already routed. Bridge B's three nets are not.

## The task

Route `BOUT2`, `BISEN` and `BOUT1` from `U1`'s pins 5, 6 and 7 on `F.Cu`, the way bridge A was routed.
Look at where the ratsnest lines go before you draw anything. A crossing has to be absorbed somewhere:
decide where, choose the cheapest, and write on the record sheet why. Whatever you choose has a cost
somewhere; write that down too.

## The settings

1. **Widths.** Pick the width from the drop-down on the top toolbar before each segment; the router keeps
   the last one.
   - `Track: 0.300 mm` off the pad, then `Track: 0.800 mm`, then `Track: 1.500 mm`.
   - The sense return, `BISEN`, steps from `Track: 0.300 mm` to `Track: use netclass width` after its
     neck, which is 0.60.
2. **Grid.** Route on the 0.025 mm grid near the chip.
3. **Necks.** Each 0.30 neck is about 2 mm or less. Measure it with the measure tool (Ctrl+Shift+M).

## Done when

Tick every line.

- [ ] Three nets on `F.Cu`: `BOUT2`, `BISEN` and `BOUT1`.
- [ ] No via.
- [ ] No detour round a connector.
- [ ] Each 0.30 neck is about 2 mm or less.
- [ ] No unrouted bridge B net: the unrouted count of the three nets is 0.
- [ ] The record sheet is filled in.

The DRC is not part of this task. Don't chase DRC markers at the chip yet: the next lectures are about
exactly that.

Then compare with the worked solution in bonus B6.5, and after that we run the DRC on the routed board.

## If you get stuck

1. **The router will not land on a pad.** The track is wider than 0.30 mm at that point. Switch to
   `Track: 0.300 mm` for the last hop onto the pad.
2. **A neck is longer than 2 mm.** The router enforces clearance, not width: it will never complain about
   a 0.30 mm neck that runs too far. Move the step to 0.80 mm closer to the chip.
3. **A short stub or a dangling end after a click.** An off-grid click leaves a 0.035 mm stub. Route on
   the 0.025 mm grid near the chip, or click straight on to the next segment.
4. **A crossing you cannot route on one layer.** That is the task: decide where it goes.
5. **The router refuses a segment beside another escape**, outside the chip's courtyard. The class's
   0.30 mm clearance applies there. Space the escapes as bridge A does.
