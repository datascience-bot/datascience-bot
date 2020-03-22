load("@rules_python//python:defs.bzl", "py_library")
load("@py_deps//:requirements.bzl", "requirement")

py_library(
    name = "lib",
    srcs = ["authpraw.py"],
    imports = ["."],
    visibility = ["//visibility:public"],
    deps = [requirement("praw")],
)
