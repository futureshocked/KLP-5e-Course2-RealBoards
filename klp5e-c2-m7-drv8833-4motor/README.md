# klp5e-c2-m7-drv8833-4motor stages

One folder per step of Module 7: the four-motor extension of the Module 6 capstone. The module
captures Module 6's driver stage as a design block, places it a second time on the sheet and on the
board, and grows the board to carry both stages. Each stage is the project as it stood at the end of
a lecture or bonus video and the start of the next one.

**Every stage is a complete KiCad project.** Open the `.kicad_pro` in a stage folder and it loads
on its own: the schematic, the board, the `.kicad_dru` custom rules, the project's symbol and
footprint library tables, `Libraries/` (the DRV8833 symbol and footprint and the logo footprints)
and `datasheets/`. From `01-block-circuit` on, the stage also holds the design block library
`peters_custom_Library.kicad_blocks/` and its table, `design-block-lib-table`. Each stage holds
`tools/checknet.py`, the netlist checker, which now knows the second chip. Copy a stage folder out
of the repository before you work in it, and do not open two stages at once.

| Stage | State | Produced by |
|---|---|---|
| `00-start` | Module 6's `16-finished`, saved as the new project `klp5e-c2-m7-drv8833-4motor`; the netlist checker replaced by the four-motor one | bonus B7.1 |
| `01-block-circuit` | The design block `DRV8833 h-bridge motor stage` in the project's block library, holding the driver stage's circuit (`U1`, `C2`, `C3`, `C4`, `R2`, `R3`, `J2`, `J3`, their labels and grounds); the board is unchanged | lecture 7.1 |
| `02-block-captured` | The same block updated with the stage's layout: the eight footprints, their tracks and vias, the four motor legends and the `U1_breakout` rule area | lecture 7.2 |
