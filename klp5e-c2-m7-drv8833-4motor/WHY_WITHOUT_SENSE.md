# Why build the board without sense resistors

A reference for the `without-sense` variant of the four-motor board, which Lecture 8.3 makes. The lecture says that the variant changes four parts from `0R2` to `0R` and points here for the reasons. This page carries them, with the datasheet's own lines and their page numbers. "DRV8833" means Texas Instruments SLVSAR1E (the file `datasheets/drv8833.pdf` in this project). The sense resistors are `R2`, `R3`, `R6` and `R7`: `R2` and `R3` serve stage one's bridges, `R6` and `R7` stage two's.

## 1. What `R2`, `R3`, `R6` and `R7` do

Each one sits between a bridge's `xISEN` pin and ground, and sets that bridge's chopping current:

`I = V_TRIP / R`

1. **The value.** With 0.2 Ω and a `V_TRIP` of 200 mV (typical), the bridge chops at about 1 A.
2. **The spread.** `V_TRIP` is 160 mV minimum, 200 mV typical and 240 mV maximum (DRV8833, p. 7), so with 0.2 Ω the limit lies anywhere between 0.8 A and 1.2 A.

## 2. Why a design limits current

The datasheet, p. 10, section 7.3.3:

> "For DC motors, current control is used to limit the start-up and stall current of the motor."

The default build does this. It is the right build for a motor whose stall current is near the limit or below it.

## 3. Why a build leaves the limit out

There are three reasons.

1. **The limit can cost torque.** A motor that needs more than about 1 A to start or to carry its load is held at the limit and loses torque, while the bridge itself is rated "1.5-A RMS, 2-A Peak per H-Bridge in PWP" (DRV8833, p. 1).
2. **The resistor costs power.** At 1 A each sense resistor drops 0.2 V and turns 0.2 W into heat.
3. **A small motor gains nothing.** A motor that never comes near 1 A gains nothing from the limit. This is the case the pin table means by "or GND if current control not needed" (p. 4), and p. 10 says: "If current control is not needed, the xISEN pins should be connected directly to ground."

## 4. What still protects the board

The datasheet, p. 11, section 7.3.5.1:

> "Overcurrent protection does not use the current sense circuitry used for PWM current control, so it functions even without presence of the xISEN resistors."

1. **Overcurrent protection.** It trips at 2 A or more (`I_OCP`: 2 A minimum, 3.3 A typical, p. 6). It disables that H-bridge only and drives `nFAULT` low. It retries after 1.35 ms (`t_OCP`, typical, p. 6).
2. **Thermal shutdown.** It acts at 150 °C or more (`T_TSD`, minimum, p. 6).

## 5. Why the link is 0 Ω and never DNP, and why 2 A in 1206

1. **0 Ω, not left off.** `AISEN` and `BISEN` are each bridge's path to ground. Leave the part off and that bridge has no return, so the motor does not turn. A 0 Ω link grounds the bridge and lets it draw whatever the motor asks for.
2. **2 A.** The link carries a whole bridge's current, 1.5 A continuous and 2 A peak. The Vishay `CRCW12060000Z0EA` is rated 2 A. The common 0603 jumper is rated 1 A, which is fine on a signal net but not here.
3. **1206.** The land on the board is 1206. A variant may change a footprint, but then it describes a second board, not a second build.

## 6. How to choose a build

1. Measure or look up the motor's stall current.
2. Order the default build when the stall current is near the limit or below it.
3. Order `without-sense` only when the stall current is above the limit and within the bridge's rating, remembering that the protection still trips at 2 A or more.
