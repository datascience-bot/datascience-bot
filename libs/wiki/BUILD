load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

py_library(
    name = "lib",
    srcs = ["__init__.py"],
    data = glob(["data/*.md"]),
    visibility = ["//:wiki"],
    deps = [
        "//libs/shared/authpraw:lib",
        "//libs/shared/modwiki:lib",
        requirement("praw"),
    ],
)

py_test(
    name = "test_wiki",
    timeout = "short",
    srcs = ["tests/test_wiki.py"],
    local = True,
    deps = [":lib"],
)
