load("@rules_python//python:defs.bzl", "py_binary", "py_library")

py_library(
    name = "lib",
    srcs = ["__init__.py"],
    deps = ["//libs/wiki:lib"],
)

py_binary(
    name = "bin",
    srcs = ["__main__.py"],
    main = "__main__.py",
    deps = [":lib"],
)
