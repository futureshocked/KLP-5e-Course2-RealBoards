# A2.1: Author the HTSSOP footprint in your own library

You have watched the DRV8833's footprint being built in lectures 2.2 to 2.10. This activity builds
it again, in your own footprint library, and links it to the symbol you made in activity 1.1. The
numbers sheet below does the decoding for you; building the footprint and checking it are yours.

Allow 60 to 90 minutes. Fill in `record-sheet.md` as you go.

## What you start from

1. **Your symbol library from A1.1**, with `DRV8833_PD` (or your own name for it) and its
   Footprint field still empty. If you did not do A1.1, use stage `04-fields`, which holds the
   worked solution's `peters_custom_Library.kicad_sym`.
2. **The datasheet**, `drv8833.pdf` (TI SLVSAR1E), in stage `00-start` and `04-fields`. The package
   outline is on page 26 and the land pattern on page 27.
3. **The 3D model**, `HTSSOP-16-1EP_4.4x5mm_P0.65mm_EP3.4x5mm.step`, from KiCad's 3D library
   (`Package_SO.3dshapes`). If KiCad shows you no models at all, the library is not installed:
   download it from <https://gitlab.com/kicad/libraries/kicad-packages3D>, unpack it somewhere
   stable, and point "Preferences", "Configure Paths", `KICAD10_3DMODEL_DIR` at it. A copy of this
   one model ships beside this file.

You need no project until the last step. Close any open project before you start.

## The numbers sheet

Every value in millimetres, every position relative to the footprint's origin. Check each one
against the datasheet as you type it.

| Object | Layer | Number | Values |
|---|---|---|---|
| Body | F.Fab | none | rectangle (−2.2, −2.5) to (2.2, 2.5), filleted 0.2; pin 1 circle inside the top-left corner; dimensions 4.4 and 5 on User.2 |
| Pad 1 | F.Cu, F.Mask, F.Paste | 1 | SMD, rounded rectangle 1.5 × 0.45, corner radius 0.05, at (−2.9, −2.275) |
| Pad rows | as pad 1 | 1 to 16 | Create Array from pad 1: 2 × 8, spacing 5.8 × 0.65, Renumber pads, Vertical then horizontal, reverse alternate columns, from start value 1, source items remain in place |
| Exposed pad | F.Cu only | 17 | SMD, rectangle 3.4 × 5 at (0, 0), heatsink pad, pad connection Solid, no mask, no paste |
| Bottom landing | B.Cu only | 17 | SMD, rectangle 2.8 × 4.4 at (0, 0), heatsink pad, Solid, every technical layer cleared |
| Mask opening | F.Mask only | none | SMD Aperture, rectangle 2.46 × 2.31 at (0, 0) |
| Thermal vias | all copper, no technical layers | 17 | through-hole, circular 0.6 on a 0.3 hole, heatsink pad, padstack Front/Inner/Back with the back 0.8; first at (−1, −1.8), then Create Array 3 × 4 at 1 × 1.2, source items remain in place, **Renumber pads off** |
| Paste openings | F.Paste only | none | SMD Aperture, rounded rectangle 0.99 × 1.86, corner 25 %, at (−0.615, 0), then an array of 2 at 1.23 |
| Courtyard | F.Courtyard | none | rectangle (−3.9, −2.75) to (3.9, 2.75) |
| Silkscreen | F.Silkscreen | none | four corner marks outside the pad rows, touching no pad; a "•" text beside pad 1, 1 mm high, 0.125 thick; reference text 0.125 thick |
| Fields | footprint properties | none | a description and keywords; component type SMD; datasheet embedded as `kicad-embed://drv8833.pdf`; the 3D model embedded, scale 1, rotation 0, offset 0 |

## The ladder

Do the steps in this order.

1. **Your footprint library.** From the KiCad window, with no project open, open the Footprint
   Editor. "File", "New Library...". Same folder as your symbol library, a name you will keep, and
   **"Add new library to global library table"**: the dialogue's default registers it nowhere.
   (Lecture 2.2)
2. **A named footprint.** "New Footprint", then save it into your library as
   `HTSSOP-16-1EP_DRV8833_PD`, or your own name. (Lecture 2.2)
3. **The body.** F.Fab, the rectangle, its corners typed in the Properties panel, the two
   dimensions, the fillet, the pin 1 circle, the text moved clear. (Lecture 2.3)
