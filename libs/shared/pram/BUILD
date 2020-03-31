load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

py_library(
    name = "lib",
    srcs = ["__init__.py"],
    visibility = ["//visibility:public"],
    deps = [
        requirement("praw"),
    ],
)

py_test(
    name = "test_BaseTestCase",
    srcs = ["tests/test_BaseTestCase.py"],
    deps = [":lib"],
)

py_test(
    name = "test_top_level_functions",
    srcs = ["tests/test_top_level_functions.py"],
    deps = [
        ":lib",
        requirement("praw"),
    ],
)
