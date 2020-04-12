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
    timeout = "short",
    srcs = ["tests/test_BaseTestCase.py"],
    local = True,
    deps = [":lib"],
)

py_test(
    name = "test_top_level_functions",
    timeout = "short",
    srcs = ["tests/test_top_level_functions.py"],
    local = True,
    deps = [
        ":lib",
        requirement("praw"),
    ],
)
