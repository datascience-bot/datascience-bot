load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

py_library(
    name = "lib",
    srcs = ["__init__.py"],
    visibility = ["//:submission_moderator_app"],
    deps = [
        "//libs/submission_moderator_app/submission_classifier:lib",
        requirement("praw"),
    ],
)

py_test(
    name = "test_SubmissionArbiter",
    srcs = ["tests/test_SubmissionArbiter.py"],
    deps = [
        ":lib",
        "//libs/shared/pram:lib",
    ],
)
