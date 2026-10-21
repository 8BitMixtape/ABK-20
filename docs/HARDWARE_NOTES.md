# ABK-20 Hardware Architecture & Design Notes

## 1. Pin Assignment Summary (ATtiny85)

| Pin | Physical | Port | Function | Description |
| :--- | :--- | :--- | :--- | :--- |
| **PB0** | Pin 5 | `NEOPIXELPIN` | Digital Out | High-speed (800kHz) DIN to 20x NeoPixels (`NEO1`–`NEO20`) via R9 (330Ω); also drives Fader LED (`RV1B`) via R13 (1kΩ). |
| **PB1** | Pin 6 | `SPEAKERPIN` | PWM Audio Out | OC1A output (Timer1 high-speed PLL) filtered through R8 (330Ω) & C3 (100nF) to Volume Pot (`POT3-Vol1`). |
| **PB2** | Pin 7 | `POTI_LEFT` / `ADC1` | Analog In | Wiper of Slide Potentiometer (`RV1A`) via R7 (22kΩ). |
| **PB3** | Pin 2 | `BUTTON_PIN` / `ADC3` | Analog In / Audio In | Biased at VCC/2 (R1 & R2 22kΩ) for AC-coupled AudioBoot In (C1 100nF). Also reads the button resistor ladder. |
| **PB4** | Pin 3 | `POTI_RIGHT` / `ADC2`| Analog In | Wiper of 10kΩ Rotary Potentiometer (`POT2-CV1`) via R6 (22kΩ). |
| **PB5** | Pin 1 | `RESET` / `GPIO` | Reset / Future I/O | Connected to Reset push button (`SW4`) and `J6` (Sync Jumper). See Section 4 below for MIDI/GPIO expansion via `RSTDISBL`. |

---

## 2. Input Controls & Resistor Ladder (PB3)

The button network alters the DC bias on `PB3` (ADC3) to distinguish multiple inputs without interfering with AudioBoot:
* **Idle / Audio Bias**: $\sim 0.50 \times V_{CC}$ ($\sim 512$ ADC count)
* **Toggle Left** (`SW3` pin 1 via R3 22k): $\sim 0.33 \times V_{CC}$ ($\sim 341$ ADC count)
* **Toggle Right** (`SW3` pin 3 via R4||R5 11k): $\sim 0.25 \times V_{CC}$ ($\sim 256$ ADC count)
* **Push Button** (`SW2` via R16 6.8k): $\sim 0.19 \times V_{CC}$ ($\sim 195$ ADC count)

---

## 3. Slide Potentiometer with LED (Bourns PTL20 / Alpha RA2045F)

* **Symbol**: `mixtape_schematics:Potentiometer_Slide_LED` (multi-unit):
  * **Unit A**: 20mm slide potentiometer (Pins 1, 2, 3) mapped to `PB2/A1`.
  * **Unit B**: Lever-integrated LED (Pin 5 Anode, Pin 4 Cathode) mapped through R13 (1kΩ) to `PB0` for status/bootloader pulse activity.
* **Footprint**: `8Bitmixtape_reworked:Potentiometer_Bourns_PTL20_Single_Slide_LED` (or compatible 5-pad slide pot `RV1`).

---

## 4. Future Implementation Note: PB5 (Pin 1) for MIDI IN / Sync

* **Context**: Pin 1 is configured by default as hardware `RESET`. Pulling it low (< ~2.5V) forces an immediate MCU reset.
* **Unlocking PB5 for MIDI / Digital Input**:
  * The ATtiny85 **`RSTDISBL`** fuse can be programmed to convert Pin 1 into a full GPIO pin with `PCINT5` (Pin Change Interrupt).
  * With `PCINT5` enabled, PB5 can run bit-banged Software UART to receive 31,250 baud MIDI serial (e.g. via optocoupler or 3.5mm TRS MIDI Type A/B).
* **Bootloader & Programming Implications**:
  * **AudioBoot Compatibility**: AudioBoot does **not** rely on the hardware reset pin; it activates on **Power-On Reset** (power switch cycle). Firmware uploads via audio remain 100% operational with `RSTDISBL` set.
  * **SPI ISP Limitation**: Disabling Reset locks out standard SPI in-system programmers (USBasp, Arduino as ISP). Recovery/fuse-clearing requires a 12V High-Voltage Serial Programmer (HVSP).

