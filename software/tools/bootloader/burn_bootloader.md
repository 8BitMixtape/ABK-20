# Burning TinyAudioBoot onto ATtiny85 (ABK-20)

> **Important**: Always use the two-stage command (`&&` between flash and fuses). 
> When programming with ArduinoISP (`avrisp`), writing flash and fuses in a single command can glitch the clock switch before the session cleanly terminates.

---

### 1. Standard Bootloader (Always waits 5s for audio on power-on)
```bash
avrdude -v -p attiny85 -c avrisp -P /dev/ttyACM0 -b 19200 \
  -U flash:w:tools/bootloader/hex/TinyAudioBoot_Standard_ABK-20.hex:i && \
avrdude -P /dev/ttyACM0 -b 19200 -c avrisp -p t85 \
  -U efuse:w:0xfe:m -U hfuse:w:0xdd:m -U lfuse:w:0xe1:m
```

---

### 2. Skipper Bootloader (Instant Boot, enters bootloader ONLY when holding SW2)
```bash
avrdude -v -p attiny85 -c avrisp -P /dev/ttyACM0 -b 19200 \
  -U flash:w:tools/bootloader/hex/TinyAudioBoot_Skipper_ABK-20.hex:i && \
avrdude -P /dev/ttyACM0 -b 19200 -c avrisp -p t85 \
  -U efuse:w:0xfe:m -U hfuse:w:0xdd:m -U lfuse:w:0xe1:m
```
cd ..
---

### Fuse Values Reference (16MHz Internal PLL)
* **lfuse**: `0xe1` (16 MHz PLL system clock, 64 MHz PCK, fast startup)
* **hfuse**: `0xdd` (SPI enabled, BOD 2.7V, RESET enabled, SELFPROGEN enabled)
* **efuse**: `0xfe` (Self-programming enabled for bootloader SPM)
