#' Localiza un interprete de Python usable
#'
#' Orden de busqueda: variable de entorno `DOCX2PROMPT_PYTHON` o `PY_PYTHON`,
#' luego `python` y `python3` en el PATH.
#'
#' @return Ruta absoluta al ejecutable, o `NULL` si no se encuentra.
#' @noRd
find_python <- function() {
  env_candidates <- c(Sys.getenv("DOCX2PROMPT_PYTHON", ""), Sys.getenv("PY_PYTHON", ""))
  for (p in env_candidates) {
    if (nzchar(p) && file.exists(p)) {
      return(normalizePath(p, winslash = "/", mustWork = TRUE))
    }
  }

  for (cmd in c("python", "python3")) {
    found <- Sys.which(cmd)
    if (nzchar(found) && file.exists(found)) {
      return(normalizePath(found, winslash = "/", mustWork = TRUE))
    }
  }

  NULL
}
