load("@rules_python//python:defs.bzl", "py_binary", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

py_library(
    name = "lib",
    srcs = ["__init__.py"],
    visibility = ["//visibility:public"],
    deps = [
        "//libs/shared/authpraw:lib",
        requirement("pandas"),
        requirement("praw"),
    ],
)

py_test(
    name = "test",
    timeout = "short",
    srcs = ["tests/test_dataset.py"],
    flaky = False,  # don't try more than once even if it interacts w/ praw
    local = False,
    main = "tests/test_dataset.py",
    deps = [
        ":lib",
        "//libs/shared/authpraw:lib",
        "//libs/shared/pram:lib",
    ],
)

py_binary(
    name = "make_dataset",
    srcs = ["__main__.py"],
    main = "__main__.py",
    deps = [
        "lib",
        requirement("pandas"),
        requirement("praw"),
    ],
)
