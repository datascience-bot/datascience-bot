load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

py_library(
    name = "lib",
    srcs = ["__init__.py"],
    visibility = ["//visibility:public"],
    deps = [requirement("praw")],
)

py_test(
    name = "test",
    timeout = "short",
    srcs = ["tests/test_authpraw.py"],
    flaky = True,  # praw integration can fail
    local = False,
    main = "tests/test_authpraw.py",
    deps = [":lib"],
)
