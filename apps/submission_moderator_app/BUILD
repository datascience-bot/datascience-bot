load("@rules_python//python:defs.bzl", "py_binary", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")
load("//tools/lambda_python_pkg:defs.bzl", "lambda_python_pkg")

py_library(
    name = "lib",
    srcs = ["__init__.py"],
    deps = [
        "//libs/shared/authpraw:lib",
        "//libs/shared/monitor:lib",
        "//libs/submission_moderator_app/submission_moderator:lib",
    ],
)

py_test(
    name = "test",
    srcs = ["tests/test_submission_moderator_app.py"],
    main = "tests/test_submission_moderator_app.py",
    deps = [
        ":lib",
        "//libs/shared/authpraw:lib",
    ],
)

py_binary(
    name = "bin",
    srcs = ["__main__.py"],
    main = "__main__.py",
    deps = [":lib"],
)

py_binary(
    name = "lambda_function",
    srcs = ["lambda_function.py"],
    main = "lambda_function.py",
    deps = [
        ":lib",
        requirement("praw"),
    ],
)

lambda_python_pkg(
    name = "lambda_pkg",
    src = ":lambda_function",
    out = "lambda_pkg.zip",
    main = "lambda_function.py",
)
