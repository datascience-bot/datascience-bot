load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

py_library(
    name = "lib",
    srcs = ["__init__.py"],
    visibility = ["//visibility:public"],
    deps = [
        "//libs/shared/authpraw:lib",
        requirement("praw"),
    ],
)

py_test(
    name = "test_modwiki",
    timeout = "short",
    srcs = ["tests/test_modwiki.py"],
    data = glob(["tests/testwiki/*.md"]),
    local = True,
    deps = [
        ":lib",
        "//libs/shared/pram:lib",
        requirement("praw"),
    ],
)
