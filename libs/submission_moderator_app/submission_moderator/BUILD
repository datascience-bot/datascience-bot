load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

py_library(
    name = "lib",
    srcs = ["__init__.py"],
    visibility = ["//:submission_moderator_app"],
    deps = [
        "//libs/shared/authpraw:lib",
        "//libs/submission_moderator_app/submission_arbiter:lib",
        "//libs/submission_moderator_app/submission_classifier:lib",
        requirement("praw"),
    ],
)

py_test(
    name = "test_SubmissionModerator",
    srcs = ["tests/test_SubmissionModerator.py"],
    deps = [
        ":lib",
        "//libs/shared/pram:lib",
    ],
)
