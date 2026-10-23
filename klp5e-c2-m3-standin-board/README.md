# klp5e-c2-m3-standin-board stages

One folder per step of Module 3's board setup, on a stand-in board: the DRV8833 capstone's chip on
a 42 x 30 mm board, placed and not routed. Each stage is the project as it stood at the end of a
lecture and the start of the next one. Module 3 sets the board's rules; nothing is routed yet.

**Every stage is a complete KiCad project.** Open the `.kicad_pro` in a stage folder and it loads
on its own: the schematic, the board, the project's symbol and footprint library tables, and
`Libraries/`, which holds the DRV8833 symbol and footprint from Module 2 (`peters_custom_Library`).
From `04-width-rule` on there is also a `.kicad_dru` file holding the custom rules. Copy a stage
folder out of the repository before you work in it, and do not open two stages at once.

| Stage | State | Produced by |
|---|---|---|
| `00-start` | The stand-in placed and unrouted, KiCad's default setup, no custom rules. The start of A3.1 | before lecture 3.1 |
| `01-floor` | The eight Constraints values set to the fabricator's floor | lecture 3.1 |
| `02-net-classes` | Default and Power net classes with the patterns `VM`, `*GND` and `*OUT*`. **The `VM` pattern has no asterisk**: the mistake lecture 3.2 finds | lecture 3.2 |
| `03-sizes` | The `VM` pattern fixed to `*VM`; the track-width and via-size menus filled in | lecture 3.3 |
| `04-width-rule` | The custom rules file holds rule 1, the Power minimum width | lecture 3.4 |
| `05-breakout-rule` | Rules 1 and 2: the second rule names its nets for U1's breakout | lecture 3.5 |
| `06-severity` | Rules 1, 2 and 3; two violation severities changed; DRC reports 0 violations. A3.1's worked solution | lecture 3.6 |

Stages `00-start` to `05-breakout-rule` report 11 `silk_edge_clearance` warnings for J1's
silkscreen at the board edge. Rule 3 in `06-severity` removes them.

## Activity A3.1

[`A3.1-activity/`](A3.1-activity/) holds the activity's task (`TASK.md`) and the record sheet
(`record-sheet.md`). Start from `00-start`, and compare your result with `06-severity` only after
you have checked every line of the acceptance list.

## Lecture 4.5

[`L4.5-stitching-examples/`](L4.5-stitching-examples/) holds the figure shown in lecture 4.5.
