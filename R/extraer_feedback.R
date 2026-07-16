#' Extrae comentarios de un archivo Word a un formato legible por IA
#'
#' Lee los comentarios nativos de un `.docx` y genera un Markdown con
#' checklist (p. ej. `FEEDBACK.md`) orientado a agentes como Cursor.
#' El agente busca cada **Texto original** en los archivos `.Rmd` fuente
#' (por defecto `*.Rmd`) y aplica la **Instruccion**.
#'
#' @param docx_path Ruta al archivo `.docx` a analizar.
#' @param output_md Ruta donde se generara el Markdown. Por defecto `"FEEDBACK.md"`.
#' @param source_glob Glob o ruta relativa de fuentes `.Rmd` para el prompt
#'   embebido. Por defecto `"*.Rmd"` (cualquier R Markdown del proyecto).
#'   En bookdown puedes usar p. ej. `"book/*.Rmd"`.
#'
#' @return Ruta del Markdown generado (invisible).
#'
#' @details
#' Flujo tipico:
#' 1. Revisas el informe en Word y dejas comentarios nativos.
#' 2. Ejecutas `extraer_feedback()` para generar el checklist Markdown.
#' 3. En Cursor (u otro agente), abres el `.md` y aplicas cada tarea sobre
#'    los `.Rmd` fuente.
#' 4. Cuando termines, llama a [vaciar_feedback()] para limpiar el checklist.
#'
#' @seealso [vaciar_feedback()]
#'
#' @examples
#' \dontrun{
#' extraer_feedback("informe_comentado.docx")
#' extraer_feedback("informe.docx", "revisiones.md", source_glob = "book/*.Rmd")
#' }
#'
#' @export
extraer_feedback <- function(docx_path,
                             output_md = "FEEDBACK.md",
                             source_glob = "*.Rmd") {
  py_exe <- find_python()
  if (is.null(py_exe)) {
    stop(
      "No se encontr\u00f3 Python. Instala Python >= 3.8 o define DOCX2PROMPT_PYTHON ",
      "con la ruta al ejecutable.",
      call. = FALSE
    )
  }

  py_script <- system.file("python", "extraer_comentarios.py", package = "docx2prompt")
  if (!nzchar(py_script) || !file.exists(py_script)) {
    stop(
      "No se encontr\u00f3 el motor de Python del paquete. ",
      "\u00bfEst\u00e1 docx2prompt instalado correctamente?",
      call. = FALSE
    )
  }

  if (!file.exists(docx_path)) {
    stop(sprintf("No se encuentra el Word en: %s", docx_path), call. = FALSE)
  }

  docx_path <- normalizePath(docx_path, winslash = "/", mustWork = TRUE)
  output_md_abs <- if (dirname(output_md) == ".") {
    file.path(getwd(), basename(output_md))
  } else {
    output_md
  }
  output_dir <- dirname(output_md_abs)
  if (!dir.exists(output_dir)) {
    dir.create(output_dir, recursive = TRUE)
  }
  output_md_abs <- normalizePath(output_md_abs, winslash = "/", mustWork = FALSE)

  message("Iniciando motor de extracci\u00f3n Python...")

  # system2 cita cada argumento (espacios en rutas Windows); no usar shQuote a mano
  args <- c(
    py_script,
    docx_path,
    output_md_abs,
    "--source-glob",
    source_glob
  )

  codigo_salida <- system2(py_exe, args = args, stdout = TRUE, stderr = TRUE)
  status <- attr(codigo_salida, "status")
  if (is.null(status)) {
    status <- 0L
  }

  if (length(codigo_salida)) {
    message(paste(codigo_salida, collapse = "\n"))
  }

  if (status != 0L) {
    stop("Hubo un error al ejecutar el motor de Python.", call. = FALSE)
  }

  message("Extracci\u00f3n completada. Puedes revisar ", output_md_abs)
  invisible(output_md_abs)
}
