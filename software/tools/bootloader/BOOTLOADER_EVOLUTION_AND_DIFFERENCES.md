# TinyAudioBoot: Evolution & Differences to Original

This document details the architectural evolution, engineering challenges, and technical differences between the **original TinyAudioBoot** (v3.0–v3.2 by Iyok / ChrisMicro) and the **ABK-20 / 8Bit Mixtape Bootloader Suite** (v3.3 Standard & v4.0 Skipper by Marc Dusseiller & Antigravity).

---

## 1. Quick Comparison Matrix

| Feature | Original TinyAudioBoot (v3.2) | ABK-20 Standard Edition (v3.3) | ABK-20 Skipper Edition (v4.0) |
| :--- | :--- | :--- | :--- |
| **Power-On Startup** | Enters 5–7s bootloader on every power cycle | Enters 5s bootloader on every power cycle | **Instant boot ($< 25\text{ ms}$)**; runs sketch immediately |
| **Bootloader Trigger** | Automatic on power-on / reset | Automatic on power-on / reset | **Hold button `SW2`** during power-on |
| **Standby Upload Window** | Fixed 5–7 seconds | 5 seconds (Red blink @ 1 Hz) | **30 seconds** (relaxed window to press play) |
| **Speaker Audio on PB1** | ❌ **Loud 1 Hz clicking/pops** in speaker/phones |  **100% Silent** (`PB1` actively clamped to 0V) |  **100% Silent** (`PB1` actively clamped to 0V) |
| **PB3 Multiplexing Logic** | Simple CMOS digital logic (`PINB & (1<<PB3)`) | Digital audio input | **Internal 8-bit ADC Ladder Decoder** (`ADCH <= 60`) |
| **Button Debounce & Release**| None (contact bounce caused demodulator freeze)| N/A | **ADC release loop + 20ms settling delay** |
| **Visual Progress Feedback** | Single LED toggle | **Alternating Green $\leftrightarrow$ Red** per 64B page | **Alternating Green $\leftrightarrow$ Red** per 64B page |
| **Binary Footprint** | **1,006 bytes** (only 18B headroom before 1KB overflow) | **874 bytes** (-132B reduction) | **960 bytes** (includes ADC & debounce in < 1KB) |
| **Bootloader Flash Base** | **$0\text{x1C00}$** (1 KB boundary) | **$0\text{x1C00}$** (1 KB boundary) | **$0\text{x1C00}$** (1 KB boundary) |
| **Flash Left for Synthesizer**| **7,168 bytes** ($0\text{x0000} \to 0\text{x1BFF}$) | **7,168 bytes** ($0\text{x0000} \to 0\text{x1BFF}$) | **7,168 bytes** ($0\text{x0000} \to 0\text{x1BFF}$) |

---

## 2. In-Depth Engineering Solutions

### A. The "Silent Standby" Problem (Shared PB1 Pin)
* **The Problem in Original Bootloaders**:
  On pin-constrained ATtiny85 synthesizers (like the 8Bit Mixtape and ABK-20), `PB1` is shared between Timer 1 Audio PWM (`OC1A`) and the status LED. In earlier bootloaders, blinking the standby LED toggled `PB1`, sending a full-amplitude square wave into the PAM8002 audio amplifier. Users heard loud, irritating 1 Hz clicking or 7 Hz chirping in their headphones and internal speaker while waiting for audio to upload.
* **The ABK-20 Solution**:
  The bi-color LED circuit connects antiparallel between `PB1` and `PB0`:
  * During standby waiting, **`PB1` is held firmly at GND ($0\text{V}$)**.
  * Standby blinking pulls **`PB0` HIGH**, forward-biasing only the Red LED segment (`PB0` $\to$ `PB1` = GND).
  * Because `PB1` remains at DC ground, zero AC current flows into the audio amplifier. Standby is **100% silent**.

```c
// ABK-20 Silent Standby Pin Macros:
#define INITLED do { \
    DDRB |= (1 << PB0) | (1 << PB1); \
    PORTB &= ~((1 << PB0) | (1 << PB1)); /* PB1 & PB0 at GND */ \
} while(0)

#define TOGGLE_RED() do { PORTB &= ~(1 << PB1); PORTB ^= (1 << PB0); } while(0)
#define LEDOFF       do { PORTB &= ~((1 << PB0) | (1 << PB1)); } while(0)
```

---

### B. Analog Resistor Ladder vs. Digital CMOS Logic (PB3)
* **The Problem in Original Bootloaders**:
  Standard bootloader button detection relies on simple digital logic:
  ```c
  if ((PINB & (1 << PB3)) == 0) // Button pressed
  ```
  On the ABK-20, `PB3` is not a dedicated digital line. It serves a triple purpose:
  1. **Audio In**: AC-coupled through a 100 nF capacitor and biased to $V_{CC}/2 \approx 2.5\text{V}$.
  2. **Toggle Switch `SW3`**: Selects resistor ladder nodes.
  3. **Push Button `SW2`**: Pulls the ladder to lower resistance nodes.

  ATtiny85 CMOS digital inputs require $V_{IH} \ge 0.6 \times V_{CC} = 3.0\text{V}$ for a digital `1`, and $V_{IL} \le 0.3 \times V_{CC} = 1.5\text{V}$ for a digital `0`.
  The physical voltage levels on PB3 across all switch combinations are:

  | Switch Combination | PB3 Physical Voltage | 8-Bit ADC Reading (`ADCH`) | CMOS Digital State |
  | :--- | :---: | :---: | :---: |
  | **Idle (No button, Toggle neutral)** | **$2.63\text{V}$** | $\approx 134$ | **UNDEFINED (Floating)** |
  | **Toggle 1 DOWN alone** | **$1.72\text{V}$** | $\approx 88$ | **UNDEFINED (Floating)** |
  | **Toggle 2 UP alone** | **$1.29\text{V}$** | $\approx 66$ | Digital `0` (False positive!) |
  | **Button `SW2` pressed solo** | **$0.99\text{V}$** | $\approx 51$ | Digital `0` |
  | **Button `SW2` + Toggle 1 DOWN** | **$0.82\text{V}$** | $\approx 42$ | Digital `0` |
  | **Button `SW2` + Toggle 2 UP** | **$0.70\text{V}$** | $\approx 36$ | Digital `0` |

  *A digital check produces false positives on Toggle 2, hangs unpredictably, or floats.*

