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
    name = "test",
    srcs = ["tests/test_authpraw.py"],
    main = "tests/test_authpraw.py",
    deps = [":lib"],
)
