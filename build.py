#!/usr/bin/env python3
"""Free Garage Sale Pack build script.

Renders every HTML sheet in src/ into a finished US-Letter PDF in
printables/ using WeasyPrint. Fully offline: no network, fonts from
local system files, no accounts or services.

Usage:
    python3 build.py            # build every sheet into printables/
    python3 build.py --list     # show what would build, then exit
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from weasyprint import HTML  # type: ignore
from pypdf import PdfReader  # type: ignore

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
OUT = ROOT / "printables"

# Every printable in the pack, in host-guide order. html paths are relative
# to src/; pdf names land in printables/.
SHEETS = [
    {
        "name": "01-pick-a-date-checklist",
        "html": "sheets/01-pick-a-date-checklist.html",
        "title": "Pick-a-Date Checklist",
    },
    {
        "name": "02-pricing-cards",
        "html": "sheets/02-pricing-cards.html",
        "title": "Pricing Cards (Default Tiers)",
    },
    {
        "name": "03-table-sort-labels",
        "html": "sheets/03-table-sort-labels.html",
        "title": "Per-Table Sort Labels",
    },
    {
        "name": "04-change-fund-worksheet",
        "html": "sheets/04-change-fund-worksheet.html",
        "title": "Change Fund Worksheet",
    },
    {
        "name": "05-layout-sketch-grid",
        "html": "sheets/05-layout-sketch-grid.html",
        "title": "Layout Sketch Grid",
    },
    {
        "name": "06-sale-day-signs",
        "html": "sheets/06-sale-day-signs.html",
        "title": "Sale-Day Signs (Big Fonts)",
    },
    {
        "name": "07-no-sold-today-fine",
        "html": "sheets/07-no-sold-today-fine.html",
        "title": "No-Sold-Today Fine Template",
    },
    {
        "name": "08-resale-lot-tally-log",
        "html": "sheets/08-resale-lot-tally-log.html",
        "title": "Resale-Lot Tally Log",
    },
    {
        "name": "host-guide",
        "html": "host-guide.html",
        "title": "Host Guide (Friend, Not Vendor)",
    },
]


def expected_pdf_name(sheet: dict) -> str:
    base = Path(sheet["html"]).stem
    return f"{base}.pdf"


def build_sheet(sheet: dict, out_dir: Path = OUT) -> Path:
    """Render one HTML sheet into out_dir and return the PDF path."""
    html_path = SRC / sheet["html"]
    if not html_path.is_file():
        raise FileNotFoundError(f"missing source: {html_path}")
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = out_dir / expected_pdf_name(sheet)
    HTML(filename=str(html_path)).write_pdf(str(pdf_path))
    return pdf_path


def verify_pdf(pdf_path: Path, min_pages: int = 1) -> int:
    """Open a generated PDF and return its page count (raises if invalid)."""
    reader = PdfReader(str(pdf_path))
    pages = len(reader.pages)
    if pages < min_pages:
        raise ValueError(f"{pdf_path.name}: expected >= {min_pages} pages, got {pages}")
    return pages


def build_all(out_dir: Path = OUT, quiet: bool = False) -> list[tuple[str, Path, int]]:
    results = []
    for sheet in SHEETS:
        pdf_path = build_sheet(sheet, out_dir)
        pages = verify_pdf(pdf_path)
        results.append((sheet["name"], pdf_path, pages))
        if not quiet:
            print(f"  built {pdf_path.relative_to(ROOT)}  ({pages} page{'s' if pages != 1 else ''})")
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the Free Garage Sale Pack PDFs (offline).")
    parser.add_argument("--out", type=Path, default=OUT, help="output directory (default: printables/)")
    parser.add_argument("--list", action="store_true", help="list the pack contents and exit")
    args = parser.parse_args(argv)

    if args.list:
        print("Free Garage Sale Pack — sheets:")
        for sheet in SHEETS:
            print(f"  {sheet['title']:<38} -> printables/{expected_pdf_name(sheet)}")
        return 0

    print(f"Building {len(SHEETS)} printables into {args.out} ...")
    results = build_all(args.out)
    total_pages = sum(p for _, _, p in results)
    print(f"Done: {len(results)} PDFs, {total_pages} pages total.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
