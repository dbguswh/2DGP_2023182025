"""Drill #8: play four animations from the supplied sprite sheet."""

from pathlib import Path

from pico2d import close_canvas, load_image, open_canvas


SHEET_PATH = Path(__file__).with_name("sprite_sheet.png")


def main():
    open_canvas(800, 600)
    load_image(str(SHEET_PATH))
    close_canvas()


if __name__ == "__main__":
    main()
