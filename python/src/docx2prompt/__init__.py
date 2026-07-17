"""docx2prompt: Word comments to AI-ready Markdown."""

from docx2prompt.core import (
    extraer_feedback,
    extract_comments_from_docx,
    vaciar_feedback,
    write_markdown_feedback,
)

__all__ = [
    "extraer_feedback",
    "extract_comments_from_docx",
    "vaciar_feedback",
    "write_markdown_feedback",
]
