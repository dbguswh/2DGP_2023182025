"""Rebuild the compact transparent sheet from the original supplied PNG.

This is a one-time asset preparation step; animation_viewer.py itself only
needs pico2d. Run this script with Pillow installed if the derived PNG is lost.
"""

from pathlib import Path

from PIL import Image


FOLDER = Path(__file__).parent
SOURCE = FOLDER / "spirtesheet.png"
TARGET = FOLDER / "sprite_sheet.png"
USED_HEIGHT = 2138


def main() -> None:
    with Image.open(SOURCE) as source:
        if source.mode != "P" or source.width != 3840 or source.height < USED_HEIGHT:
            raise ValueError("The supplied sprite sheet has an unexpected format or size")

        palette = source.getpalette()
        alpha = bytearray([255] * 256)
        original_alpha = source.info.get("transparency")
        if isinstance(original_alpha, int):
            alpha[original_alpha] = 0
        elif isinstance(original_alpha, bytes):
            alpha[:len(original_alpha)] = original_alpha

        magenta_indices = [
            index for index in range(256)
            if palette[index * 3:index * 3 + 3] == [255, 0, 255]
        ]
        if not magenta_indices:
            raise ValueError("No magenta background found in the sprite sheet")
        for index in magenta_indices:
            alpha[index] = 0

        source.crop((0, 0, source.width, USED_HEIGHT)).save(
            TARGET, transparency=bytes(alpha), optimize=True,
        )


if __name__ == "__main__":
    main()
