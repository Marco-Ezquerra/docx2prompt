test_that("extraer_feedback escribe checklist desde fixture", {
  skip_if(is.null(docx2prompt:::find_python()), "Python no disponible")

  fixture <- testthat::test_path("fixtures", "comentarios_minimos.docx")
  out <- tempfile(fileext = ".md")
  on.exit(unlink(out), add = TRUE)

  path <- extraer_feedback(fixture, output_md = out)
  expect_true(file.exists(path))

  md <- paste(readLines(path, encoding = "UTF-8", warn = FALSE), collapse = "\n")
  expect_match(md, "PROMPT PARA CURSOR")
  expect_match(md, "\\*\\.Rmd")
  expect_false(grepl("book/\\*\\.Rmd", md))
  expect_match(md, "Texto original:")
  expect_match(md, "alfa")
  expect_match(md, "Cambia alfa por alpha")
  expect_match(md, "beta gamma")
  expect_match(md, "Unifica beta gamma")
})

test_that("extraer_feedback respeta source_glob personalizado", {
  skip_if(is.null(docx2prompt:::find_python()), "Python no disponible")

  fixture <- testthat::test_path("fixtures", "comentarios_minimos.docx")
  out <- tempfile(fileext = ".md")
  on.exit(unlink(out), add = TRUE)

  path <- extraer_feedback(fixture, output_md = out, source_glob = "book/*.Rmd")
  md <- paste(readLines(path, encoding = "UTF-8", warn = FALSE), collapse = "\n")
  expect_match(md, "book/\\*\\.Rmd")
})

test_that("extraer_feedback con docx sin comentarios", {
  skip_if(is.null(docx2prompt:::find_python()), "Python no disponible")

  fixture <- testthat::test_path("fixtures", "sin_comentarios.docx")
  out <- tempfile(fileext = ".md")
  on.exit(unlink(out), add = TRUE)

  path <- extraer_feedback(fixture, output_md = out)
  md <- paste(readLines(path, encoding = "UTF-8", warn = FALSE), collapse = "\n")
  expect_match(md, "No se encontraron comentarios")
})

test_that("extraer_feedback falla si el docx no existe", {
  expect_error(
    extraer_feedback("archivo_que_no_existe_xyz.docx"),
    "No se encuentra el Word"
  )
})
