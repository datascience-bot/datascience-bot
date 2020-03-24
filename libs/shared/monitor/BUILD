load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

py_library(
    name = "lib",
    srcs = ["monitor/__init__.py"],
    imports = ["."],
    visibility = ["//visibility:public"],
    deps = [
        "//libs/shared/authpraw:lib",
        requirement("praw"),
    ],
)

py_test(
    name = "test",
    srcs = ["tests/test_monitor.py"],
    main = "tests/test_monitor.py",
    deps = [
        ":lib",
        requirement("praw"),
    ],
)
