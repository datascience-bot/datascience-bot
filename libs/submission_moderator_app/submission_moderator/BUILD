load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

py_library(
    name = "lib",
    srcs = ["__init__.py"],
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
        ":lib",
        ":test_SubmissionClassifier",
    ],
)
