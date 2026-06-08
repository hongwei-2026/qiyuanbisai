#!/usr/bin/env python3
"""Convert markdown report to PDF with Chinese text and embedded images."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from fpdf import FPDF

FONT = Path("C:/Windows/Fonts/simhei.ttf")
IMG_RE = re.compile(r"^!\[(.*?)\]\((.+?)\)\s*$")
CAPTION_RE = re.compile(r"^\*\*(图\d+[^*]*)\*\*\s*(.*)$")


class ReportPDF(FPDF):
    def footer(self):
        self.set_y(-12)
        self.set_font("hei", size=9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, f"第 {self.page_no()} 页", align="C")


def _clean(text: str) -> str:
    text = text.replace("**", "")
    for a, b in [("✅", "完成"), ("🔄", "进行"), ("⏳", "待办"), ("•", "-")]:
        text = text.replace(a, b)
    return text


def _mc(pdf: ReportPDF, h: float, text: str, size: int = 10, color=(30, 30, 30)) -> None:
    pdf.set_font("hei", size=size)
    pdf.set_text_color(*color)
    pdf.multi_cell(pdf.epw, h, _clean(text))


def _embed_image(pdf: ReportPDF, img_path: Path, caption: str = "") -> None:
    if not img_path.is_file():
        _mc(pdf, 6, f"[图片缺失: {img_path}]", color=(180, 0, 0))
        return
    max_w = pdf.epw
    max_h = 100
    pdf.ln(3)
    x = pdf.l_margin
    y = pdf.get_y()
    if y > 180:
        pdf.add_page()
        y = pdf.get_y()
    pdf.image(str(img_path), x=x, y=y, w=max_w)
    pdf.set_y(y + max_h + 2)
    if caption:
        _mc(pdf, 5, caption, size=9, color=(80, 80, 80))
    pdf.ln(3)


def write_line(pdf: ReportPDF, line: str, base_dir: Path) -> None:
    line = line.rstrip()
    if not line:
        pdf.ln(3)
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
        pdf.ln(8)
        _mc(pdf, 12, line[2:].strip(), size=20, color=(15, 15, 15))
        pdf.ln(4)
        return

    if line.startswith("## "):
        pdf.ln(5)
        _mc(pdf, 9, line[3:].strip(), size=15, color=(25, 25, 25))
        pdf.ln(2)
        return

    if line.startswith("### "):
        pdf.ln(3)
        _mc(pdf, 7, line[4:].strip(), size=12, color=(35, 35, 35))
        pdf.ln(1)
        return

    if line.startswith("> "):
        pdf.set_fill_color(245, 245, 245)
        _mc(pdf, 6, line[2:].strip(), size=9, color=(70, 70, 70))
        return

    if line.startswith("```"):
        return

    if line.strip() == "---":
        pdf.ln(2)
        pdf.set_draw_color(180, 180, 180)
        y = pdf.get_y()
        pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
        pdf.ln(5)
        return

    if line.startswith("|") and "---" not in line:
        _mc(pdf, 6, "  |  ".join(c.strip() for c in line.strip("|").split("|")), size=9)
        return

    if line.startswith("|") and "---" in line:
        return

    if line.startswith("- "):
        _mc(pdf, 6, "  - " + line[2:].strip())
        return

    if re.match(r"^\d+\.\s", line):
        _mc(pdf, 6, line.strip())
        return

    _mc(pdf, 6, line)


def convert(md_path: Path, out_path: Path) -> None:
    if not FONT.is_file():
        raise FileNotFoundError(f"Chinese font not found: {FONT}")

    base_dir = md_path.parent
    pdf = ReportPDF()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_left_margin(20)
    pdf.set_right_margin(20)
    pdf.add_page()
    pdf.add_font("hei", "", str(FONT))

    for line in md_path.read_text(encoding="utf-8").splitlines():
        write_line(pdf, line, base_dir)

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
