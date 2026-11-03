# klp5e-c2-m7-drv8833-4motor stages

One folder per step of Module 7: the four-motor extension of the Module 6 capstone. The module
captures Module 6's driver stage as a design block, places it a second time on the sheet and on the
board, and grows the board to carry both stages. Each stage is the project as it stood at the end of
a lecture or bonus video and the start of the next one.

**Every stage is a complete KiCad project.** Open the `.kicad_pro` in a stage folder and it loads
on its own: the schematic, the board, the `.kicad_dru` custom rules, the project's symbol and
footprint library tables, `Libraries/` (the DRV8833 symbol and footprint and the logo footprints)
and `datasheets/`. From `01-block-circuit` on, the stage also holds the design block library
`peters_custom_Library.kicad_blocks/` and its table, `design-block-lib-table`: at the top of the
project folder in `01` and `02`, and inside `Libraries/` from `02b-block-tidied` on. Each stage holds
`tools/checknet.py`, the netlist checker, which now knows the second chip. Copy a stage folder out
of the repository before you work in it, and do not open two stages at once.

| Stage | State | Produced by |
|---|---|---|
| `00-start` | Module 6's `16-finished`, saved as the new project `klp5e-c2-m7-drv8833-4motor`; the netlist checker replaced by the four-motor one | bonus B7.1 |
| `01-block-circuit` | The design block `DRV8833 h-bridge motor stage` in the project's block library, holding the driver stage's circuit (`U1`, `C2`, `C3`, `C4`, `R2`, `R3`, `J2`, `J3`, their labels and grounds); the board is unchanged | lecture 7.1 |
| `02-block-captured` | The same block updated with the stage's layout: the eight footprints, their tracks and vias, the four motor legends and the `U1_breakout` rule area | lecture 7.2 |
| `02b-block-tidied` | The block library moved into `Libraries/` and the block renamed `DRV8833-Stage`; the sheet and board groups renamed and re-linked to it; the eight stage-one parts and the `U1_breakout` rule area locked | lecture 7.2b |
| `03-sheet-arranged` | The parts that appear only once moved along the bottom of the sheet to make room for a second stage; no connection changed | bonus B7.2 |
| `04-second-stage` | The block placed a second time and grouped: `DRV8833-Stage-1` and `DRV8833-Stage-2`, the copy's parts `U2` to `J6`; its labels are still stage one's, so ERC reports 5 errors | lecture 7.3 |
| `05-labels-renamed` | Stage two's twelve labels renamed (`CIN1`, `COUT1` and so on); 32 nets; ERC leaves 8 expected items | lecture 7.4 |
| `06-stage-on-board` | Stage two on the board beside the outline, laid out and routed by the block; its motor legends retyped; rule areas `U1_breakout` and `U2_breakout` | lecture 7.5 |
| `07-board-grown` | The board grown to 91 × 48 mm with stage two inside it; the old runs to `J4` cut back, `J4` and `R1` moved | bonus B7.3 |
| `08-trunk-routed` | `Power` class at 3.80 mm; the `VM` rail routed as a 3.80 mm trunk that splits above `C1` into 1.50 mm branches to the two stages | lecture 7.6 |
| `09-rules-fixed` | The two custom rules copied from Module 6 edited to cover both stages; DRC clear of width and breakout violations. `J4` is still the eight-pin header: this is Activity A7.1's start | lecture 7.7 |
| `10-header-routed` | `J4` replaced by the 2 × 6 header and routed to both stages; the outline cut to 86 × 48 mm, the right-hand holes moved with it | bonus B7.4 |
| `11-stage-classed` | Stage two's eight parts given the component class `Stage-2`, on the sheet and on the board | lecture 7.8 |
| `12-finished` | Stage one's leftover copper group ungrouped, so each stage has one group; pours refilled; DRC clean (0 violations, 0 unconnected, 0 parity). Module 8 starts here | bonus B7.5 |

## Activity A7.1

[`A7.1-activity/`](A7.1-activity/) holds Activity A7.1, "Swap the header and route the control side": the task (`README.md`), the record sheet you fill in (`record-sheet.md`) and the slide deck (`slides.html`). It starts from `09-rules-fixed`.
