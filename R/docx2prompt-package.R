#' docx2prompt: de comentarios Word a prompts Markdown para agentes
#'
#' Automatiza el paso de revision de informes redactados en R Markdown o Quarto:
#' extrae comentarios nativos de un `.docx` a un checklist Markdown
#' (`FEEDBACK.md`) listo para Cursor u otros agentes de IA, que aplican
#' las instrucciones sobre los archivos fuente indicados por `source_glob`.
#'
#' Por defecto en R el prompt apunta a `*.Rmd`. Para Quarto usa
#' `source_glob = "*.qmd"`. Tambien puedes instalar el paquete Python
#' (`pip install -e python/`) y usarlo sin R.
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
