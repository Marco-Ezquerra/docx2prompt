# docx2prompt

Extrae comentarios nativos de Word (`.docx`) a Markdown listo para agentes de IA
(p. ej. Cursor). Esta pensado para informes redactados en **R Markdown (`.Rmd`)**:
el agente aplica las instrucciones sobre esos fuentes. No requiere bookdown;
`book/` es solo un ejemplo si organizas los Rmd en una carpeta.

## Requisitos

- R >= 4.1
- Python >= 3.8 en el PATH (o variable `DOCX2PROMPT_PYTHON` con la ruta al ejecutable)

No hace falta instalar paquetes Python: el extractor usa solo la biblioteca estandar.

## Instalacion

```r
# install.packages("remotes")
remotes::install_github("Marco-Ezquerra/docx2prompt")
```

En desarrollo (clon del repo):

```r
devtools::load_all()
```

## Flujo de uso

1. Revisa el informe exportado a Word y deja **comentarios nativos** sobre el texto.
2. Extrae el feedback a Markdown.
3. Abre el `.md` en Cursor y pide aplicar las tareas sobre los `.Rmd` fuente.
4. Cuando termines, vacia el feedback para la siguiente iteracion.

```r
library(docx2prompt)

extraer_feedback("informe_comentado.docx")
# → FEEDBACK.md (prompt por defecto: *.Rmd)

# Si usas bookdown u otra carpeta de fuentes:
extraer_feedback(
  "informe_comentado.docx",
  output_md = "revisiones.md",
  source_glob = "book/*.Rmd"
)

# Tras aplicar las correcciones con el agente:
vaciar_feedback()
```

Ayuda en R: `?docx2prompt`, `?extraer_feedback`, `help(package = "docx2prompt")`.

## Que genera

Un checklist Markdown del estilo:

```markdown
- [ ] **Texto original:** `fragmento senalado en Word`
      **Instruccion:** cambia X por Y
```

El prompt embebido indica al agente donde buscar (`source_glob`, por defecto
`*.Rmd`) y que marque las casillas al terminar.

## Pruebas

```r
devtools::test()
```

## Licencia

MIT (c) Marco Ezquerra Ruano
