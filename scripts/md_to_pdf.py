#!/usr/bin/env python3
"""Convert markdown report to PDF with Chinese text and embedded images."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from fpdf import FPDF

try:
    from PIL import Image
except ImportError:
    Image = None  # type: ignore

FONT = Path("C:/Windows/Fonts/simhei.ttf")
IMG_RE = re.compile(r"^!\[(.*?)\]\((.+?)\)\s*$")
CAPTION_RE = re.compile(r"^\*\*(图\d+[^*]*)\*\*\s*(.*)$")


class ReportPDF(FPDF):
    def footer(self):
        self.set_y(-12)
        self.set_font("hei", size=9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, f"- {self.page_no()} -", align="C")


def _clean(text: str) -> str:
    text = text.replace("**", "")
    text = text.replace("−", "-").replace("–", "-").replace("—", "-")
    for a, b in [("✅", "[OK]"), ("🔄", "[进行中]"), ("⏳", "[待办]"), ("•", "-")]:
        text = text.replace(a, b)
    return text


def _mc(pdf: ReportPDF, h: float, text: str, size: int = 10, color=(30, 30, 30)) -> None:
    pdf.set_font("hei", size=size)
    pdf.set_text_color(*color)
    pdf.multi_cell(pdf.epw, h, _clean(text))


def _image_size(img_path: Path, max_w: float, max_h: float) -> tuple[float, float]:
    if Image is None:
        return max_w, max_h * 0.6
    with Image.open(img_path) as im:
        w, h = im.size
    ratio = h / w if w else 1.0
    dw = max_w
    dh = dw * ratio
    if dh > max_h:
        dh = max_h
        dw = dh / ratio if ratio else max_w
    return dw, dh


def _embed_image(pdf: ReportPDF, img_path: Path, caption: str = "") -> None:
    if not img_path.is_file():
        _mc(pdf, 6, f"[图片缺失: {img_path.name}]", color=(180, 0, 0))
        return

    dw, dh = _image_size(img_path, pdf.epw, 155)
    need = dh + (14 if caption else 6)
    if pdf.get_y() + need > pdf.h - pdf.b_margin:
        pdf.add_page()

    pdf.ln(2)
    x = pdf.l_margin
    y = pdf.get_y()
    pdf.image(str(img_path), x=x, y=y, w=dw, h=dh)
    pdf.set_y(y + dh + 2)
    if caption:
        _mc(pdf, 5, caption, size=9, color=(80, 80, 80))
    pdf.ln(4)


def write_line(pdf: ReportPDF, line: str, base_dir: Path, in_code: list[bool]) -> None:
    line = line.rstrip()

    if line.startswith("```"):
        in_code[0] = not in_code[0]
        if in_code[0]:
            pdf.ln(2)
            pdf.set_fill_color(248, 248, 248)
        else:
            pdf.ln(2)
        return

    if in_code[0]:
        if line:
            pdf.set_font("hei", size=8)
            pdf.set_text_color(40, 40, 40)
            pdf.set_fill_color(248, 248, 248)
            pdf.multi_cell(pdf.epw, 4.5, _clean(line), fill=True)
        return

    if not line:
        pdf.ln(2)
        return

    m_img = IMG_RE.match(line)
    if m_img:
        alt, rel = m_img.group(1), m_img.group(2)
        _embed_image(pdf, (base_dir / rel).resolve(), alt)
        return

    m_cap = CAPTION_RE.match(line)
    if m_cap:
        _mc(pdf, 5, f"{m_cap.group(1)} {m_cap.group(2)}".strip(), size=9, color=(80, 80, 80))
        return

    if line.startswith("# "):
        pdf.add_page()
        pdf.ln(4)
        _mc(pdf, 12, line[2:].strip(), size=18, color=(15, 15, 15))
        pdf.ln(3)
        return

    if line.startswith("## "):
        if pdf.get_y() > 240:
            pdf.add_page()
        pdf.ln(4)
        _mc(pdf, 9, line[3:].strip(), size=14, color=(25, 25, 25))
        pdf.ln(2)
        return

    if line.startswith("### "):
        pdf.ln(2)
        _mc(pdf, 7, line[4:].strip(), size=11, color=(35, 35, 35))
        pdf.ln(1)
        return

    if line.startswith("> "):
        _mc(pdf, 6, line[2:].strip(), size=9, color=(70, 70, 70))
        return

    if line.strip() == "---":
        pdf.ln(2)
        pdf.set_draw_color(200, 200, 200)
        y = pdf.get_y()
        pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
        pdf.ln(4)
        return

    if line.startswith("|") and "---" not in line:
        cells = [c.strip() for c in line.strip("|").split("|")]
        _mc(pdf, 5, " | ".join(cells), size=8)
        return

    if line.startswith("|") and "---" in line:
        return

    if line.startswith("- "):
        _mc(pdf, 5, "  * " + line[2:].strip())
        return

    if re.match(r"^\d+\.\s", line):
        _mc(pdf, 5, line.strip())
        return

    _mc(pdf, 5, line)


def convert(md_path: Path, out_path: Path) -> None:
    if not FONT.is_file():
        raise FileNotFoundError(f"Chinese font not found: {FONT}")

    base_dir = md_path.parent
    pdf = ReportPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.set_left_margin(18)
    pdf.set_right_margin(18)
    pdf.set_top_margin(16)
    pdf.add_page()
    pdf.add_font("hei", "", str(FONT))

    in_code = [False]
    for line in md_path.read_text(encoding="utf-8").splitlines():
        write_line(pdf, line, base_dir, in_code)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(out_path))


def main() -> None:
    p = argparse.ArgumentParser(description="Convert markdown report to PDF")
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    convert(args.input, args.output)
    print(f"Created {args.output}")


if __name__ == "__main__":
    main()
