# klp5e-c2-m1-drv8833-parts stages

One folder per step of the DRV8833 symbol's authoring, used by Course 2 Module 1 and Activity
A1.1. Each stage is the library as it stood at the end of a lecture and the start of the next one.

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
| `04-fields` | The fields filled in, Footprint left empty for Module 2. A1.1's worked solution | lecture 1.5 |

## Activity A1.1

[`A1.1-activity/`](A1.1-activity/) holds the activity's task (`TASK.md`) and the record sheet you
fill in as you go (`record-sheet.md`). Start from `00-start`, and compare your result with
`04-fields` only after you have checked every line of the acceptance list.

Your pin positions can differ from the solution's. Your pin numbers and types cannot.

Module 2's stages (`05-` to `13-`), which add the footprint library, are added here once that
module is recorded.
