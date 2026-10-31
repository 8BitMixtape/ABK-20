# TinyAudioBoot for ATtiny85 (8Bit Mixtape & ABK-20)

**TinyAudioBoot** is an ultra-compact ($\approx 1\text{ KB}$) audio bootloader for the Microchip ATtiny85 microcontroller. It allows uploading compiled firmware sketches directly through a standard 3.5mm headphone jack or web browser via `.wav` audio streams—**no USB-to-Serial converter or dedicated ISP programmer required**.

---

## 1. Lineage & Project Links

* **Original AudioBoot** (ATmega8 / ATmega168): Created by [Chris Haberer (ChrisMicro)](https://github.com/radioelfe/audioboot).
* **TinyAudioBoot for ATtiny85**: Ported and adapted by [Budi Prakosa (Iyok / sensorium)](https://github.com/sensorium/TinyAudioBoot) with the Differential Manchester demodulator and [Hex2Wav](https://github.com/sensorium/Hex2Wav).
* **Web Audio Uploader**: WebAudio implementation by [Fredrik Olofsson](https://github.com/f0/TinyAudioBoot).
* **8Bit Mixtape & ABK-20 Extensions (v3.3 / v4.0)**: Developed by [Marc Dusseiller (dusjagr)](https://github.com/8BitMixtape/8Bit-Vintage) & Antigravity pair programming:
  * Silent speaker standby on PB1
  * Alternating Green $\leftrightarrow$ Red bi-color LED progress on every 64-byte page
  * Analog ladder Skipper on PB3 (ADC-based SW2 detection, button release wait, 20ms debounce)
  * Standardized 1KB bootloader section at `0x1C00` (leaving 7,168 bytes for user sketches)
  * Configurable upload windows (5s for Standard, 30s for Skipper)

---

## 2. Directory Structure

```
tools/bootloader/
├── README.md                                  # Complete technical architecture & user guide
├── burn_bootloader.md                         # Quick one-liner AVRDUDE flash commands
├── src/
│   ├── TinyAudioBoot.c                        # Unified C source (Standard & Skipper modes)
│   ├── TinyAudioBoot_skipper.c                # Synchronized reference source
│   ├── EEPROM.h                               # EEPROM support routines
│   └── Makefile                               # AVR-GCC build script (targets ATtiny85 @ 16MHz)
└── hex/
    ├── TinyAudioBoot_Standard_ABK-20.hex      # Standard 5s bootloader (874 bytes)
    └── TinyAudioBoot_Skipper_ABK-20.hex       # Skipper 30s bootloader (960 bytes)
```

---

## 3. The Two Bootloader Editions

| Feature | Standard Edition (`TinyAudioBoot_Standard_ABK-20`) | Skipper Edition (`TinyAudioBoot_Skipper_ABK-20`) |
| :--- | :--- | :--- |
| **Power-On Behavior** | Always enters bootloader on every power cycle/reset | Skips bootloader in $< 25\text{ ms}$; runs sketch immediately |
| **Bootloader Trigger** | Automatic on power-on or reset | Hold button **`SW2`** during power-on |
| **Standby Upload Window** | **5 seconds** (Red LED blinks @ 1 Hz, then sketch runs) | **30 seconds** (Red LED blinks @ 1 Hz, then sketch runs) |
| **Speaker Audio on PB1** | **Completely Silent** (PB1 grounded at 0V) | **Completely Silent** (PB1 grounded at 0V) |
| **Programming Visuals** | Alternates **Green $\leftrightarrow$ Red** on every 64-byte page | Alternates **Green $\leftrightarrow$ Red** on every 64-byte page |
| **Code Size** | **874 bytes** ($\le 1\text{ KB}$ at `0x1C00`) | **960 bytes** ($\le 1\text{ KB}$ at `0x1C00`) |
| **Flash Free for Sketch** | **7,168 bytes** ($0\text{x0000} \to 0\text{x1BFF}$) | **7,168 bytes** ($0\text{x0000} \to 0\text{x1BFF}$) |

---

## 4. Technical Architecture & Engineering Solutions

### A. The Shared Speaker & LED Pin Solution (Silent Standby)
On pin-constrained ATtiny85 synthesizers (like the 8Bit Mixtape and ABK-20):
* `PB1` is shared between Timer 1 Audio PWM (`OC1A`) and the bi-color LED anode.
* `PB0` drives the NeoPixel data line and the bi-color LED cathode.

In older bootloaders, toggling `PB1` to flash an indicator LED caused unpleasant audio clicks/chirps in the speaker or headphones at 1 Hz or 7 Hz. 

**The Solution**:
In both new bootloaders:
* During standby waiting, **`PB1` is held firmly at GND ($0\text{V}$)**.
* Status blinking toggles **`PB0` HIGH**, lighting only the Red LED segment without passing any AC audio current through the speaker.
* Result: **Absolute silence** on headphones/speaker during standby!

### B. Analog Resistor Ladder vs. Digital CMOS Logic (PB3)
Standard ATtiny85 boards use a digital push-button that connects a pin directly to GND. On the ABK-20:
* Pin `PB3` is shared between the AC-coupled audio input (biased at $V_{CC}/2 \approx 2.5\text{V}$) and a 5-position resistor ladder connected to Toggle Switch `SW1` and Button `SW2`.
* Digital CMOS input buffers on ATtiny85 require $V_{IH} \ge 0.6 \times V_{CC} = 3.0\text{V}$ to register HIGH. The idle ladder voltage sits at $2.63\text{V}$, Toggle 1 DOWN sits at $1.72\text{V}$, and Toggle 2 UP sits at $1.29\text{V}$. None of these reach $3.0\text{V}$!
* A conventional digital check `while ((PINB & (1 << PB3)) == 0)` hangs permanently on power-on because PB3 never reaches $3.0\text{V}$.

**The Solution**:
The Skipper bootloader activates the internal 8-bit ADC (`ADC3` / `ADCH` with left-adjusted output):
* **Button SW2 Solo**: pulls PB3 to $\approx 0.99\text{V}$ ($\text{ADCH} \approx 51$).
* **Button SW2 + Toggle 1/2**: pulls PB3 to $0.70\text{V}\text{--}0.82\text{V}$ ($\text{ADCH} \approx 36\text{--}42$).
* **Toggle 2 alone**: sits at $1.29\text{V}$ ($\text{ADCH} \approx 66$).
* **Idle (no button)**: sits at $2.63\text{V}$ ($\text{ADCH} \approx 134$).

By evaluating the calibrated threshold **`ADCH <= 60`** ($< 1.18\text{V}$), the bootloader cleanly detects button `SW2` press while remaining immune to all toggle switch positions and idle noise.

### C. Switch Bounce & ADC Button Release Detection
When releasing `SW2`, mechanical contact bounce produces voltage transitions on `PB3`. Without release filtering, the edge detector in the audio demodulator mistakes these contact bounces for audio carrier tones, prematurely breaking into the frame decoder and locking up.

**The Solution**:
1. When SW2 is detected, the bootloader turns the **Red LED ON solid** as immediate user feedback.
2. The ADC repeatedly polls PB3 in a loop until the voltage rises above $1.18\text{V}$ (`ADCH > 60`), confirming `SW2` has been physically released.
3. A 20 ms settling delay lets all electrical transients decay.
4. The ADC is powered down (`ADCSRA = 0`), cleanly releasing `PB3` to function as an AC-coupled audio input.

### D. Dynamic Green $\leftrightarrow$ Red Page Write Visuals
During audio programming, the bi-color LED sits antiparallel between `PB1` and `PB0`:
* Even 64-byte flash pages drive `PB1=HIGH, PB0=LOW` (Green).
* Odd 64-byte flash pages drive `PB1=LOW, PB0=HIGH` (Red).
* The user receives rhythmic alternating Green $\leftrightarrow$ Red flashing throughout the transfer, providing unmistakable visual confirmation of successful data reception.

### E. Flash Memory Budget & Addressing (`0x1C00`)
* **Bootloader Start Address**: `0x1C00` (byte address $7,168$).
* **Total ATtiny85 Flash**: $8,192$ bytes.
* **Bootloader Size**: Standard = 874 bytes, Skipper = 960 bytes (both $< 1,024$ bytes).
* **User Application Space**: $7,168$ bytes ($0\text{x0000} \to 0\text{x1BFF}$).
* **Safe Sketch Budget**: $\le 6,300$ bytes (recommended in `platformio.ini`).

---

## 5. ATtiny85 Fuse Configuration

To operate the ATtiny85 at $16\text{ MHz}$ using the internal 64 MHz high-speed PLL and enable self-programming:

| Fuse | Value | Setting & Purpose |
| :--- | :---: | :--- |
| **Low Fuse** (`lfuse`) | `0xE1` | 64 MHz PLL internal clock ($\to 16\text{ MHz}$ CPU clock), `CKDIV8` disabled. |
| **High Fuse** (`hfuse`) | `0xDD` | `SELFPROGEN` enabled (allows bootloader flash writes), Brown-out Detection (BOD) at $2.7\text{V}$, SPI enabled. |
| **Extended Fuse** (`efuse`) | `0xFE` | Self-programming target page protection enabled. |

---

## 6. How to Flash the Bootloaders via AVRDUDE

> [!IMPORTANT]
> Always execute AVRDUDE in **two stages** (`flash && fuses`). When programming with ArduinoISP (`avrisp`), combining flash write and fuse programming into a single command can desynchronize the SPI clock when the chip resets.

### Flash Standard Bootloader (5s timeout):
```bash
avrdude -v -p attiny85 -c avrisp -P /dev/ttyACM0 -b 19200 \
  -U flash:w:tools/bootloader/hex/TinyAudioBoot_Standard_ABK-20.hex:i && \
avrdude -P /dev/ttyACM0 -b 19200 -c avrisp -p t85 \
  -U efuse:w:0xfe:m -U hfuse:w:0xdd:m -U lfuse:w:0xe1:m
```

### Flash Skipper Bootloader (SW2 entry, 30s timeout):
```bash
avrdude -v -p attiny85 -c avrisp -P /dev/ttyACM0 -b 19200 \
  -U flash:w:tools/bootloader/hex/TinyAudioBoot_Skipper_ABK-20.hex:i && \
avrdude -P /dev/ttyACM0 -b 19200 -c avrisp -p t85 \
  -U efuse:w:0xfe:m -U hfuse:w:0xdd:m -U lfuse:w:0xe1:m
```

---

## 7. How to Compile from Source

From the `tools/bootloader/src` directory:

```bash
cd tools/bootloader/src
make clean
make
```

The Makefile compiles both hex targets from `TinyAudioBoot.c`:
1. `TinyAudioBoot_Standard_ABK-20.hex` (without `-DUSE_SKIPPER`)
2. `TinyAudioBoot_Skipper_ABK-20.hex` (with `-DUSE_SKIPPER`)

Convenience flash commands in Makefile:
```bash
make flash_standard   # Flash standard edition
make flash_skipper    # Flash skipper edition
```
