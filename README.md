# Free Garage Sale Pack

A free, printable pack for a smooth garage or yard sale — pick a date, price
your items, sort your tables, run the cash box, and keep a clean tally of what
sold. Eight practical printables plus a friendly host guide, all built from
plain HTML/CSS into unbranded PDFs by one local script.

Made by **Asdale Dynamics, LLC** — beginner-friendly, local-first tools that
explain things like a friend would. Part of the free printables/toolkits line;
see [dylanasdale.github.io](https://dylanasdale.github.io) for more plain-English guides.

## What's inside

| PDF (in `printables/`) | What it's for |
| --- | --- |
| `01-pick-a-date-checklist.pdf` | Choose a sale date, then a three-week prep checklist |
| `02-pricing-cards.pdf` | Cut-out price cards with sensible default tiers ($1–$15, free, offer, half-off) |
| `03-table-sort-labels.pdf` | Per-table sort labels so buyers sort themselves (+ blank labels) |
| `04-change-fund-worksheet.pdf` | Count a starting change fund and settle the cash box at close |
| `05-layout-sketch-grid.pdf` | 1 ft × 1 ft grid for sketching your table layout before setup |
| `06-sale-day-signs.pdf` | Big-font main sign, direction arrows, and half-off posters |
| `07-no-sold-today-fine.pdf` | A friendly "nothing sold today" fine template + quiet-table postmortem |
| `08-resale-lot-tally-log.pdf` | A tally log that folds into resale-lot-style records for online reselling |
| `host-guide.pdf` | The friendly how-to companion for the whole pack |

All PDFs are **unbranded** — no logos, credit lines, or links — so they slide
straight into whatever else you use.

## How to use (no computer skills required)

1. **Already got PDFs?** Just open the files in `printables/` and print on US
   Letter at **100% / "Actual size"**. That's it.
2. Start with `host-guide.pdf` — it explains every sheet in about two minutes.
3. Everything is pen-and-paper friendly: fill in, cut on dashed lines, tape up.

## How to build it yourself

The PDFs are generated on your machine and never touch the internet.

```bash
# one-time setup (WeasyPrint does the rendering; pypdf verifies the output)
python3 -m pip install weasyprint pypdf

# build every sheet into printables/
python3 build.py

# see the sheet list
python3 build.py --list

# verify every sheet builds into a valid PDF
python3 -m pytest
```

Generating HTML to PDF with WeasyPrint is a classic local build: no accounts,
no services, no model calls, nothing phoned home. Edit any sheet in `src/sheets/`,
re-run `python3 build.py`, and your updated PDF lands in `printables/`.

## Test coverage

`tests/test_build.py` verifies:

- every sheet in the build manifest has an HTML source and a title;
- sources contain **no remote URLs** (offline guarantee);
- sources contain **no branding** (PDFs stay unbranded);
- **every sheet builds** into a valid multi-page PDF in a temp directory;
- the committed `printables/` folder matches the manifest exactly (no strays);
- the `LICENSE` is MIT with the correct copyright line, and the README credits
  **Asdale Dynamics, LLC**;
- no obvious secrets anywhere in the repo.

## Customizing

Sheets are ordinary HTML/CSS in `src/sheets/` with a shared print stylesheet in
`src/styles/common.css`. Change prices, add a table label, add a whole page —
then rebuild. The build script auto-detects page counts and validates each PDF.

## For whom

Written warmly and plainly for first-time hosts: paperwork-organizer style,
ADHD-friendly structure (small checklists, one job at a time), and a resale
bridge for folks who eventually list what didn't sell online. Education and
organization only — nothing here is financial, legal, or career advice.

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Asdale Dynamics, LLC.
The PDFs are unbranded and free to print, reuse, and share.
