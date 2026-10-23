# A3.1: Set up a power board

You have watched the stand-in board being set up in lectures 3.1 to 3.6, page by page. This
activity sets it up again, from the same start, with a values sheet that carries every number.
The values sheet does the remembering for you; putting each value in the right place, and
checking it, is yours.

Allow 45 to 60 minutes. Fill in `record-sheet.md` as you go.
This folder also holds `slides.html`, the lecture's slide deck, to open in a browser.

## What you start from

Download stage `00-start` from `github.com/futureshocked/KLP-5e-Course2-RealBoards`: it is the
folder `klp5e-c2-m3-standin-board/00-start`. It is the stand-in board, 42 × 30 mm, placed and
not routed, with KiCad's default setup. Close KiCad, copy the stage folder somewhere you will
keep it, then open its `klp5e-c2-m3-standin-board.kicad_pro` from the KiCad project manager.
Open the PCB editor from there.

## The ladder

Do the steps in this order. Each step names the lecture that shows it.

1. **The floor.** "File", "Board Setup...", "Constraints". Type the six floor values from the
   sheet. Leave "Minimum clearance" and "Minimum connection width" at 0 for now. (Lecture 3.1)
2. **Two classes and three patterns.** "Net Classes". Add `Power`, give it its four values, and
   move it above Default. Change Default's "Track Width" to 0.25. Under "Netclass Assignments"
   add the three patterns, each set to Power. Select each pattern's row and read the `Nets
   matching` list under it. Write each list on your record sheet the first time you read it,
   before you fix anything. (Lecture 3.2)
3. **The size menu.** "Pre-defined Sizes". Four track widths and two via sizes. Press "OK" and
   save the board. If you want to test a route, write down the width of your first track before
   you change anything, and delete the track afterwards. (Lecture 3.3)
4. **Power minimum width.** "Tools", "DRC Rule Editor". Type `routing` in the search box: "Routing
   width" is under "Highspeed design". Add a "Routing width" rule named `Power minimum width`,
   matching the Netclass Power, any layer, width 1.50 with a tolerance of 0.70. Read "Show
   Matches", then "Save". Open "File", "Board Setup...", "Custom Rules", write down the three
   numbers the rule wrote, and press "OK". (Lecture 3.4)
5. **U1 breakout width.** Back in "Tools", "DRC Rule Editor", add a second "Routing width" rule
   named `U1 fine-pitch breakout width`, "Where object matches:" "Custom Query", with the query on
   the sheet. Give it width 0.2 and tolerance 0, then read "Show Matches". Save, close the editor,
   and finish the rule as text on "Custom Rules" so that it reads `(min 0.2mm)` and nothing else.
   Write the rule's line before and after the edit. (Lecture 3.5)
6. **Two severities and the exemption.** "Violation Severity": set the two rows named on the
   sheet. "Constraints": give "Minimum connection width" its value. "Custom Rules": type rule 3
   below the other two, exactly as it is written below. Run the syntax check: it is the icon
   button under the text. Press "OK" and save the board. (Lecture 3.6)

## The values sheet

Every value in millimetres. Every value is the one the lectures use.

**Constraints (the floor)**

| Field | Value |
|---|---|
| Minimum track width | 0.127 |
| Minimum annular width | 0.09 |
| Minimum via diameter | 0.48 |
| Minimum drill size | 0.15 |
| Minimum text height | 0.762 |
| Minimum text thickness | 0.125 |
| Copper to hole clearance | 0.25 (already set) |
| Copper to edge clearance | 0.5 (already set) |
| Minimum clearance | 0 (leave) |
| Minimum connection width | 0.2 (set in step 6; 0 until then) |

**Net classes**

| Class | Clearance | Track Width | Via Size | Via Hole | Order |
|---|---|---|---|---|---|
| Default | 0.2 | 0.25 | 0.6 | 0.3 | below Power |
| Power | 0.3 | 1.5 | 0.8 | 0.4 | above Default |

Leave every other cell blank: it falls back to Default.

**Patterns, each set to Power**

| Pattern | Nets it should list |
|---|---|
| `*VM` | `/VM` |
| `*GND` | `GND` |
| `*OUT*` | `/AOUT1`, `/AOUT2`, `/BOUT1`, `/BOUT2` |

Each pattern starts with an asterisk, because a net's label arrives with its slash.

**Pre-defined Sizes**

| List | Sizes |
|---|---|
| Tracks | 0.25, 0.30, 0.80, 1.50 |
| Vias | 0.6 with a 0.3 hole, and 0.8 with a 0.4 hole |
| Differential pairs | none |

**Custom rules**

| Rule | Name | Built as | Ends as |
|---|---|---|---|
| 1 | `Power minimum width` | "Routing width", "Where object matches:" "Netclass" `Power`, Layer "Any", 1.50 with tolerance 0.70 | `(constraint track_width (min 0.8mm) (opt 1.5mm) (max 2.2mm))` |
| 2 | `U1 fine-pitch breakout width` | "Routing width", "Custom Query", 0.2 with tolerance 0 | `(constraint track_width (min 0.2mm))` |
| 3 | `Allow connector silk to intersect board edge` | typed on "Custom Rules" | the four lines below |

Rule 2's query:

```
A.NetName == '/AOUT*' || A.NetName == '/BOUT*' || A.NetName == '/VM'
```

Rule 3, typed below the other two:

```
(rule "Allow connector silk to intersect board edge"
	(constraint silk_clearance)
	(severity ignore)
	(condition "A.memberOfFootprint('J*') && B.Layer=='Edge.Cuts'")
)
```

**Violation Severity**

| Row | Setting |
|---|---|
| Footprint has no courtyard defined: | Warning (ships at Ignore) |
| Copper connection too narrow: | Error (ships at Warning) |

## Acceptance

Read this before you start, and check every line at the end.

- [ ] `*VM` lists `/VM`.
- [ ] `*GND` lists `GND`.
- [ ] `*OUT*` lists `/AOUT1`, `/AOUT2`, `/BOUT1` and `/BOUT2`.
- [ ] "Show Matches" reads 28 for rule 1 and 11 for rule 2.
- [ ] Rule 2 reads `(min 0.2mm)` and nothing else.
- [ ] The Custom Rules page holds three rules, the exemption last.
- [ ] The syntax check says "No errors found."

## Compare

The worked solution is stage `06-severity`, the end of lecture 3.6. Compare it page by page in
Board Setup, and compare its `.kicad_dru` with yours line by line. Rule names may differ. Numbers
and conditions may not.

## If you get stuck

1. **`Nets matching` is empty for a pattern.** The pattern lacks its leading asterisk. A
   net's label begins with a slash, so `VM` matches nothing and `*VM` matches `/VM`.
2. **The check says "Missing ')'".** A bracket went with the `opt` and `max` when you deleted
   them. The line must keep the constraint's closing bracket: `(constraint track_width (min 0.2mm))`.
3. **"Show Matches" reads 0.** The condition names the wrong class or net: check the class is
   `Power`, and that the query's net names carry their slash.

## Optional: a board of your own

Set up a board of your own, a Course 1 board is fine, for the currents it carries: the floor
from your fabricator's capability, a class for each kind of net, and a minimum-width rule for the
nets that carry current. There is no worked solution: your currents decide the numbers.

## When you are done

Module 4 starts from stage `07-routed`: this setup with the tracks already routed. Compare your setup with it before you start.
