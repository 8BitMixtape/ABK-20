# ABK-20

**ABK-20** is a complete interface redesign of the **8Bit Mixtape**, featuring an expressive array of **20 addressable NeoPixels (RGB LEDs)** and an optimized audio circuit around the ATtiny85 microcontroller.

Still based on the 8Bit Mixtape philosophy—lo-fi algorithmic bytebeats, synth engines, and audio programming via the AudioBoot bootloader—but with expanded visual feedback and an updated physical layout.

---

## Key Hardware Features

* **Microcontroller**: Microchip ATtiny85 (16 MHz internal PLL)
* **Visual Matrix**: 20x WS2812B / SK6812 RGB NeoPixels
* **Audio Synthesis**: 8-bit PWM algorithmic synthesis engine
* **Audio Interface**: 3.5mm stereo output jack (line-out / headphones)
* **Bootloader**: AudioBoot (flash new sound sketches directly through audio cable or web browser)
* **Controls**:
  * Dual analog potentiometers (pitch, modulation, filter, rate)
  * Tactile control button(s) / touch contacts
* **Power**: USB-C (5V power rail for high-brightness NeoPixels) / battery input option
* **EDA Tool**: Designed in **KiCad 9**

---

## Compatible Firmware & Web Flasher

ABK-20 is fully compatible with the sound sketches and web player in:
* **[8Bit-Vintage Firmware Repository](https://github.com/8BitMixtape/8Bit-Vintage)**
* **[Web Audio Player & Flasher](https://8bitmixtape.github.io/8Bit-Vintage/)**

---

## Repository Structure

```
hardware/       KiCad 9 schematic (.kicad_sch), PCB layout (.kicad_pcb), and project files
libraries/      Custom KiCad symbols and footprints
production/     Fabrication deliverables
  gerbers/      Ready-to-order Gerbers and drill files
  bom/          Bill of Materials and component sourcing
docs/           Schematic exports (PDF), 3D renders, and hardware documentation
```

---

## License

Open Source Hardware (OSHW). See [LICENSE](LICENSE) for details.
