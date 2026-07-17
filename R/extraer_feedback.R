#' Extrae comentarios de un archivo Word a un formato legible por IA
#'
#' Lee los comentarios nativos de un `.docx` y genera un Markdown con
#' checklist (p. ej. `FEEDBACK.md`) orientado a agentes como Cursor.
#' El agente busca cada **Texto original** en los archivos fuente
#' (por defecto `*.Rmd`) y aplica la **Instruccion**.
#'
#' @param docx_path Ruta al archivo `.docx` a analizar.
#' @param output_md Ruta donde se generara el Markdown. Por defecto `"FEEDBACK.md"`.
#' @param source_glob Glob de fuentes para el prompt embebido. Por defecto `"*.Rmd"`.
#'   Para Quarto usa p. ej. `"*.qmd"`. En bookdown: `"book/*.Rmd"`.
#'
#' @return Ruta del Markdown generado (invisible).
#'
#' @details
#' Flujo tipico:
#' 1. Revisas el informe en Word y dejas comentarios nativos.
#' 2. Ejecutas `extraer_feedback()` para generar el checklist Markdown.
#' 3. En Cursor (u otro agente), abres el `.md` y aplicas cada tarea sobre
#'    los fuentes indicados por `source_glob`.
#' 4. Cuando termines, llama a [vaciar_feedback()] para limpiar el checklist.
#'
#' @seealso [vaciar_feedback()]
#'
#' @examples
#' \dontrun{
#' extraer_feedback("informe_comentado.docx")
#' extraer_feedback("informe.docx", "revisiones.md", source_glob = "book/*.Rmd")
#' extraer_feedback("informe.docx", source_glob = "*.qmd")
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

  run_python <- function(args) {
    out <- system2(py_exe, args = args, stdout = TRUE, stderr = TRUE)
    status <- attr(out, "status")
    if (is.null(status)) {
      status <- 0L
    }
    list(output = out, status = status)
  }

  args_module <- c(
    "-m", "docx2prompt", "extract",
    docx_path, "-o", output_md_abs,
    "--source-glob", source_glob
  )
  res <- run_python(args_module)

  if (res$status != 0L) {
    py_script <- system.file("python", "extraer_comentarios.py", package = "docx2prompt")
    if (!nzchar(py_script) || !file.exists(py_script)) {
      stop(
        "No se encontr\u00f3 el motor de Python del paquete. ",
        "Instala docx2prompt con pip install -e python/ o reinstala el paquete R.",
        call. = FALSE
      )
    }
    args_script <- c(
      py_script,
      docx_path,
      output_md_abs,
      "--source-glob",
      source_glob
    )
    res <- run_python(args_script)
  }

  if (length(res$output)) {
    message(paste(res$output, collapse = "\n"))
  }

  if (res$status != 0L) {
    stop("Hubo un error al ejecutar el motor de Python.", call. = FALSE)
  }

  message("Extracci\u00f3n completada. Puedes revisar ", output_md_abs)
  invisible(output_md_abs)
}
