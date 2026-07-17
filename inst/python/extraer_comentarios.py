#!/usr/bin/env python3
"""Shim legacy para el paquete R: delega en docx2prompt (default *.Rmd)."""

from __future__ import annotations

import sys
from pathlib import Path


def _bootstrap_path() -> None:
    here = Path(__file__).resolve()
    candidates = [
        here.parents[2] / "python" / "src",
        here.parents[1] / "python" / "src",
    ]
    for src in candidates:
        if (src / "docx2prompt").is_dir():
            p = str(src)
            if p not in sys.path:
                sys.path.insert(0, p)
            return


def main() -> int:
    _bootstrap_path()
    try:
        from docx2prompt.cli import main_legacy_script
    except ImportError:
        print(
            "Error: no se encontro el paquete docx2prompt. "
            "Instala con: pip install -e python/",
            file=sys.stderr,
        )
        return 1
    return main_legacy_script(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())