---

## 5. Power Architecture & Diode OR-ing

* **Multi-Source Inputs**:
  * **USB-C 5V** (`VBUS` on `J5`): 6-pin Type-C receptacle (GCT USB4125 compatible). Includes **two 5.1kΩ pull-down resistors** (`R17` on `CC1`, `R18` on `CC2`) to GND, ensuring immediate 5V VBUS delivery from modern USB-PD sources, smart chargers, and MacBook Type-C ports.
  * **DC In** (7–12V regulated to 5V via 7805 `U3`)
  * **Battery** (3x AAA or 2x AAA / LiPo via `BT1/BT2` or `J4`)
* **Diode Isolation**:
  * **`D1` (SS14)**: Protects 7805 regulator output from back-driving.
  * **`D2` (SS14)**: Protects USB port from external voltage back-feed.
  * **`D3` (SS14)**: Protects batteries from being reverse-charged by 5V USB. Automatically shuts off battery drain when USB is connected.
* **Master Power Switch (`SW1`)**:
  * Latching push switch (`Push_SWITCH_hole` / `SW_SPST`) placed between combined diode cathodes and `VCC`.
  * Cycling `SW1` (OFF then ON) provides the exact power-cycle timing required to activate the **AudioBoot** bootloader on demand.

---

## 6. PCB Layout & Decoupling Placement Rules

When routing the PCB, place capacitors according to the following strict proximity rules:
1. **`C2` (100nF ceramic)**: Place **immediately touching** ATtiny85 Pin 8 (`VCC`) and Pin 4 (`GND`) ($\le 3\text{ mm}$) to supply high-speed clock/PLL switching pulses.
2. **`C4` (10µF)**: Place near ATtiny85 ($\le 10\text{ mm}$) as a local energy reservoir.
3. **`C8` (100nF ceramic)**: Place **directly bridging** PAM8002 Pin 6 (`VCC`) and Pin 7 (`GND`) ($\le 3\text{ mm}$) to block high-frequency digital noise from the audio amp.
4. **`C7` (220µF bulk electrolytic)**: Place near the PAM8002 / speaker block ($\le 20\text{ mm}$) to buffer low-frequency bass current spikes.


---

## 7. PAM8002 Audio Amplifier Optimization

* **Unity Gain ($A_v = 1.0$)**:
  * The PAM8002 is configured as a Bridge-Tied Load (BTL) amplifier. Its closed-loop gain is defined by $A_v = 2 	imes rac{R_F}{R_I}$.
  * With internal feedback resistor $R_F pprox 20	ext{ k}\Omega$ and external input resistor $R_{14} = 22	ext{ k}\Omega$:
    $$A_v pprox 2 	imes rac{20	ext{ k}\Omega}{22	ext{ k}\Omega} pprox 1.8	ext{ to }1.0$$
  * This matches the filtered 0–5V 8-bit PWM line output from the ATtiny85 RC network (`R8 = 330Ω`, `C3 = 100nF`) and volume pot (`POT3-Vol1`), preventing clipping and speaker distortion while maximizing headroom.
* **Low-Frequency Audio Coupling**:
  * Input capacitor `C5 = 1µF` forms a high-pass filter with $R_{14} = 22	ext{ k}\Omega$:
    $$f_c = rac{1}{2 \pi R_{14} C_5} = rac{1}{2 \pi 	imes 22000 	imes 10^{-6}} pprox 7.2	ext{ Hz}$$
  * This preserves the full sub-bass and low-frequency bytebeat rumble down to single-digit frequencies.
* **Power Supply Decoupling**:
  * Dedicated high-frequency ceramic bypass capacitor `C8 = 100nF` placed right across PAM8002 Pin 6 (`VCC`) and Pin 7 (`GND`) to suppress digital switching buzz.

---

## 8. Headphone Jack Auto-Shutdown Upgrade (Planned for v0.3)

