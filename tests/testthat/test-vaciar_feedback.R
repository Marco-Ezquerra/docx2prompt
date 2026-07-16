test_that("vaciar_feedback escribe plantilla limpia", {
  out <- tempfile(fileext = ".md")
  on.exit(unlink(out), add = TRUE)

  writeLines(c("- [ ] tarea vieja", ""), out)
  path <- vaciar_feedback(out, source_glob = "src/*.Rmd")
  expect_true(file.exists(path))

  md <- paste(readLines(path, encoding = "UTF-8", warn = FALSE), collapse = "\n")
  expect_match(md, "PROMPT PARA CURSOR")
  expect_match(md, "src/\\*\\.Rmd")
  expect_match(md, "Sin tareas pendientes")
  expect_false(grepl("tarea vieja", md, fixed = TRUE))
})
