"""Extraccion de comentarios Word (.docx) a Markdown para agentes."""

from __future__ import annotations

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
    """Devuelve lista de {original_text, instruction} en orden de aparicion."""
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
    source_glob: str = "*.qmd",
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


def extraer_feedback(
    docx_path: str | Path,
    output_md: str | Path = "FEEDBACK.md",
    source_glob: str = "*.qmd",
) -> Path:
    """Extrae comentarios Word a un checklist Markdown."""
    docx = Path(docx_path)
    if not docx.is_file():
        raise FileNotFoundError(f"No se encuentra el Word en: {docx}")

    out = Path(output_md)
    try:
        extracted = extract_comments_from_docx(docx)
    except zipfile.BadZipFile as exc:
        raise ValueError(f"No es un .docx valido: {docx}") from exc

    write_markdown_feedback(extracted, out, source_glob=source_glob)
    return out.resolve()


def vaciar_feedback(
    md_path: str | Path = "FEEDBACK.md",
    source_glob: str = "*.qmd",
) -> Path:
    """Sobrescribe el Markdown con una plantilla vacia."""
    out = Path(md_path)
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# Revisiones del documento - {stamp}",
        "",
        "> **PROMPT PARA CURSOR:**",
        "> Lee cada tarea de esta lista. Busca el fragmento exacto indicado en **Texto original**",
        f"> dentro de los archivos que coincidan con `{source_glob}` y aplica la **Instrucción**.",
        "> No alteres el resto del documento. Al terminar cada cambio, marca la casilla con una `x`.",
        "",
        "*Sin tareas pendientes. Ejecuta `docx2prompt` tras revisar el Word.*",
        "",
    ]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    return out.resolve()
