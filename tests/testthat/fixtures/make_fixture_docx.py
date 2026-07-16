#!/usr/bin/env python3
"""Genera un .docx mínimo con comentarios nativos (fixture de tests).

Uso:
  python make_fixture_docx.py [salida.docx]
"""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"
REL = "http://schemas.openxmlformats.org/package/2006/relationships"
OFFICE_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def _document_xml() -> bytes:
    # Dos comentarios: id 0 sobre "alfa", id 1 sobre "beta gamma" (solapado simple)
    xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="{W}">
  <w:body>
    <w:p>
      <w:commentRangeStart w:id="0"/>
      <w:r><w:t>alfa</w:t></w:r>
      <w:commentRangeEnd w:id="0"/>
      <w:r><w:commentReference w:id="0"/></w:r>
      <w:r><w:t> </w:t></w:r>
      <w:commentRangeStart w:id="1"/>
      <w:r><w:t>beta</w:t></w:r>
      <w:r><w:t> gamma</w:t></w:r>
      <w:commentRangeEnd w:id="1"/>
      <w:r><w:commentReference w:id="1"/></w:r>
    </w:p>
  </w:body>
</w:document>
"""
    return xml.encode("utf-8")


def _comments_xml() -> bytes:
    xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:comments xmlns:w="{W}">
  <w:comment w:id="0" w:author="Tester" w:date="2026-01-01T00:00:00Z" w:initials="T">
    <w:p><w:r><w:t>Cambia alfa por alpha</w:t></w:r></w:p>
  </w:comment>
  <w:comment w:id="1" w:author="Tester" w:date="2026-01-01T00:00:00Z" w:initials="T">
    <w:p><w:r><w:t>Unifica beta gamma en una sola palabra</w:t></w:r></w:p>
  </w:comment>
</w:comments>
"""
    return xml.encode("utf-8")


def _content_types() -> bytes:
    xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="{CT}">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/comments.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml"/>
</Types>
"""
    return xml.encode("utf-8")


def _rels_root() -> bytes:
    xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="{REL}">
  <Relationship Id="rId1" Type="{OFFICE_REL}/officeDocument" Target="word/document.xml"/>
</Relationships>
"""
    return xml.encode("utf-8")


def _rels_document() -> bytes:
    xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="{REL}">
  <Relationship Id="rId1" Type="{OFFICE_REL}/comments" Target="comments.xml"/>
</Relationships>
"""
    return xml.encode("utf-8")


def make_fixture(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", _content_types())
        zf.writestr("_rels/.rels", _rels_root())
        zf.writestr("word/document.xml", _document_xml())
        zf.writestr("word/comments.xml", _comments_xml())
        zf.writestr("word/_rels/document.xml.rels", _rels_document())
    print(f"Fixture escrito: {path}")


def main() -> int:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("comentarios_minimos.docx")
    make_fixture(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
