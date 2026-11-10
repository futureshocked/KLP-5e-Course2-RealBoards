# A9.1: Run the ladder on your four-motor board

You have watched the five checks run on the two-motor board and seen the plotted files made. This
activity runs the same checks, in the same order, on the four-motor board from Module 8, and then
makes the files for the factory once and the files for the assembler for each build. Ordering at the
end is optional. Fill in `record-sheet.md` as you go.

Allow 60 to 90 minutes. Ordering adds the fab's build and shipping time.

This folder also holds `slides.html`, the lecture's slide deck, to open in a browser.

## What you start from

Download stage `18-assembly-bill` from `github.com/futureshocked/KLP-5e-Course2-RealBoards`: it is the
folder `klp5e-c2-m7-drv8833-4motor/18-assembly-bill`. **Work on a copy.** Copy the stage folder
somewhere you will keep it, rename the copy `a91-four-motor`, close KiCad, and open the copy's
`klp5e-c2-m7-drv8833-4motor.kicad_pro` from the KiCad project manager.

The board has three builds (design variants): `< Default >`, `two-motor` and `without-sense`.

## The steps

Do them in this order. The five rungs are in steps 2 and 7; do each of them even when it comes back
clean.

1. **The finish.** Board Setup › Board Stackup › "Board Finish": set "Copper finish:" to ENIG.
   (Lecture 9.3)
2. **Rungs 1 and 2.** The DRC with the fab's numbers (refill zones, parity on), then the HQ DFM
   plugin: step through every row that is not clean. (Lecture 9.2)
3. **Plot the factory's files once.** Into `Gerbers/`: the nine layers with Protel filename
   extensions, the job file, and a single-file drill in millimetres, decimal format. (Lecture 9.4)
4. **Plot the assembler's files, one build at a time.** File › Fabrication Outputs › "Component
   Placement (.pos, .gbr)...": for each of the three builds, choose it first in the PCB editor's
   top toolbar (the dialogue's own "Design variant:" list does not change the file), then choose
   the CSV format, millimetres, tick "Exclude all footprints with the Do Not Populate flag set", and
   generate. The dialogue gives every build's file the same name, so give each build its own output
   directory beside the bills from Module 8: `BOM/position-default/`, `BOM/position-two-motor/` and
   `BOM/position-without-sense/`.
5. **The cross-out.** File › Plot: format PDF, layers `F.Fab` and `Edge.Cuts` only, "Design variant:"
   `two-motor`, "Indicate DNP on fabrication layers" ticked with "Cross-out", output directory
   `BOM/`. Open the PDF. Then put the Plot dialogue back to Gerber, `Gerbers/` and the nine layers,
   and press "Plot" before "Close": it saves its last format and directory with the board, and
   "Close" alone does not save what you put back.
6. **The archive.** Zip the factory's eleven files (the nine layers, the drill file and the job
   file), the files and not the folder. (Lecture 9.4)
7. **Rungs 3 to 5 on the zip.** The Gerber viewer, the online viewer and the desktop application.
   (Lecture 9.5)

For each rung, write down what it found that the rung before it did not. If it found nothing, write
that too.

**One rule:** if a rung finds a problem, fix the layout in KiCad, plot again, and start the affected
rungs again. Never edit the output files by hand.

## Checks to make yourself

1. **The nine layers are the same whichever build is selected.** Plot them twice, under two
   different builds, into two folders, and compare the files: only their creation-date lines may
   differ. A variant changes which parts are fitted, never the copper.
2. **The two-motor position file is shorter than the default one by eight lines.** The
   `two-motor` build leaves stage two unfitted; with the do-not-populate box ticked, those parts
   drop out. The other two files are the same length as each other.
3. **The cross-out covers stage two only.** In the PDF, the same eight parts that dropped out of
   the position file carry the cross, and nothing else does.

## Before you order

1. Make the choices from Lecture 9.6. The parser's numbers are yours, not the lecture's.
2. Expect the same engineering query as in Lecture 9.6, about the holes under each chip. The notes
   in `if-you-order.md` give the answer that was sent.

## If you get stuck

1. **The plugin and the online viewer disagree.** Each speaks for its own factory's limits. Fix
   what you can, and justify in the record sheet what you leave.
2. **The fab rejects the drill file.** Check the format against Lecture 9.4: decimal format, one
   file for PTH and NPTH.
3. **A finding is on a feature you cannot move.** Write it down with the reason. A justified
   finding is a valid result.
4. **The plugin's rows come twice over.** That is the two chips: `U1` and `U2` carry the same rows.
   Lecture 9.2 explains each row. Gold rows print orange, and the Check window calls them
   "Warning" and the red ones "Error".
5. **The plugin stops responding after you click entries in more than one row.** Close the plugin
   window and open it again from the toolbar; the table comes back at once.
6. **The DRC dialogue has no "Test for parity between PCB and schematic" box.** Open the PCB editor
   from the Project Manager, not from the schematic.
7. **The "Copper finish:" list shows None and no ENIG.** The list opens scrolled to the bottom;
   scroll up.
8. **The placement dialogue opens on a format that is not CSV.** On a fresh configuration it opens
   on "Format:" Plain text. Choose CSV, and check "Units:" Millimeters and that the output directory
   reads `BOM/`. In Lecture 9.4 the dialogue named the file `<project>-all-pos.csv`; read the name
   it gives each build.
9. **`Gerbers/` holds twelve files.** The drill dialogue's "Generate map:" is ticked. Clear it, delete
   the `-drl_map.ps` file, and plot the drill again. The factory's eleven files are the nine layers,
   one drill file and the job file.
10. **The two-motor position file lists `U2`.** The box "Exclude all footprints with the Do Not
    Populate flag set" is clear. Tick it and generate that build again.
11. **The plugin is not on the toolbar.** Install it from the Plugin and Content Manager: "Install",
    then "Apply Pending Changes" (bonus B9.1).
12. **All three position files are alike.** The build was chosen in the placement dialogue. Choose
    it in the PCB editor's top toolbar, then generate that build's file again.

## When you are done

You have a filled record sheet, the eleven files and the zip, one position file per build, and the
cross-out drawing. If you want boards, an order placed. Show the board to someone when it arrives.
Then compare with the worked solution in bonus B9.2.
