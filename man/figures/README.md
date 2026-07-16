# Figuras del README

Las capturas del landing deben salir de un **caso real**: informe Rmd con tablas, graficos y redaccion, exportado a Word, con comentarios nativos.

Hasta que existan los PNG, el README mostrara imagenes rotas en GitHub; es esperado.

## Archivos a anadir aqui

| Archivo | Que capturar |
|---------|----------------|
| `01-word-comentarios.png` | Word knit desde Rmd (tablas/graficos visibles) con 2–3 comentarios nativos visibles |
| `02-cursor-rmd.png` | Cursor/IDE con el `.Rmd` y el checklist `FEEDBACK.md` aplicando un cambio |
| `03-feedback-md.png` | (Opcional) Fragmento del `FEEDBACK.md` generado |

## Demo local en este repo (gitignored)

Hay una carpeta `demo-informe/` (en `.gitignore`, no se sube a GitHub) con un Rmd
basado en `ggplot2::mpg` (tablas, graficos y redaccion):

```r
# En la raiz del paquete:
source("demo-informe/render.R")
# → demo-informe/informe_demo.docx
```

Luego abre ese Word, comenta tabla / figura / parrafo, guarda y:

```r
docx2prompt::extraer_feedback("demo-informe/informe_demo.docx")
```

## Pasos recomendados

1. Knit el demo (`source("demo-informe/render.R")`) o tu propio informe Rmd a `.docx`.
2. Abre el Word, anade comentarios nativos sobre fragmentos concretos, guarda.
3. En R: `docx2prompt::extraer_feedback("demo-informe/informe_demo.docx")`.
4. Abre `FEEDBACK.md` en Cursor y aplica una tarea sobre el `.Rmd`.
5. Haz las capturas, guardalas con los nombres de la tabla y copialas a esta carpeta.
6. Commit + push **solo** de los PNG en `man/figures/` (no de `demo-informe/`).


## Formato

- PNG (o GIF con el mismo nombre si mas adelante quieres animacion).
- Ancho orientativo 1200–1600 px; evita datos personales o confidenciales en pantalla.
