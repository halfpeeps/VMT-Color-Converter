# VMT Color Converter ($color to $color2)

A simple Python GUI tool to convert Source Engine `$color` (used on brushes) to `$color2` (used on models), using perceptual brightness correction to visually match the in-game appearance between shaders.

![Preview](https://files.perpheads.com/OgOZUYy36w6L14na.jpg)

## Interface Overview

- **R / G / B fields**: Enter brush color values (0–255)
- **Output Line**: `$color2` value ready to paste into a VMT
- **VMT Snippet**: Full `VertexLitGeneric` VMT block
- **Preview Swatch**: Shows final color as it will appear on models
- **Advanced Mode**: Allows you to edit the boost factor (affects brightness for converting between shaders)

---

### Requirements (for build)

- Python 3.10–3.12 (PyInstaller compatible)
- Tkinter (comes with Python)
- Run with:

```bash
pyinstaller --onefile --windowed --icon=vmt_color_converter.ico ^
    --add-data "vmt_color_converter.ico;." vmt_color_converter.py