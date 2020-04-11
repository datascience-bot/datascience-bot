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
    name = "test",
    srcs = ["tests/test_monitor.py"],
    flaky = True,  # praw integration can fail
    main = "tests/test_monitor.py",
    deps = [
        ":lib",
        requirement("praw"),
    ],
)
