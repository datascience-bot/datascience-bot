load("@rules_python//python:defs.bzl", "py_binary", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")
load("//tools/zipper:defs.bzl", "lambda_python_pkg")

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

# new
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

# py_binary(
#     name = "handler",
#     srcs = ["handler.py"],
#     deps = [
#         "//examples/kitchensink/lib:core_python_proto",
#         "//examples/kitchensink/lib:id_gen",
#         "@pip3//silly",
#         requirement("redis"),
#     ],
# )

# lambda_python_pkg(
#     name = "handler_func",
#     src = ":handler",
#     out = "handler_func.zip",
#     main = "handler.py",
# )

# TODO: instead of --build_python_zip, create the binary from our BUILD files
# load("@rules_pkg//:pkg.bzl", "pkg_zip")
# pkg_zip(
#     # pkg_zip does not include the binary's runfiles; this is known behavior
#     #     https://github.com/bazelbuild/rules_pkg/pull/127
#     # The experimental pkgfilegroup rule was PR'd in an effort to resolve this
#     #     https://github.com/bazelbuild/rules_pkg/pull/128
#     # This rule should work in bazelbuild/rules_pkg v0.2.5. It does not.
#     #     https://github.com/bazelbuild/rules_pkg/issues/104
#     # When the PR is merged, we should be able to create zips with the binary
#     # runfiles with the following statement
#     #     load("@rules_pkg//experimental:genpkg.bzl", "pkgfilegroup")
#     name = "lambda-zip",
#     srcs = [":bin"],
# )
