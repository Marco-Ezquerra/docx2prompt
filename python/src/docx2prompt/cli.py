"""CLI de docx2prompt."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from docx2prompt.core import extraer_feedback, vaciar_feedback


def _cmd_extract(args: argparse.Namespace) -> int:
    docx_path = Path(args.input_docx)
    if not docx_path.is_file():
        print(f"Error: no existe el documento: {docx_path}", file=sys.stderr)
        return 1

    md_path = Path(args.output)
    print(f"Analizando {docx_path}...")
    try:
        out = extraer_feedback(docx_path, md_path, source_glob=args.source_glob)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001
        print(f"Error procesando {docx_path}: {exc}", file=sys.stderr)
        return 1

    content = out.read_text(encoding="utf-8")
    n = content.count("- [ ] **Texto original:**")
    print(f"Listo: {n} instrucciones en {out}")
    if n == 0:
        print(
            "(Sin comentarios: abre el Word, usa Nuevo comentario, guarda y vuelve a ejecutar.)"
        )
    return 0


def _cmd_vaciar(args: argparse.Namespace) -> int:
    out = vaciar_feedback(args.output, source_glob=args.source_glob)
    print(f"Feedback vaciado: {out}")
    return 0


def _parse_extract_argv(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("input_docx")
    parser.add_argument("output_md", nargs="?", default=None)
    parser.add_argument("-o", "--output", dest="output_flag", default=None)
    parser.add_argument("--source-glob", default="*.qmd")
    args = parser.parse_args(argv)
    output = args.output_flag or args.output_md or "FEEDBACK.md"
    return argparse.Namespace(
        input_docx=args.input_docx,
        output=output,
        source_glob=args.source_glob,
    )


def main(argv: list[str] | None = None) -> int:
    argv = list(argv if argv is not None else sys.argv[1:])

    if not argv or argv[0] in ("-h", "--help"):
        print(
            "Uso:\n"
            "  docx2prompt extract INPUT.docx [-o FEEDBACK.md] [--source-glob '*.qmd']\n"
            "  docx2prompt vaciar [-o FEEDBACK.md] [--source-glob '*.qmd']\n"
            "  docx2prompt INPUT.docx [-o FEEDBACK.md] [--source-glob GLOB]\n"
        )
        return 0 if argv and argv[0] in ("-h", "--help") else 1

    if argv[0] == "extract":
        return _cmd_extract(_parse_extract_argv(argv[1:]))
    if argv[0] == "vaciar":
        parser = argparse.ArgumentParser(prog="docx2prompt vaciar")
        parser.add_argument("-o", "--output", default="FEEDBACK.md")
        parser.add_argument("--source-glob", default="*.qmd")
        return _cmd_vaciar(parser.parse_args(argv[1:]))

    return _cmd_extract(_parse_extract_argv(argv))


def main_legacy_script(argv: list[str] | None = None) -> int:
    """Entry point compatible con inst/python/extraer_comentarios.py (R fallback)."""
    argv = list(argv if argv is not None else sys.argv[1:])
    if not argv or argv[0] in ("-h", "--help"):
        print(
            "Uso: extraer_comentarios.py input.docx [output.md] "
            "[--source-glob GLOB]",
            file=sys.stderr,
        )
        return 0 if argv else 1

    ns = _parse_extract_argv(argv)
    if ns.source_glob == "*.qmd":
        ns.source_glob = "*.Rmd"
    return _cmd_extract(ns)
