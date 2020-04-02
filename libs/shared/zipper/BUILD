load("@rules_python//python:defs.bzl", "py_binary", "py_library")

py_library(
    name = "lib",
    srcs = ["zipper.py"],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "bin",
    srcs = [":lib"],
    main = "zipper.py",
    visibility = ["//visibility:public"],
)
