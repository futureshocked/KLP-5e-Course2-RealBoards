# A1.1: Author the DRV8833 symbol in your own library

You have watched the DRV8833 symbol being made in lectures 1.2 to 1.5. This activity makes it
again, in your own library, under your own name. The pin file does part of the work; reading the
datasheet, placing the pins and checking the result are yours.

Allow 45 to 60 minutes. Fill in `record-sheet.md` as you go.
This folder also holds `slides.html`, the lecture's slide deck, to open in a browser.

## What you start from

Stage `00-start`, which holds three files and no project:

1. `drv8833.pdf`, the datasheet (TI SLVSAR1E). The Pin Functions table is on pages 3 and 4.
2. `drv8833-pins-remaining.csv`, twelve of the seventeen pins.
3. `drv8833-pins-all.csv`, all seventeen. Use it only to check your work at the end.

You need no project for any of this. Close any open project before you start.

## The ladder

Do the steps in this order.

1. **Your library.** From the KiCad window, with no project open, open the Symbol Editor. "File",
   "New Library...". Save it in a folder you keep for long-lived work, outside every project, and
   give it a name you will keep. (Lecture 1.2)
2. **The symbol and its body.** "New Symbol": name `DRV8833_PD`, or your own ending in place of
   `_PD`; designator U; one unit. Draw the body rectangle. Set the grid to 50 mil first.
   (Lecture 1.3)
3. **Five pins by hand.** AIN1, AIN2, BIN1, BIN2 and nSLEEP, all of type Input, on the left edge,
   each through the Pin Properties dialogue. Read the numbers from the column for the package you
   are drawing, the HTSSOP. (Lecture 1.3)
4. **Import the other twelve.** Open the Pin Table. Check that "Append to existing pins" is
   selected, then "From File..." and `drv8833-pins-remaining.csv`. Before you change anything,
   copy the summary line onto your record sheet. (Lecture 1.4)
5. **Arrange by function.** The imported pins are stacked at the origin. Drag them out on the
   50 mil grid: bridge A, bridge B and nFAULT on the right, VM, VINT and VCP along the top, GND and
   PAD along the bottom. Resize the body to fit and move the Value text clear of every pin name.
   Run the Symbol Checker, fix what it reports, and save. (Lecture 1.4)
6. **The fields.** In Library Symbol Properties: Value `DRV8833`, a one-line Description, the
   datasheet link in Datasheet, and two fields of your own with "+": MPN `DRV8833PWPR` and
   Supplier. Leave Footprint empty. Save. (Lecture 1.5)
7. **Find it from a project.** Make a throwaway project, open its schematic, press A and type
   `drv8833`. Your symbol should be listed under your library's name, with "No footprint
   specified" in its preview. Then close the project without saving and delete its folder.
   (Lecture 1.6)

## Acceptance

Check every line before you compare.

- [ ] The Pin Table's summary line reads 1-17 for the pin numbers, 17 for the pin count, and none
      for the duplicate pins.
- [ ] Every pin's type matches the table in lecture 1.1, and `drv8833-pins-all.csv`.
- [ ] The Symbol Checker reports nothing.
- [ ] Reference, Value, Description, Datasheet, MPN and Supplier are filled in.
- [ ] Footprint is empty. Module 2 fills it.

## Compare

The worked solution is stage `04-fields`. To look at it beside your own, add its
`peters_custom_Library.kicad_sym` in Manage Symbol Libraries under a nickname of your choosing,
such as `a11-solution`, so that it cannot clash with your own library. Remove that row when you
have finished.

Your pin positions can differ from the solution's. Your pin numbers and types cannot.

## If you get stuck

1. **The summary line shows a duplicate.** Two pins share a number. The table is sorted by
   number, so the pair sits on adjacent rows. Check both against the datasheet's HTSSOP column
   and correct the wrong one in its cell.
2. **Your five hand-placed pins disappeared after the import.** "Replace all existing pins" was
   selected. Cancel the Pin Table and import again with Append. If you had already pressed OK,
   place the five pins again (lecture 1.3).
3. **The Symbol Checker reports pins off the grid.** The grid was finer than 50 mil when they were
   placed. Set it to 50 mil and move each pin it names.
4. **Your symbol is not in the chooser.** Open "Preferences", "Manage Symbol Libraries..." and
   look for your library on the "Global Libraries" tab. If it is missing, add it there.

## Optional: a part of your own

Choose a part from your own work that no library has. Download its datasheet and author it in
the same library, by the same method. There is no worked solution: the datasheet is the answer
key. Hold it to the same acceptance list, with the datasheet's pin count in place of 17.

## When you are done

You have a library you will keep, a finished `DRV8833_PD` in it, and a filled record sheet. In
Module 2 the symbol gets its footprint, and in Module 6 it goes on a board.
