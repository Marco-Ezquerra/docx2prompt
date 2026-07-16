#!/usr/bin/env python3
"""Extrae comentarios nativos de Word (.docx) a Markdown para agentes (Cursor).

Uso:
  python extraer_comentarios.py input.docx [output.md]
  python extraer_comentarios.py input.docx -o FEEDBACK.md --source-glob "*.Rmd"
  python extraer_comentarios.py --help
"""

from __future__ import annotations

import argparse
import sys
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W_NS}


def _w_tag(local: str) -> str:
    return f"{{{W_NS}}}{local}"


def _w_attr(elem: ET.Element, name: str) -> str | None:
    return elem.attrib.get(_w_tag(name))


def _normalize_text(text: str) -> str:
    return " ".join(text.split())


def _escape_backticks(text: str) -> str:
    return text.replace("`", "'")


def extract_comments_from_docx(docx_path: Path) -> list[dict[str, str]]:
    """Devuelve lista de {original_text, instruction} en orden de aparición."""
    comments_dict: dict[str, str] = {}

    with zipfile.ZipFile(docx_path, "r") as docx_zip:
        names = docx_zip.namelist()
        if "word/comments.xml" not in names:
            return []

        comments_xml = docx_zip.read("word/comments.xml")
        root = ET.fromstring(comments_xml)
        for comment in root.findall(".//w:comment", NS):
            c_id = _w_attr(comment, "id")
            if c_id is None:
                continue
            parts = [t.text for t in comment.findall(".//w:t", NS) if t.text]
            comments_dict[c_id] = "".join(parts)

        if not comments_dict:
            return []

        if "word/document.xml" not in names:
            raise FileNotFoundError("El .docx no contiene word/document.xml")

        document_xml = docx_zip.read("word/document.xml")
        doc_root = ET.fromstring(document_xml)

        # Stack: lista de (id, buffer_list) para rangos anidados/solapados
        active: list[tuple[str, list[str]]] = []
        results: list[dict[str, str]] = []

        for elem in doc_root.iter():
            tag = elem.tag
            if tag == _w_tag("commentRangeStart"):
                c_id = _w_attr(elem, "id")
                if c_id is not None:
                    active.append((c_id, []))
            elif tag == _w_tag("t") and active:
                if elem.text:
                    for _, buf in active:
                        buf.append(elem.text)
            elif tag == _w_tag("commentRangeEnd"):
                end_id = _w_attr(elem, "id")
                if end_id is None:
                    continue
                for i in range(len(active) - 1, -1, -1):
                    if active[i][0] == end_id:
                        c_id, buf = active.pop(i)
                        original = _normalize_text("".join(buf))
                        instruction = comments_dict.get(c_id, "").strip()
                        if original and instruction:
                            results.append(
                                {
                                    "original_text": original,
                                    "instruction": instruction,
                                }
                            )
                        break

        return results


def write_markdown_feedback(
    comments: list[dict[str, str]],
    output_path: Path,
    source_glob: str = "*.Rmd",
) -> None:
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# Revisiones del documento - {stamp}",
        "",
        "> **PROMPT PARA CURSOR:**",
        "> Lee cada tarea de esta lista. Busca el fragmento exacto indicado en **Texto original**",
        f"> dentro de los archivos que coincidan con `{source_glob}` y aplica la **Instrucción**.",
        "> No alteres el resto del documento. Al terminar cada cambio, marca la casilla con una `x`.",
        "",
    ]

    if not comments:
        lines.append("*No se encontraron comentarios en el documento Word.*")
        lines.append("")
    else:
        for c in comments:
            original = _escape_backticks(c["original_text"])
            lines.append(f"- [ ] **Texto original:** `{original}`")
            lines.append(f"      **Instrucción:** {c['instruction']}")
            lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Extrae comentarios nativos de Word (.docx) a Markdown "
            "optimizado para agentes (FEEDBACK.md)."
        )
    )
    parser.add_argument(
        "input_docx",
        help="Ruta al .docx con comentarios nativos de Word",
    )
    parser.add_argument(
        "output_md",
        nargs="?",
        default=None,
        help="Ruta del Markdown resultante (default: FEEDBACK.md)",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_flag",
        default=None,
        help="Alias de output_md",
    )
    parser.add_argument(
        "--source-glob",
        default="*.Rmd",
        help='Glob de fuentes .Rmd para el prompt (default: "*.Rmd")',
    )
    args = parser.parse_args(argv)

    docx_path = Path(args.input_docx)
    if args.output_flag:
        md_path = Path(args.output_flag)
    elif args.output_md:
        md_path = Path(args.output_md)
    else:
        md_path = Path("FEEDBACK.md")

    if not docx_path.is_file():
        print(f"Error: no existe el documento: {docx_path}", file=sys.stderr)
        return 1

    print(f"Analizando {docx_path}...")
    try:
        extracted = extract_comments_from_docx(docx_path)
    except zipfile.BadZipFile:
        print(f"Error: no es un .docx válido: {docx_path}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001 — CLI: mensaje claro y exit
        print(f"Error procesando {docx_path}: {exc}", file=sys.stderr)
        return 1

    write_markdown_feedback(extracted, md_path, source_glob=args.source_glob)
    print(f"Listo: {len(extracted)} instrucciones en {md_path}")
    if not extracted:
        print(
            "(Sin comentarios: abre el Word, usa Nuevo comentario, guarda y vuelve a ejecutar.)"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
