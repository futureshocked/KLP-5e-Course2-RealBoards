# A5.1: Finish the other cells with Repeat Layout

In lectures 5.7 and 5.8 you saw cell 1 routed and copied onto cells 2 to 4. Here the shared wiring
is already drawn into and out of cells 1 and 2. Your job is to give cells 3 and 4 theirs, with one
Repeat Layout from cell 2, and to record what arrived. Repair nothing yet: the next lecture reads
what the copy left, so leave it exactly as it lands.

Allow about 10 minutes. Fill in `record-sheet.md` as you go.
This folder also holds `slides.html`, the lecture's slide deck, to open in a browser.

## What you start from

Download stage `10-shared-wiring` from `github.com/futureshocked/KLP-5e-Course2-RealBoards`: it is the
folder `klp5e-c2-m5-led-matrix/10-shared-wiring`. Close KiCad, copy the stage folder somewhere you
will keep it, then open its `klp5e-c2-m5-led-matrix.kicad_pro` from the KiCad project manager and
open the PCB editor from there.

Before you change anything, write the Unrouted count on your record sheet.

## What is already done, and what is left

Cells 1 and 2 are finished, shared wiring included. Cell 2 carries its own share of every net the
cells pass along:

1. its own piece of the `CLK` strip, from just west of the `DS1`/`DS2` seam to just west of the
   `DS2`/`DS3` seam, with a drop through a via into `U2`;
2. the `LOAD` riser at the `DS1`/`DS2` seam and the stub from it into `U2`;
3. the `+5V` hop from `C1` into `R2`;
4. the link in from `U1`, and the link out from `U2`'s `DOUT` to a via just west of the `DS2`/`DS3`
   seam.

Cells 3 and 4 have their own cell routing, copied in lecture 5.8, and a `LOAD` riser standing at
each seam with nothing attached yet. They have no `CLK`, no `LOAD` stub, no `+5V` hop from the cell
before, and no link in or out. That is the work left, and the one Repeat Layout below does all of
it: you route nothing by hand.

`GND` stays unconnected everywhere. The copper pour in lecture 5.10 joins it.

## The steps

1. **Locked items.** In the Selection Filter, tick "Locked items". The matrices are locked, and the
   area edge you need lies on a locked matrix's courtyard.
2. **Widen group `DS2`'s area.** Zoom to the seam between `DS1` and `DS2`. Select group `DS2`'s area
   by its edge, and drag its west edge left to **x 28.75 mm from the grid origin**, about 1.25 mm past
   the seam. Watch X on the status bar while you drag: it reads 144.75 if KiCad shows page
   coordinates (the default) and 28.75 if it shows grid-origin coordinates. At that edge the area
   takes in the `+5V` hop from `C1`, the link via just west of the seam, the start of cell 2's `CLK`
   strip piece and the `LOAD` riser at the seam. Leave room for the track's own width: an edge that
   only touches a join does not take it in, and an edge further west takes in pieces of cell 1 that do not belong to cell 2. Write down where the west edge ended up.
3. **One Repeat Layout.** Select group `DS2`'s area. "Tools", "Multi-Channel", "Repeat Layout…".
   - "Anchor footprint:" `DS2`.
   - In the target list, untick `auto-placement-area-DS1`. KiCad offers cell 1 as a target,
     ticked; leave it ticked and cell 2's copper replaces cell 1's.
   - Clear "Copy footprint placement" and "Copy other items". They open ticked.
   - Leave "Copy routing" and "Include locked items" ticked.
4. **OK, then save.** Press OK, then save with Ctrl+S.

## Done when

Tick every line.

- [ ] Both targets report "OK".
- [ ] The message "Copied to 2 Rule Areas." appeared.
- [ ] Cells 3 and 4 each gain a `CLK` via, a `LOAD` hop, a `+5V` join, a link in and a link out.
- [ ] For each of cells 3 and 4, you have written down what arrived and anything that looks wrong.
- [ ] You repaired nothing.

Then compare with the worked solution, stage `11-copied`, made in bonus B5.6. Your board should
match it cell for cell, with one expected difference at the east end of cell 4: the copy also gives
cell 4 a piece of `CLK` strip running past `U4` and a link out from `U4`'s `DOUT` to a via, and
neither has anywhere to go. Bonus B5.6 deletes both at the end and explains why. Leave yours in
place and note them on your record sheet.

## Where you finish

You finish with your board saved straight after the one Repeat Layout, nothing repaired. Lecture
5.9 starts from stage `11-copied` and repairs what the copy left. To follow it on your own board,
first delete cell 4's two extra pieces, as B5.6 does; otherwise open `11-copied`.

## If you get stuck

1. **A target does not say "OK".** A part has moved out of its cell. Press Ctrl+Z to undo the step
   before it, and run the Repeat Layout again.
2. **A join is missing in cells 3 and 4.** The area edge cuts it. Widen the area a little more
   and run it again.
3. **Cell 1 changed.** `DS1` was left ticked as a target. Press Ctrl+Z, and run it again with
   it unticked.
