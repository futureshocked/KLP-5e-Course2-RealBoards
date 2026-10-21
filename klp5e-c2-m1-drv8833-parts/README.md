# klp5e-c2-m1-drv8833-parts stages

One folder per step of the DRV8833 symbol's and footprint's authoring, used by Course 2 Modules 1
and 2 and Activities A1.1 and A2.1. Each stage is the library as it stood at the end of a lecture
and the start of the next one.

**These are library folders, not projects.** Modules 1 and 2 work in the symbol and footprint
editors with no project open, so a stage holds the library file beside the datasheet and the two
CSV files. To open a stage, add its `peters_custom_Library.kicad_sym` in "Preferences", "Manage
Symbol Libraries..." under a nickname that cannot clash with your own library (for example
`stage-03`), or copy the file into your own library folder. Remove the row when you have finished.

| Stage | State | Produced by |
|---|---|---|
| `00-start` | The datasheet (`drv8833.pdf`, TI SLVSAR1E) and two pin files: `drv8833-pins-remaining.csv` (twelve pins) and `drv8833-pins-all.csv` (all seventeen); no library, no project. The start of A1.1 | before lecture 1.2 |
| `01-library` | The empty `peters_custom_Library` | lecture 1.2 |
| `02-five-pins` | `DRV8833_PD` with its body and the five left-edge pins. AIN1 is numbered 14: the mistake lecture 1.4 finds and fixes | lecture 1.3 |
| `03-pins-arranged` | All 17 pins, AIN1 corrected to 16, arranged by function on the 50 mil grid | lecture 1.4 |
| `04-fields` | The fields filled in, Footprint left empty for Module 2. A1.1's worked solution and A2.1's start | lecture 1.5 |
| `05-footprint-library` | Adds the footprint library `peters_custom_Library.pretty/` with the named, empty `HTSSOP-16-1EP_DRV8833_PD` | lecture 2.2 |
| `06-body` | The body on F.Fab, the pin 1 circle, and two dimensions on User.2 | lecture 2.3 |
| `07-pad-rows` | Pads 1 to 16 | lecture 2.4 |
| `08-exposed-pad` | Pad 17 on F.Cu (3.4 x 5 mm) and B.Cu (2.8 x 4.4 mm), with its F.Mask opening | lecture 2.5 |
| `09-thermal-vias` | Twelve thermal vias, **numbered 1 to 12**: the mistake lecture 2.7 finds and fixes | lecture 2.6 |
| `10-paste-checked` | Two paste apertures; the vias renumbered 17, tented, 0.6 mm with a 0.8 mm back ring; 33 pads | lecture 2.7 |
| `11-outer-layers` | Courtyard and silkscreen; the Footprint Checker clean | lecture 2.8 |
| `12-embedded` | Description, datasheet and 3D model embedded: the finished footprint | lecture 2.9 |
| `13-linked` | The symbol's Footprint field reads `peters_custom_Library:HTSSOP-16-1EP_DRV8833_PD`. A2.1's worked solution | lecture 2.10 |

From `05-footprint-library` on, each stage holds both libraries. To open the footprint, add the
stage's `peters_custom_Library.pretty` folder in "Preferences", "Manage Footprint Libraries..."
under a nickname that cannot clash with your own (for example `stage-08`).

## Activity A1.1

[`A1.1-activity/`](A1.1-activity/) holds the activity's task (`TASK.md`) and the record sheet you
fill in as you go (`record-sheet.md`). Start from `00-start`, and compare your result with
`04-fields` only after you have checked every line of the acceptance list.

Your pin positions can differ from the solution's. Your pin numbers and types cannot.

## Activity A2.1

[`A2.1-activity/`](A2.1-activity/) holds the activity's task (`TASK.md`), the record sheet
(`record-sheet.md`) and a copy of the 3D model, `HTSSOP-16-1EP_4.4x5mm_P0.65mm_EP3.4x5mm.step`,
for anyone without KiCad's 3D library. Start from your own library from A1.1, or from
`04-fields`, and compare your result with `13-linked` only after you have checked every line of
the acceptance list.

Your silkscreen can differ from the solution's. Your numbers, sizes and layers cannot.
