# ABK-20 Audio Flasher WAVs (`docs/wav/`)

This directory contains pre-rendered 44.1 kHz 16-bit PCM `.wav` audio tracks for the [ABK-20 Web Flasher](../index.html).

### How to generate new WAV tracks:
When compiling firmware sketches in `software/`:
```bash
pio run
```
The post-build script automatically runs `hex2wav` to produce `.pio/build/attiny85/firmware.wav`.
Copy and rename the `.wav` to this directory:
```bash
cp software/.pio/build/attiny85/firmware.wav docs/wav/<sketch_name>.wav
```
