load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

py_library(
    name = "lib",
    srcs = ["authpraw.py"],
    imports = ["."],
    visibility = ["//visibility:public"],
    deps = [requirement("praw")],
)

py_test(
    name = "authpraw_test",
    srcs = ["tests/authpraw_test.py"],
    deps = [":lib"],
)
