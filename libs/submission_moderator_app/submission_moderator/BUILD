load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

py_library(
    name = "lib",
    srcs = ["submission_moderator/__init__.py"],
    imports = ["."],
    visibility = ["//visibility:public"],
    deps = [
        "//libs/shared/authpraw:lib",
        requirement("packaging"),
        requirement("praw"),
    ],
)

py_test(
    name = "test_SubmissionClassifier",
    srcs = [
        "tests/BaseTestCase.py",
        "tests/test_SubmissionClassifier.py",
    ],
    deps = [":lib"],
)

py_test(
    name = "test_SubmissionModerator",
    srcs = [
        "tests/BaseTestCase.py",
        "tests/test_SubmissionModerator.py",
    ],
    deps = [
        ":test_SubmissionClassifier",
        ":lib",
    ],
)

py_test(
    name = "test_get_submission",
    srcs = ["tests/test_get_submission.py"],
    deps = [
        ":lib",
        "//libs/shared/authpraw:lib",
        requirement("praw"),
    ],
)
