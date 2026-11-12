"""Render one PNG per lecture step from the executed notebook.

The images show the step title, the code cells and their text outputs, exactly
as stored in ``notebooks/day_72_data_exploration.ipynb``. Nothing is captured
from the desktop, so no GUI is driven on the host.

Usage: python tools/make_screenshots.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK = ROOT / "notebooks" / "day_72_data_exploration.ipynb"
OUTPUT = ROOT / "docs" / "images"
FONT_CANDIDATES = (
    "C:/Windows/Fonts/consola.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/System/Library/Fonts/Menlo.ttc",
)
BACKGROUND = (255, 255, 255)
CODE_BG = (243, 244, 246)
TITLE_BG = (30, 41, 59)
TITLE_FG = (255, 255, 255)
TEXT = (17, 24, 39)
PROMPT = (37, 99, 235)
PAD = 16
SIZE = 15


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Return a monospaced font, falling back to the Pillow default."""
    for candidate in FONT_CANDIDATES:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def read_steps() -> list[tuple[str, list[tuple[str, str]]]]:
    """Group the notebook cells by lecture step: title and (code, output) pairs."""
    cells = json.loads(NOTEBOOK.read_text(encoding="utf-8"))["cells"]
    steps: list[tuple[str, list[tuple[str, str]]]] = []
    for cell in cells:
        source = "".join(cell["source"])
        if cell["cell_type"] == "markdown":
            match = re.match(r"## (Step \d+: .+)", source)
            if match:
                steps.append((match.group(1), []))
            elif steps and (source.startswith("### ") or source.startswith("**Answer")):
                steps[-1][1].append((source.lstrip("# ").replace("**", ""), ""))
        elif cell["cell_type"] == "code" and steps:
            steps[-1][1].append((source, _output_text(cell)))
    return steps


def _output_text(cell: dict) -> str:
    parts: list[str] = []
    for output in cell.get("outputs", []):
        if output["output_type"] == "stream":
            parts.append("".join(output["text"]))
        elif "data" in output and "text/plain" in output["data"]:
            parts.append("".join(output["data"]["text/plain"]))
    return "\n".join(part.rstrip("\n") for part in parts)


def render(title: str, pairs: list[tuple[str, str]], target: Path) -> None:
    """Draw one step as a notebook-style image."""
    font = load_font(SIZE)
    bold = load_font(SIZE + 3)
    blocks: list[tuple[str, tuple[int, int, int], str]] = []
    for code, output in pairs:
        if code:
            blocks.append((code, CODE_BG, "In"))
        if output:
            blocks.append((output, BACKGROUND, "Out"))
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    line_height = SIZE + 6
    lines = [line for text, _, _ in blocks for line in text.splitlines()] or [""]
    width = int(max(probe.textlength(line, font=font) for line in lines)) + PAD * 2 + 60
    width = max(width, int(probe.textlength(title, font=bold)) + PAD * 2, 640)
    height = 44 + sum(len(text.splitlines()) * line_height + PAD for text, _, _ in blocks) + PAD
    image = Image.new("RGB", (width, height), BACKGROUND)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, 44), fill=TITLE_BG)
    draw.text((PAD, 11), title, font=bold, fill=TITLE_FG)
    y = 44
    for text, background, label in blocks:
        block_height = len(text.splitlines()) * line_height + PAD
        draw.rectangle((0, y, width, y + block_height), fill=background)
        draw.text((PAD // 2, y + PAD // 2), label, font=font, fill=PROMPT)
        for number, line in enumerate(text.splitlines()):
            draw.text((60, y + PAD // 2 + number * line_height), line, font=font, fill=TEXT)
        y += block_height
    target.parent.mkdir(parents=True, exist_ok=True)
    image.save(target)


def main() -> None:
    """Write docs/images/step-NN.png for every lecture step."""
    for title, pairs in read_steps():
        number = int(re.search(r"\d+", title).group())
        render(title, pairs, OUTPUT / f"step-{number:02d}.png")
        print(f"wrote step-{number:02d}.png: {title}")


if __name__ == "__main__":
    main()
