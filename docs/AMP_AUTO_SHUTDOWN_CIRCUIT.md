# ABK-20 Hardware Design Proposal: Automatic Headphone Amp Shutdown

**Status**: Candidate for Next PCB Revision (v0.3+)  
**Author**: Antigravity & dusjagr  
**Target Subsystem**: Audio Amplifier (`U2` PAM8002 / 8002-family) & Audio Out Jack (`Jack2` PJ-317)  
**Associated Issues**: Idle battery current drain when using headphones, floating input noise.

---

## 1. Problem Statement (Current v0.2 Design)

In the current ABK-20 v0.2 hardware:
1. **Hardwired Enable**: The PAM8002 amplifier pin 1 (`SHT` / Shutdown) is tied directly to **GND** (permanently enabled).
2. **Audio Disconnect Only**: When headphones or an external patch cable are inserted into `Jack2`, the normalling switch (Pin 2 $\leftrightarrow$ Pin 4) mechanically disconnects the incoming audio line (`Sound_OUT`).
3. **Wasted Idle Power**: Even though no audio signal enters the amp, the PAM8002 stays fully powered:
   - Burns **$\approx 3.5\text{–}6\text{ mA}$ of continuous quiescent current** from the battery ($V_{CC}$).
   - Generates slight idle heat.
   - Leaves the high-gain input stage floating, which can pick up minor RF/switching hum.

---

## 2. The Solution: Jack-Controlled Autonomous Hardware Auto-Shutdown

By leveraging the **unused Ring switch contacts** already present inside the 5-pin 3.5mm stereo phone jack (`Jack2` PJ-317), the amplifier can enter **true low-power shutdown ($I_{SD} < 0.5\,\mu\text{A}$)** the instant a cable is plugged in, without requiring any MCU GPIO pins.

### Jack2 (PJ-317) Switch Topology:
* **Pin 1**: Sleeve (GND)
* **Pin 2**: Tip (Mono Audio Out from volume potentiometer `POT3-Vol1` wiper)
* **Pin 4**: Tip Normal switch (connected to Pin 2 when unplugged)
* **Pin 3**: Ring contact (**currently unconnected in v0.2**)
* **Pin 5**: Ring Normal switch (**currently unconnected in v0.2**)

Inside the jack, **Pin 5 is normally closed (NC) against Pin 3**:
* **Unplugged**: Pin 5 is mechanically shorted to Pin 3.
* **Plugged In**: Inserting any 3.5mm plug (TRS stereo or TS mono) lifts the spring blade, breaking the connection between Pin 5 and Pin 3.

---

## 3. Circuit Schematic

Only **one additional passive component** is required: a single **$100\text{k}\Omega$ pull-up resistor** (`R_SHT`, 0805 or 1206).

```
                  VCC (+5V)
                     │
                    [ ] R_SHT (100kΩ)
                     │
                     ├───────────────────► U2 (PAM8002) Pin 1 [SHT]
                     │
                 ┌───┴──────────┐
                 │  Pin 5 (RN)  │
                 │     o        │
                 │      \       │  Jack2 (PJ-317)
                 │       o      │
                 │  Pin 3 (Ring)│
                 └───┬──────────┘
                     │
                    GND
```

---

## 4. Operational Truth Table

| Physical State | Jack2 Switch (Pin 3 $\leftrightarrow$ Pin 5) | PAM8002 Pin 1 (`SHT`) Voltage | PAM8002 State | Quiescent Current ($I_Q$) | Audio Destination |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **No cable plugged in** | **CLOSED** (Connected) | **$0\text{V}$ (GND)** | **ACTIVE / ON** | $\approx 4\text{ mA}$ | **Internal Speaker (`Speaker1`)** |
| **Headphones / Cable Inserted** | **OPEN** (Broken) | **$V_{CC}$ ($+5\text{V}$)** | **SHUTDOWN** | **$< 0.5\,\mu\text{A}$** | **Headphones / External Jack (`Jack2`)** |

---

## 5. Engineering Benefits

1. **Battery Longevity**: When operating as a tabletop synth connected to headphones, speakers, or a recording interface, the internal power amplifier is completely shut down, extending battery life significantly.
2. **Zero Signal Crosstalk & Hiss**: Completely de-energizes the BTL output stages (`OUT+` and `OUT-`), eliminating any background switching noise, RF pickup, or battery ground bounce from bleeding into the headphone stream.
3. **Compatibility**:
   - **Stereo TRS Plugs**: Ring contact lifts Pin 5 away from Pin 3 $\rightarrow$ Pin 1 pulled high $\rightarrow$ Shutdown.
   - **Mono TS Eurorack / Guitar Plugs**: The long conductive sleeve grounds Pin 3, but the switch contact still mechanically opens $\rightarrow$ Pin 1 pulled high $\rightarrow$ Shutdown.
4. **Autonomous Hardware Operation**: Zero software overhead; operates without requiring any of the ATtiny85's scarce GPIO pins.

---

## 6. Implementation Guide for PCB Revision v0.3

### Schematic Changes (`hardware/ABK-20.kicad_sch`):
1. Disconnect `U2` Pin 1 from `GND`.
2. Add resistor `R19` (Value: `100k`, Footprint: `R_1206_HandSoldering` or `R_0805`).
   - Pin 1 of `R19` $\rightarrow$ `VCC`.
   - Pin 2 of `R19` $\rightarrow$ `U2` Pin 1 (`SHT`).
3. Connect `U2` Pin 1 to `Jack2` Pin 5 (`RN` / Ring Normal).
4. Connect `Jack2` Pin 3 (`R` / Ring) to `GND`.
5. Connect `Sound_OUT` directly to `U2` input capacitor `C5` (removing the need to route audio through the mechanical switch contact).

### Prototype Bodge Instructions (for v0.2 Boards):
1. Gently cut the small copper trace connecting `U2` Pin 1 to the ground plane.
2. Solder a $100\text{k}\Omega$ surface-mount or through-hole resistor between `U2` Pin 1 and `U2` Pin 6 ($V_{CC}$).
3. Solder a thin kynar/enamelled wire from `U2` Pin 1 to **`Jack2` Pin 5**.
4. Bridge a short wire from **`Jack2` Pin 3** to **GND** (e.g. `Jack2` Pin 1).
