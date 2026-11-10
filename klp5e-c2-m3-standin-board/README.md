# klp5e-c2-m3-standin-board stages

One folder per step of Module 3's board setup, on a stand-in board: the DRV8833 capstone's chip on
a 42 x 30 mm board, placed and not routed. Each stage is the project as it stood at the end of a
lecture and the start of the next one. Module 3 sets the board's rules on the unrouted board; Module 4 continues on the routed board from `07-routed` and adds the copper zones.

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
| `07-routed` | The stand-in routed on `06-severity`'s setup: 50 track segments and 3 vias, no zone yet. DRC reports 0 violations and 3 unconnected items (GND to U1 pad 17). Module 4 starts here | Module 4 start |
| `08-gnd-top` | `GND_top` poured on F.Cu at the dialogue's defaults; DRC reports one `starved_thermal` on U1 pad 13 | lecture 4.1 |
| `09-gnd-both` | `GND_bottom` added on B.Cu; both pours at minimum width 0.2 mm, clearance 0.5 mm, spoke 0.5 mm; the same `starved_thermal` | lecture 4.2 |
| `10-thermal` | Both pours at clearance 0.2 mm, minimum width 0.2 mm, spoke 0.3 mm; DRC reports 0 violations | lecture 4.3 |
| `11-vm-zone` | `VM_zone` added on F.Cu (`/VM`, L-shaped, 2 mm fillet), at a higher priority than `GND_top`; the four VM track segments it replaces deleted | lecture 4.4 |
| `12-stitched` | Nine free GND stitching vias (0.6 / 0.3 mm) in the top-right corner | lecture 4.5 |
| `13-keepout` | The rule area `Mounting hole` keeps tracks, vias and zone fills away from the hole; DRC reports 0 violations | lecture 4.6 |

Stages `00-start` to `05-breakout-rule` report 11 `silk_edge_clearance` warnings for J1's
silkscreen at the board edge. Rule 3 in `06-severity` removes them.

## Activity A3.1

[`A3.1-activity/`](A3.1-activity/) has everything for the activity in its own README: the
instructions, every value to enter and the acceptance list. The folder also holds a record sheet
(`record-sheet.md`) and the lecture's slide deck (`slides.html`). Start from `00-start`, and compare
your result with `06-severity` only after you have checked every line of the acceptance list.

## Lecture 4.5

[`L4.5-stitching-examples/`](L4.5-stitching-examples/) holds the figure shown in lecture 4.5.
