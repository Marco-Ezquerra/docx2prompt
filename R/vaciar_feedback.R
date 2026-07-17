#' Vacia un archivo de feedback Markdown
#'
#' Sobrescribe `FEEDBACK.md` (u otra ruta) con una plantilla limpia para
#' no acumular tareas ya aplicadas ni consumir tokens innecesarios en la
#' siguiente iteracion con un agente.
#'
#' @param md_path Ruta al Markdown de feedback. Por defecto `"FEEDBACK.md"`.
#' @param source_glob Glob de fuentes mostrado en el prompt de la plantilla.
#'   Por defecto `"*.Rmd"`. Para Quarto usa `"*.qmd"`.
#'
#' @return Ruta del archivo vaciado (invisible).
#'
#' @details
#' Usa esta funcion despues de que el agente haya aplicado las correcciones
#' del checklist generado por [extraer_feedback()].
#'
#' @seealso [extraer_feedback()]
#'
#' @examples
#' \dontrun{
#' vaciar_feedback()
#' vaciar_feedback("revisiones.md", source_glob = "*.qmd")
#' }
#'
#' @export
vaciar_feedback <- function(md_path = "FEEDBACK.md",
                            source_glob = "*.Rmd") {
  stamp <- format(Sys.time(), "%Y-%m-%d %H:%M")
  lines <- c(
    sprintf("# Revisiones del documento - %s", stamp),
    "",
    "> **PROMPT PARA CURSOR:**",
    "> Lee cada tarea de esta lista. Busca el fragmento exacto indicado en **Texto original**",
    sprintf(
      "> dentro de los archivos que coincidan con `%s` y aplica la **Instrucci\u00f3n**.",
      source_glob
    ),
    "> No alteres el resto del documento. Al terminar cada cambio, marca la casilla con una `x`.",
    "",
    "*Sin tareas pendientes. Ejecuta `docx2prompt::extraer_feedback()` tras revisar el Word.*",
    ""
  )

  out_dir <- dirname(md_path)
  if (!identical(out_dir, ".") && !dir.exists(out_dir)) {
    dir.create(out_dir, recursive = TRUE)
  }

  writeLines(lines, md_path, useBytes = FALSE)
  message("Feedback vaciado: ", normalizePath(md_path, winslash = "/", mustWork = FALSE))
  invisible(normalizePath(md_path, winslash = "/", mustWork = FALSE))
}
