# klp5e-c2-m6-drv8833 stages

One folder per step of Module 6's capstone: a two-motor driver board built round the DRV8833,
using the symbol and footprint you authored in Modules 1 and 2. The module draws the sheet, sets
the board up, places the driver stage first and routes the motor bridges at full width. Each stage
is the project as it stood at the end of a lecture or bonus video and the start of the next one.

**Every stage is a complete KiCad project.** Open the `.kicad_pro` in a stage folder and it loads
on its own: the schematic, the board, the project's symbol and footprint library tables,
`Libraries/` (the DRV8833 symbol and footprint) and `datasheets/`. From `05-board-setup` on, the
stage also holds the `.kicad_dru` custom rules. Each stage also holds `tools/checknet.py`, the
netlist checker, and `tools/checkplacement.py`, the placement checker. Copy a stage folder out of
the repository before you work in it, and do not open two stages at once.

| Stage | State | Produced by |
|---|---|---|
| `00-start` | An empty A4 sheet with the title block, an empty board, the `Default` net class only, the DRV8833 library and datasheet, and the two checkers | bonus B6.1 |
| `01-classes-and-stage` | The `Power` and `Sense` net classes and their four patterns; the eight-part driver stage placed on the sheet, unannotated and unwired | lecture 6.4 |
| `02-sheet-placed` | Every part placed and annotated, with values and footprints filled in; still no wire | bonus B6.2 |
| `03-wired` | The sheet wired and labelled; ERC reports two `power_pin_not_driven` errors | lecture 6.5 |
| `04-netlist-clean` | Two `PWR_FLAG`s added; ERC clean; checknet's three checks pass | lecture 6.6 |
| `05-board-setup` | The fabricator's limits and mask clearance imported, default severities, two copper layers, the two-rule `.kicad_dru`; the board is still empty | lecture 6.7 |
| `06-outline` | Predefined track and via sizes, silkscreen default 0.15 mm, the 20 footprints on the board, the outline drawn | bonus B6.3 |
| `07-stage-placed` | The eight driver-stage parts placed; the other twelve still off the board | lecture 6.8 |
| `08-all-placed` | Every part at its table position, the driver stage locked; the board agrees with the sheet | bonus B6.4 |
| `09-bridge-a` | `VM_IN`, `VM`, `AOUT1`, `AOUT2` and `AISEN` routed on `F.Cu`. The start of A6.1 | lecture 6.9 |

Stages to the end of the module are added as they are recorded.

## Checking the netlist (lecture 6.6)

From a stage folder, from `03-wired` on:

```bash
kicad-cli sch export netlist -o net.net klp5e-c2-m6-drv8833.kicad_sch
python3 tools/checknet.py net.net --nets
python3 tools/checknet.py net.net --u1-pins
python3 tools/checknet.py net.net --classes
```

On `04-netlist-clean` and later, all three pass.

## Checking the placement (bonus B6.4)

From a stage folder, from `08-all-placed` on:

```bash
python3 tools/checkplacement.py --outline --fit --overlap --proximity
```

On `07-stage-placed` it fails, because twelve parts are still off the board.

## Activity A6.1

[`A6.1-activity/`](A6.1-activity/) has everything for the activity in its own README: where you
start, the task, the settings, the acceptance list and what to do if you get stuck. The folder also
holds a record sheet (`record-sheet.md`) and the lecture's slide deck (`slides.html`). Start from
`09-bridge-a`. The worked solution is bonus B6.5, and its stage, `10-bridge-b`, is added here once
it is recorded.
