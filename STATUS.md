# STATUS.md — Free Garage Sale Pack

Last updated: 2026-10-28

## What was built

A complete, free printable pack for running a garage or yard sale, from
plain HTML/CSS sources to finished unbranded US-Letter PDFs:

1. **Pick-a-date checklist** — candidate-date comparison table plus
   three-weeks/two-weeks/week-of/night-before/sale-morning checklists.
2. **Pricing cards** — cut-out cards in sensible default tiers
   ($1 / $2–$3 / $5–$15, free, "make an offer", per-item clothing rates,
   half-off-cards for the last two hours).
3. **Per-table sort labels** — 12 fold-over category labels (kitchen, books,
   kids toys, clothes, tools, electronics, free box, pay here…) plus six
   blank labels; second page.
4. **Change-fund worksheet** — starting-cash denomination sheet (suggested
   ~$60 fund), money-handling rules, mid-day drawer log, and a closing
   reconciliation table that cross-checks the tally log.
5. **Layout-sketch grid** — 1 ft × 1 ft sketch grid with a setup checklist
   (driveway arrow, cash-box X, big-item marker, parking).
6. **Sale-day signs, big fonts** — main GARAGE SALE sign with fill-in
   date/time/address, two direction arrow signs, and large half-off /
   every-must-go posters; 3 pages.
7. **No-sold-today fine template** — friendly novelty fine notice (iced tea
   payable) for items that never sold, plus a "quiet tables" postmortem page
   that feeds the next year's plan.
8. **Resale-lot tally log** — one-line-per-lot tally (lot #, table, item,
   asked, sold, paid-by, notes) with totals, plus a mapping table showing how
   each column folds into resale-lot-style records for online reselling.
9. **Host guide** — friendly, plain-English companion PDF: what's in the
   pack, how many copies to print, printing tips, and a sale-day rhythm.

Infrastructure:

- `build.py` — **one build script**; renders every sheet with WeasyPrint
  into `printables/`, verifies each PDF with pypdf, prints a page-count
  summary. Supports `--list` and a custom `--out` directory.
- `src/styles/common.css` — shared print stylesheet (`@page` Letter,
  checkboxes, ruled tables, fill-in lines); sources use system fonts only.
- `tests/test_build.py` — 23 tests (pytest).
- `README.md`, `LICENSE` (MIT, Copyright (c) 2026 Asdale Dynamics, LLC).

## How to run it

```bash
python3 build.py        # build all 9 PDFs into printables/ (fully offline)
python3 build.py --list # show manifest
python3 -m pip install weasyprint pypdf   # only if not already installed
python3 -m pytest tests # run the test suite
```

Print from `printables/` at **100% / Actual size**, US Letter.

## Verification results (2026-10-28)

- `python3 build.py` — **pass**: 9 PDFs, 19 pages total, all pages verified by
  pypdf (`01`–`08` each 2 pages, `06-sale-day-signs` 3 pages, host guide 2 pages).
- `python3 -m pytest` — **23/23 pass**, covering:
  - manifest ↔ sources ↔ committed `printables/` completeness (no strays);
  - every sheet builds and yields ≥1 valid page (temp-dir builds, parametrized);
  - offline guarantee (no remote URLs in any HTML source);
  - unbranded guarantee (no branding tokens in sources);
  - LICENSE is MIT with the exact required copyright line; README credits
    Asdale Dynamics, LLC;
  - no obvious secrets in repo files.
- Visual spot-checks rendered each PDF at 60 dpi and corrected layout/typo
  issues found there (signed-line cramping, sign fill widths, sketch-grid
  column alignment, tier-note text).

## Known gaps / future ideas

- Signs use US Letter only; an A4 variant of the styles is not yet provided.
- No CSV/export path for the tally log (it is designed to be keyed into your
  own resale spreadsheet; an optional export script could be added later).
- Pricing tiers assume US-dollar, US-market defaults; a blank-priced card
  set for other price scales would be a small follow-up.
- No dark-mode or screen-preview page; PDFs are the single source of truth.
- The host guide is a 2-page PDF only; a longer HTML tips page could be added.

Local-first and quiet by design: **nothing online, nothing published, no
secrets, no personal data** in the repo.
