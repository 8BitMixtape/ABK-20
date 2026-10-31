# ABK-20 Software Suite

Firmware, sketches, and audio bootloader tools for the **ABK-20** (8Bit Mixtape MS-20 synthesizer variant).

---

## Hardware Pinout & Architecture (ATtiny85 @ 16 MHz PLL)

| ATtiny85 Pin | Port / Function | ABK-20 Hardware Connection |
|:---:|:---:|:---|
| **Pin 1** | `PB5` / `RESET` | Reset / ISP Pin / (Optional Key / Resistor ladder) |
| **Pin 2** | `PB3` / `ADC3` | **POT 2** (Left Potentiometer / CV In 2) |
| **Pin 3** | `PB4` / `ADC2` | **BUTTON 1** & **Audio Bootloader In** (Multiplexed via voltage divider) |
| **Pin 4** | `GND` | Ground |
| **Pin 5** | `PB0` / `OC0A` | **AUDIO OUT** (High-speed 8-bit PWM to 3.5mm Jack & Output Filter) |
| **Pin 6** | `PB1` / `DO` | **NEOPIXEL / BI-COLOR LED** (Addressable RGB LED / Status indicator) |
| **Pin 7** | `PB2` / `ADC1` | **POT 1** (Thumbwheel / Right Potentiometer / CV In 1) |
| **Pin 8** | `VCC` | +3.3V to +5V (USB-C power / Battery) |

Hardware pin definitions and helper macros are centralized in [`include/abk20_hardware.h`](include/abk20_hardware.h).

---

## Included Sketches (`src/`)

1. **`interface_test_AKB20.cpp`** *(Default)*
   - Comprehensive hardware test sketch.
   - Tests both analog potentiometers, button inputs, NeoPixel / LED feedback, and PWM audio output.
2. **`acid_AKB-20.cpp`**
   - 303-style acid bassline synthesizer and 16-step sequencer.
   - Interactive live parameter tweaking (cutoff, resonance, tempo, decay).
3. **`test_bicolor_led.cpp`**
   - Verification sketch for reverse-parallel bi-color LED circuits on `PB1`.

---

## Quickstart & Build Instructions

This project uses [PlatformIO](https://platformio.org/).

### 1. Select the Sketch
Open [`platformio.ini`](platformio.ini) and adjust the `build_src_filter` section so only one sketch is active:

```ini
build_src_filter =
    -<*>
    +<interface_test_AKB20.cpp>
    ;+<acid_AKB-20.cpp>
```

### 2. Compile
Run PlatformIO to compile the sketch:
```bash
pio run
```
The build system will automatically compile the sketch, verify it stays within the **6,300 byte flash limit** (preserving 1.7 KB for the bootloader), and convert `firmware.hex` into the audio bootloader file:
`.pio/build/attiny85/firmware.wav`

---

## Uploading to ABK-20 Hardware

### Method A: TinyAudioBoot (Audio Jack Upload)
1. Connect a 3.5mm stereo/mono audio cable from your computer or phone headphone jack to the **Audio In / Bootloader** jack of the ABK-20.
2. Set your playback device volume to **80% - 100%** (ensure all EQ, spatial audio, and bass boosts are turned OFF).
3. Power cycle the ABK-20 (or turn on power) to enter bootloader mode (status LED will pulse/blink rapidly).
4. Run:
   ```bash
   pio run --target upload
   ```
   *(Or manually play `.pio/build/attiny85/firmware.wav` using `aplay -q .pio/build/attiny85/firmware.wav` / your preferred media player).*
5. Upon successful audio transfer, the bootloader writes the flash and launches your sketch immediately.

---

## Bootloader Setup (ISP Flashing)

If you are assembling a new board or need to install/re-flash the bootloader, pre-compiled binaries are located in [`tools/bootloader/`](tools/bootloader/):

- **Recommended**: `tools/bootloader/TinyAudioBoot_skipper_16MHz.hex` (skips bootloader instantly on reset unless button is held).
- **Fuses**:
  - `lfuse`: `0xe1` (PLL internal 16MHz)
  - `hfuse`: `0xdd` (SPI enabled, BOD 2.7V)
  - `efuse`: `0xfe` (Self-programming enabled)

Refer to [`tools/bootloader/burn_bootloader.md`](tools/bootloader/burn_bootloader.md) for full `avrdude` commands.

