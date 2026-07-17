# docx2prompt (Python)

Paquete Python instalable para extraer comentarios Word a Markdown, orientado a **Quarto** (`*.qmd` por defecto).

## Instalacion

```bash
pip install -e python/
# o desde GitHub:
pip install "git+https://github.com/Marco-Ezquerra/docx2prompt.git#subdirectory=python"
```

## Uso

### API

```python
from docx2prompt import extraer_feedback, vaciar_feedback

extraer_feedback("informe.docx", output_md="FEEDBACK.md", source_glob="*.qmd")
vaciar_feedback(source_glob="*.qmd")
```

### CLI

```bash
docx2prompt extract informe.docx -o FEEDBACK.md --source-glob "*.qmd"
docx2prompt vaciar -o FEEDBACK.md --source-glob "*.qmd"
# atajo sin subcomando:
docx2prompt informe.docx -o FEEDBACK.md
```

### Quarto

```bash
quarto render informe.qmd --to docx
docx2prompt extract informe.docx --source-glob "*.qmd"
```

## Desarrollo

```bash
cd python
pip install -e ".[dev]"
pytest
```

## R vs Python

| Canal | Default `source_glob` |
|-------|----------------------|
| Python / Quarto | `*.qmd` |
| Paquete R | `*.Rmd` |

En ambos casos puedes pasar `source_glob` explicitamente.