4. **The pad rows.** Pad 1 from the sheet, then Create Array. Check: pad 2 sits 0.65 below pad 1,
   and the measure tool reads 5.8 from pad 1 to pad 16. (Lecture 2.4)
5. **Pad 17.** The top copper, the bottom landing, the mask opening. (Lecture 2.5)
6. **The vias.** One via with its pad stack, then the array. Untick "Renumber pads". Then open the
   Pad Table and copy its summary line onto your record sheet before you change anything.
   (Lecture 2.6)
7. **The paste, and the check.** The two paste openings. "Inspect", "Footprint Checker", "Run
   Checks"; read the Pad Table's summary line; fix what they report. Then show F.Mask, F.Paste and
   B.Cu one at a time. (Lecture 2.7)
8. **The outer layers.** Courtyard and silkscreen, the 0.125 thicknesses, and a clean Footprint
   Checker. (Lecture 2.8)
9. **The paperwork.** Description and keywords, the embedded datasheet, the embedded 3D model.
   Press D to open the datasheet from the footprint. Save. (Lecture 2.9)
10. **The link.** In the Symbol Editor, still with no project, open your symbol's properties and
    fill its Footprint field with the library button. Read the chooser's preview: every pad
    should carry its pin's name. Save. (Lecture 2.10)
11. **Find it from a project.** Make a throwaway project, open its schematic, press A and type
    `drv8833`. Your symbol's preview should show your footprint. Close without saving and delete
    the project's folder. (Lecture 2.11)

## Acceptance

Check every line before you compare.

- [ ] The Pad Table's summary reads 1-17 for the pad numbers, 33 for the pad count, and 17 for
      the duplicate pads, and nothing else.
- [ ] The Footprint Checker reports 0 errors and 0 warnings.
- [ ] F.Mask on its own is one window in the middle of pad 17; F.Paste on its own is two rounded
      rectangles.
- [ ] Every via is tented (no technical layer) and has a 0.8 ring on the back.
- [ ] The courtyard sits 0.25 outside the pads.
- [ ] The pin 1 dot and the reference are 0.125 thick.
- [ ] The datasheet and the 3D model are embedded, and D opens the datasheet.
- [ ] Your symbol's Footprint field names your footprint, as `yourlibrary:yourfootprint`, and the
      Footprint Chooser's preview puts the pin names on the pads: nSLEEP on 1, AIN1 on 16, PAD on 17.

## Compare

The worked solution is stage `13-linked`. To look at it beside your own, add its
`peters_custom_Library.pretty` folder in "Preferences", "Manage Footprint Libraries..." under a
nickname of your choosing, such as `a21-solution`, so that it cannot clash with your own library.
Remove that row when you have finished.

Your silkscreen can differ from the solution's. Your numbers, sizes and layers cannot.

## If you get stuck

1. **The New Library dialogue saved, but the library is not in the tree.** The project button
   was selected. With no project open it registers the library nowhere. Add the `.pretty` folder
   in "Manage Footprint Libraries...", "Global Libraries", or delete it and make it again with the
   global button.
2. **The Pad Table says "Duplicate pads: 1,10,11,12,17,2,…".** The vias were renumbered by Create
   Array. Change each through-hole row's number to 17 in the Pad Table.
3. **The pad rows are numbered 1 to 8 and 9 to 16 down both sides.** "Reverse numbering on
   alternate rows/columns" was off. Delete pads 2 to 16 and array pad 1 again.
4. **The array landed in the wrong place.** "Grid Position" was "Centre on source items". Undo
   and choose "Source items remain in place".
5. **The checker reports "Footprint has no courtyard defined".** The courtyard is missing, or it
   is on a layer other than F.Courtyard.
6. **Your footprint is not in the Footprint Chooser.** The library is not in the Global table (see
   1), or "Filter by pin count" is hiding it because your pad numbers do not run 1 to 17.

## Optional: a part of your own

Two choices, no worked solution for either:

1. A footprint for a part from your own work that has an exposed pad. Use its datasheet's package
   outline and land pattern; the datasheet is the answer key.
2. The pad rows again, by hand, in a copy of your footprint: place each pad with the relative
   readout (space bar, then move until dy reads 0.65), as Volume 2, Chapter 2 does. Compare the
   result with the array's.

## When you are done

You have a footprint library and a symbol library you will keep, and one component whose two
halves agree pad for pin. In Module 3 it goes on its first board.
