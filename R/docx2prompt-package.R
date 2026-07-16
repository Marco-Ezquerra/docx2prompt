#' docx2prompt: de comentarios Word a prompts Markdown para agentes
#'
#' Automatiza el paso de revision de informes redactados en R Markdown:
#' extrae comentarios nativos de un `.docx` a un checklist Markdown
#' (`FEEDBACK.md`) listo para Cursor u otros agentes de IA, que aplican
#' las instrucciones sobre los archivos `.Rmd` fuente.
#'
#' El flujo no asume bookdown: por defecto el prompt apunta a `*.Rmd`.
#' Si tus fuentes estan en una carpeta (p. ej. `book/`), pasa
#' `source_glob = "book/*.Rmd"`.
#'
#' @section Funciones principales:
#' \describe{
#'   \item{[extraer_feedback()]}{Word con comentarios -> Markdown checklist.}
#'   \item{[vaciar_feedback()]}{Limpia el Markdown tras aplicar correcciones.}
#' }
#'
#' @seealso [extraer_feedback()], [vaciar_feedback()]
#'
#' @keywords internal
"_PACKAGE"
