load("@rules_python//python:defs.bzl", "py_binary")
load("//tools/lambda_python_pkg:defs.bzl", "lambda_python_pkg")

py_binary(
    name = "bin",
    srcs = ["__main__.py"],
    main = "__main__.py",
    deps = [
        "//libs/shared/authpraw:lib",
        "//libs/shared/logging:lib",
        "//libs/submission_moderator_app:lib",
    ],
)

py_binary(
    name = "lambda_function",
    srcs = ["lambda_function.py"],
    main = "lambda_function.py",
    deps = [
        "//libs/shared/authpraw:lib",
        "//libs/shared/logging:lib",
        "//libs/submission_moderator_app:lib",
    ],
)

lambda_python_pkg(
    name = "lambda_pkg",
    src = ":lambda_function",
    out = "lambda_pkg.zip",
    main = "lambda_function.py",
)
