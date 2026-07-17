"""Tests for docx2prompt core and CLI."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from docx2prompt.core import extraer_feedback, vaciar_feedback, write_markdown_feedback

FIXTURES = Path(__file__).parent / "fixtures"


def test_extract_fixture_comments():
    docx = FIXTURES / "comentarios_minimos.docx"
    out = FIXTURES / "_tmp_feedback.md"
    try:
        path = extraer_feedback(docx, out, source_glob="*.qmd")
        md = path.read_text(encoding="utf-8")
        assert "PROMPT PARA CURSOR" in md
        assert "*.qmd" in md
        assert "alfa" in md
        assert "Cambia alfa por alpha" in md
        assert "beta gamma" in md
    finally:
        if out.exists():
            out.unlink()


def test_extract_empty_docx():
    docx = FIXTURES / "sin_comentarios.docx"
    out = FIXTURES / "_tmp_empty.md"
    try:
        extraer_feedback(docx, out)
        md = out.read_text(encoding="utf-8")
        assert "No se encontraron comentarios" in md
    finally:
        if out.exists():
            out.unlink()


def test_extract_missing_docx():
    with pytest.raises(FileNotFoundError):
        extraer_feedback(FIXTURES / "no_existe.docx")


def test_vaciar_feedback():
    out = FIXTURES / "_tmp_vaciar.md"
    try:
        out.write_text("- [ ] tarea\n", encoding="utf-8")
        path = vaciar_feedback(out, source_glob="*.qmd")
        md = path.read_text(encoding="utf-8")
        assert "Sin tareas pendientes" in md
        assert "*.qmd" in md
        assert "- [ ] tarea" not in md
    finally:
        if out.exists():
            out.unlink()


def test_cli_module_extract():
    docx = FIXTURES / "comentarios_minimos.docx"
    out = FIXTURES / "_tmp_cli.md"
    try:
        cmd = [
            sys.executable,
            "-m",
            "docx2prompt",
            "extract",
            str(docx),
            "-o",
            str(out),
            "--source-glob",
            "*.qmd",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        assert result.returncode == 0
        assert out.exists()
        assert "*.qmd" in out.read_text(encoding="utf-8")
    finally:
        if out.exists():
            out.unlink()


def test_write_markdown_custom_glob():
    out = FIXTURES / "_tmp_glob.md"
    try:
        write_markdown_feedback([], out, source_glob="docs/**/*.qmd")
        assert "docs/**/*.qmd" in out.read_text(encoding="utf-8")
    finally:
        if out.exists():
            out.unlink()
