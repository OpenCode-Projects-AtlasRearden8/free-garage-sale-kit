"""Tests for the Free Garage Sale Pack build.

By default these run against the committed PDFs in printables/ and, for the
build-itself checks, render sources into a temporary directory so the repo
stays clean. Fully offline; no network access anywhere.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from pypdf import PdfReader

import build as build_mod

ROOT = Path(build_mod.__file__).resolve().parent
SRC = ROOT / "src"
PRINTABLES = ROOT / "printables"


# --------------------------------------------------------------------------- #
# Source sanity: HTML + CSS must exist for every manifest sheet
# --------------------------------------------------------------------------- #

def test_every_sheet_has_a_source_file():
    for sheet in build_mod.SHEETS:
        assert (SRC / sheet["html"]).is_file(), f"missing source for {sheet['name']}"


def test_every_sheet_has_a_title():
    for sheet in build_mod.SHEETS:
        assert sheet.get("title", "").strip(), f"no title for {sheet['name']}"


def test_sources_are_offline_only():
    """'Nothing online': sources must not pull web fonts, images, or scripts."""
    offline_ok = re.compile(r"(https?:)?//", re.I)
    offenders = []
    for html in SRC.rglob("*.html"):
        body = html.read_text(encoding="utf-8")
        if offline_ok.search(body):
            offenders.append(html.name)
    assert offenders == [], f"sources reference remote URLs: {offenders}"


def test_sources_carry_no_branding():
    """PDFs must be unbranded: no credits, trademarks, or author credits."""
    forbidden = re.compile(r"(asdale|dynamics|dylan|github\.io|trademark|\b(tm)\b)", re.I)
    offenders = []
    for path in SRC.rglob("*.html"):
        body = path.read_text(encoding="utf-8")
        m = forbidden.search(body)
        if m:
            offenders.append((path.name, m.group(0)))
    assert offenders == [], f"branding leaked into printables sources: {offenders}"


# --------------------------------------------------------------------------- #
# Build evaluation: every sheet builds into a valid PDF
# --------------------------------------------------------------------------- #

@pytest.fixture(scope="module")
def built_pack(tmp_path_factory):
    out_dir = tmp_path_factory.mktemp("pack")
    results = build_mod.build_all(out_dir, quiet=True)
    return out_dir, results


def test_build_produces_every_sheet_in_manifest(built_pack):
    _, results = built_pack
    names = {name for name, _, _ in results}
    assert names == {sheet["name"] for sheet in build_mod.SHEETS}


def test_manifest_pdf_filenames_are_unique_and_prefixed(built_pack):
    _, results = built_pack
    pdf_names = sorted(path.name for _, path, _ in results)
    assert len(pdf_names) == len(set(pdf_names))
    for name in pdf_names:
        assert re.fullmatch(r"\d\d-.+\.pdf|host-guide\.pdf", name), name


@pytest.mark.parametrize(
    "sheet",
    build_mod.SHEETS,
    ids=[sheet["name"] for sheet in build_mod.SHEETS],
)
def test_every_sheet_builds_with_pages(built_pack, sheet):
    out_dir, _ = built_pack
    pdf_path = out_dir / build_mod.expected_pdf_name(sheet)
    assert pdf_path.is_file() and pdf_path.stat().st_size > 1_000
    assert build_mod.verify_pdf(pdf_path, min_pages=1) >= 1


def test_signs_sheet_has_at_least_two_pages(built_pack):
    _, results = built_pack
    pages = {name: n for name, _, n in results}
    assert pages["06-sale-day-signs"] >= 2


def test_prompts_and_rebuild_run_directory_is_stable(built_pack):
    """A second build into the same dir rewrites PDFs in place, no strain."""
    out_dir, _ = built_pack
    build_mod.build_all(out_dir, quiet=True)
    for sheet in build_mod.SHEETS:
        pdf_path = out_dir / build_mod.expected_pdf_name(sheet)
        assert pdf_path.is_file()
        read = PdfReader(str(pdf_path))
        assert len(read.pages) >= 1


# --------------------------------------------------------------------------- #
# Committed printables/ must exist and contain the manifest set
# --------------------------------------------------------------------------- #

def test_printables_folder_contains_built_pdfs():
    committed = {p.name for p in PRINTABLES.glob("*.pdf")}
    expected = {build_mod.expected_pdf_name(sheet) for sheet in build_mod.SHEETS}
    assert expected <= committed, f"printables/ missing: {sorted(expected - committed)}"


def test_printables_folder_has_no_extra_strays():
    committed = {p.name for p in PRINTABLES.glob("*.pdf")}
    expected = {build_mod.expected_pdf_name(sheet) for sheet in build_mod.SHEETS}
    strays = committed - expected
    assert strays == set(), f"unexpected files in printables/: {sorted(strays)}"


# --------------------------------------------------------------------------- #
# Repo hygiene for the pack itself
# --------------------------------------------------------------------------- #

def test_repo_has_license_and_readme():
    assert (ROOT / "LICENSE").is_file()
    assert (ROOT / "README.md").is_file()


def test_license_is_mit_with_company_line():
    text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert "MIT License" in text
    assert "Copyright (c) 2026 Asdale Dynamics, LLC" in text


def test_readme_credits_the_company():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "Asdale Dynamics, LLC" in text


def test_no_obvious_secrets_in_repo():
    forbidden = re.compile(
        r"(api[_-]?key|secret|password|token)\s*[:=]\s*\S", re.I
    )
    offenders = []
    for path in list(ROOT.rglob("*.py")) + list(SRC.rglob("*.html")) + [
        ROOT / "README.md",
        ROOT / "STATUS.md",
    ]:
        if not path.is_file():
            continue
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if forbidden.search(line):
                offenders.append(f"{path.relative_to(ROOT)}:{i}")
    assert offenders == [], f"possible secrets: {offenders}"
