load("@rules_python//python:defs.bzl", "py_library")
load("@py_deps//:requirements.bzl", "requirement")

py_library(
    name = "lib",
    srcs = ["__init__.py"],
    data = ["data/welcome.md"],
    visibility = ["//:modtools"],
    deps = [
        requirement("praw"),
    ],
)
