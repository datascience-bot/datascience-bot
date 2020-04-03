load("@rules_python//python:defs.bzl", "py_binary", "py_library")

py_library(
    name = "lib",
    srcs = [
        "__init__.py",
        "__main__.py",
        "data/preamble_template.py",
    ],
    data = ["data/preamble_template.py"],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "bin",
    srcs = [":lib"],
    main = "__main__.py",
    visibility = ["//visibility:public"],
)
