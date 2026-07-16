test_that("find_python encuentra un ejecutable o NULL", {
  found <- docx2prompt:::find_python()
  expect_true(is.null(found) || (is.character(found) && file.exists(found)))
})
