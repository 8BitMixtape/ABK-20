# ABK-20 Hardware Architecture & Design Notes

## 1. Pin Assignment Summary (ATtiny85)

| Pin | Physical | Port | Function | Description |
| :--- | :--- | :--- | :--- | :--- |
| **PB0** | Pin 5 | `NEOPIXELPIN` | Digital Out | High-speed (800kHz) DIN to 20x NeoPixels (`NEO1`–`NEO20`) via R9 (330Ω); also drives Fader LED (`RV1B`) via R13 (1kΩ). |
| **PB1** | Pin 6 | `SPEAKERPIN` | PWM Audio Out | OC1A output (Timer1 high-speed PLL) filtered through R8 (330Ω) & C3 (100nF) to Volume Pot (`POT3-Vol1`). |
| **PB2** | Pin 7 | `POTI_LEFT` / `ADC1` | Analog In | Wiper of Slide Potentiometer (`RV1A`) via R7 (22kΩ). |
| **PB3** | Pin 2 | `BUTTON_PIN` / `ADC3` | Analog In / Audio In | Biased at VCC/2 (R1 & R2 22kΩ) for AC-coupled AudioBoot In (C1 100nF). Also reads the button resistor ladder. |
| **PB4** | Pin 3 | `POTI_RIGHT` / `ADC2`| Analog In | Wiper of Rotary Potentiometer (`POT2-CV1`) via R6 (22kΩ) and push button `SW4`. |
| **PB5** | Pin 1 | `RESET` / `GPIO` | Reset / Future I/O | Connected to `J6` (Sync Jumper). See Section 4 below for MIDI/GPIO expansion via `RSTDISBL`. |

---

## 2. Input Controls & Resistor Ladder (PB3)

The button network alters the DC bias on `PB3` (ADC3) to distinguish multiple inputs without interfering with AudioBoot:
* **Idle / Audio Bias**: $\sim 0.50 \times V_{CC}$ ($\sim 512$ ADC count)
* **Toggle Left** (`SW3` pin 1 via R3 22k): $\sim 0.33 \times V_{CC}$ ($\sim 341$ ADC count)
* **Toggle Right** (`SW3` pin 3 via R4||R5 11k): $\sim 0.25 \times V_{CC}$ ($\sim 256$ ADC count)
* **Push Button** (`SW2` via R16 6.8k): $\sim 0.19 \times V_{CC}$ ($\sim 195$ ADC count)

---

## 3. Slide Potentiometer with LED (Alpha RA2045F)

* **Symbol**: `mixtape_schematics:Potentiometer_Slide_LED` (multi-unit):
  * **Unit A**: 20mm slide potentiometer (Pins 1, 2, 3) mapped to `PB2/A1`.
  * **Unit B**: Lever-integrated LED (Pin 5 Anode, Pin 4 Cathode) mapped through R13 (1kΩ) to `PB0` for status/bootloader pulse activity.
* **PCB**: Merges into a single 5-pad footprint (`RV1`).

---

## 4. Future Implementation Note: PB5 (Pin 1) for MIDI IN / Sync

* **Context**: Pin 1 is configured by default as hardware `RESET`. Pulling it low (< ~2.5V) forces an immediate MCU reset.
* **Unlocking PB5 for MIDI / Digital Input**:
  * The ATtiny85 **`RSTDISBL`** fuse can be programmed to convert Pin 1 into a full GPIO pin with `PCINT5` (Pin Change Interrupt).
  * With `PCINT5` enabled, PB5 can run bit-banged Software UART to receive 31,250 baud MIDI serial (e.g. via optocoupler or 3.5mm TRS MIDI Type A/B).
* **Bootloader & Programming Implications**:
  * **AudioBoot Compatibility**: AudioBoot does **not** rely on the hardware reset pin; it activates on **Power-On Reset** (power switch cycle). Firmware uploads via audio remain 100% operational with `RSTDISBL` set.
  * **SPI ISP Limitation**: Disabling Reset locks out standard SPI in-system programmers (USBasp, Arduino as ISP). Recovery/fuse-clearing requires a 12V High-Voltage Serial Programmer (HVSP).