* **The ABK-20 Solution**:
  The Skipper bootloader activates the internal ADC (`ADC3` on PB3, left-adjusted for fast 8-bit reads from `ADCH`):
  $$\text{Threshold}: \quad \text{ADCH} \le 60 \quad (\approx 1.18\text{V})$$
  - Any condition where `SW2` is pressed produces $\text{ADCH} \le 51 \implies$ **Bootloader enters!**
  - Toggle 2 alone produces $\text{ADCH} = 66 > 60 \implies$ **Ignored! Normal instant boot.**
  - Idle produces $\text{ADCH} = 134 > 60 \implies$ **Ignored! Normal instant boot.**

---

### C. Contact Bounce & Demodulator Lockup
* **The Problem in Original Bootloaders**:
  When a user releases button `SW2`, mechanical micro-sparks create voltage transients on `PB3`. The Differential Manchester audio demodulator in TinyAudioBoot relies on edge transitions. It interpreted these mechanical contact bounces as an incoming audio carrier tone, broke out of the standby loop into `receiveFrame()`, timed out waiting for the rest of a non-existent packet, and threw an unrecoverable red blink error.
* **The ABK-20 Solution**:
  1. When `SW2` is pressed at power-on, the bootloader turns the **Red LED ON solid** as immediate visual confirmation.
  2. The ADC repeatedly polls `PB3` in a tight loop until it detects the physical release:
     ```c
     do {
       ADCSRA |= (1 << ADSC);
       while (ADCSRA & (1 << ADSC));
     } while (ADCH <= 60); // Wait until released
     ```
  3. A $20\text{ ms}$ electrical settling delay lets all line ringing decay.
  4. The ADC is powered down (`ADCSRA = 0`), completely freeing `PB3` to act as an AC-coupled audio input before the audio demodulator is armed.

---

### D. Real-Time Page-Write Bi-Color Visuals
* **The Problem in Original Bootloaders**:
  Earlier bootloaders used sporadic single-LED flashes or kept the LED solid, offering little insight into whether a 15-second audio stream was actually succeeding or failing mid-transfer.
* **The ABK-20 Solution**:
  The bootloader takes advantage of the antiparallel bi-color LED between `PB1` and `PB0`:
  ```c
  // In the page write handler:
  if (pageNumber & 1) {
    LED_RED();   // PB1 = LOW,  PB0 = HIGH
  } else {
    LED_GREEN(); // PB1 = HIGH, PB0 = LOW
  }
  ```
  On every 64-byte flash page successfully written, the LED toggles color. The user sees a crisp alternating **Green $\leftrightarrow$ Red** heartbeat throughout the audio upload.

---

### E. Flash Memory Budget & The 1 KB Boundary
* **The Baseline in Original Bootloader**:
  The original `TinyAudioBoot_LedPB0.hex` binary occupied **1,006 bytes** (`0x1C00` to `0x1FEE`). While it did fit within 1 KB, it left a razor-thin margin of **only 18 bytes** before overflowing into a 2 KB partition (`0x1800`).
* **The ABK-20 Challenge & Solution**:
  Adding the internal ADC peripheral setup, button ladder threshold checks, release polling loop, 20 ms electrical settling delay, and bi-color page alternating logic would have added $> 150$ bytes—blowing past the 1,024-byte ceiling and forcing a 2 KB boundary (which would have stolen 1,024 bytes of flash from user synth sketches).

  To prevent this, the C codebase was systematically refactored using lean `pgm_read_word` macros, register-level bit-ops, and unified compile-time flags:
  - **Standard Edition**: Compressed down to **874 bytes** (a 132-byte reduction from the 1,006-byte original).
  - **Skipper Edition**: Incorporates all ADC ladder decoding, button debouncing, and release loops in just **960 bytes**—preserving 64 bytes of headroom inside the 1 KB partition.
  
  Both editions preserve the full **7,168 bytes** ($0\text{x0000} \to 0\text{x1BFF}$) for user sketches without sacrifice.

---

## 3. Summary of Files

All bootloader artifacts are located in [`software/tools/bootloader/`](.):

* **`src/TinyAudioBoot.c`**: Unified single-source C implementation (compiled with or without `-DUSE_SKIPPER`).
* **`src/Makefile`**: Build script targeting ATtiny85 @ 16 MHz internal PLL.
* **`hex/TinyAudioBoot_Standard_ABK-20.hex`**: 874-byte production binary (5s auto-window).
* **`hex/TinyAudioBoot_Skipper_ABK-20.hex`**: 960-byte production binary (instant boot, SW2 entry).
* **`burn_bootloader.md`**: AVRDUDE one-liner commands and fuse configuration (`lfuse:0xe1`, `hfuse:0xdd`, `efuse:0xfe`).