* In v0.2, the PAM8002 Pin 1 (`SHT`) is hardwired to GND, drawing $4\text{–}6\text{ mA}$ idle even when headphones are plugged in.
* For revision v0.3, the spare Ring switch contacts on `Jack2` (Pins 3 & 5) combined with a $100\text{k}\Omega$ pull-up resistor enable **autonomous hardware auto-shutdown ($< 0.5\,\mu\text{A}$)** whenever a 3.5mm plug is inserted.
* Detailed schematic, operational truth table, and prototype bodge instructions are documented in [AMP_AUTO_SHUTDOWN_CIRCUIT.md](AMP_AUTO_SHUTDOWN_CIRCUIT.md).

---

## 9. Star Grounding & Audio Isolation (Planned for v0.3)

* **The Problem (Common-Impedance Ground Coupling)**:
  * In v0.2, the return currents from the 20× NeoPixels switch at their internal $\sim 1.2\text{ kHz}$ PWM frequency through the shared ground copper plane back to the USB-C port.
  * Because `POT3-Vol1` ground, `Jack2` ground, and `C3` ground are tapped along this same path, the $1.2\text{ kHz}$ switching current creates an audible AC voltage drop across the ground plane ($V = I \cdot R_{gnd}$) that is directly audible in headphones at Volume = 0.
* **The v0.3 Architecture**:
  * **Dedicated Analog Audio Ground Trace**: Give the entire audio chain (`POT3-Vol1` pin 3, `Jack2` pin 1, `C3` ground, `U2` pin 7, and `C6` bypass) its own isolated star-ground trace that routes directly back to the USB-C ground entry (`J5` pins A12/B12).
  * **Digital / Matrix Ground Separation**: All 20 NeoPixel ground pins return on a separate digital copper pour, completely preventing heavy LED PWM current from flowing under or through the audio path.

---

## 10. PB3 Analog Resistor Ladder Calibration (Buttons & Toggle Switch)

Pin PB3 (ADC3) multiplexes the navigation buttons and toggle switch through an analog resistor divider.

### Hardware Measurements & Calibration Table (at $V_{CC} \approx 5.0\text{V}$)

| Control State | Measured Voltage | Nominal ADC (10-bit) | Recommended Detection Range |
| :--- | :---: | :---: | :---: |
| **Idle / Released** (Center toggle, no button) | $2.62\text{ V}$ | $\approx 536$ | $> 450$ |
| **Toggle Switch Physical UP** | $1.36\text{ V}$ | $\approx 278$ | $240\text{ -- }310$ |
| **Toggle Switch Physical DOWN** | $1.74\text{ V}$ | $\approx 356$ | $320\text{ -- }420$ |
| **Button 3 (SW4) Pressed Solo** | $1.00\text{ V}$ | $\approx 205$ | $185\text{ -- }235$ |
| **Button 3 (SW4) + Toggle Physical UP** | $0.72\text{ V}$ | $\approx 147$ | $< 155$ |
| **Button 3 (SW4) + Toggle Physical DOWN** | $0.83\text{ V}$ | $\approx 170$ | $155\text{ -- }180$ |

> [!NOTE]
> On standard SPDT toggle switches (e.g. MTS-102), the internal contact pivots opposite the lever arm: flipping the lever physically UP connects the middle contact to the bottom PCB pin ($1.36\text{V}$), while flipping DOWN connects to the top pin ($1.74\text{V}$). All states provide non-overlapping windows of $30\text{--}60$ ADC counts.

---

## 11. Potentiometer & Slide Fader Calibration (4.7k Series Resistor)

Both analog inputs have a $4.7\text{k}\Omega$ series resistor in line with $V_{CC}$, restricting the wiper sweep to $\frac{10\text{k}}{10\text{k} + 4.7\text{k}} \times V_{CC} \approx 0.68 \times V_{CC}$ (ADC counts $\approx 15\text{--}670$).

### Polarity & Scaling

| Control | Pin | Physical Sweep | Raw ADC Range | Polarity | Scaling Math ($0\text{--}255$) |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **Rotary Pot** (`POT2-CV1`) | `PB4` / `ADC2` | CCW (Min) $\to$ CW (Max) | $670 \to 15$ | **Inverted** | `val = ((670 - raw) * 100) >> 8` |
| **Slide Fader** (`RV1`) | `PB2` / `ADC1` | DOWN (Min) $\to$ UP (Max) | $15 \to 670$ | **Direct** | `val = ((raw - 15) * 100) >> 8` |



