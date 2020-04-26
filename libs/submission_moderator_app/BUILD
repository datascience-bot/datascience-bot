load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

py_library(
    name = "lib",
    srcs = ["__init__.py"],
    visibility = ["//:submission_moderator_app"],
    deps = [
        "//libs/shared/monitor:lib",
        requirement("praw"),
    ],
)

py_test(
    name = "test_SubmissionArbiter",
    timeout = "short",
    srcs = ["tests/test_SubmissionArbiter.py"],
    local = True,
    deps = [
        ":lib",
        "//libs/shared/pram:lib",
    ],
)

py_test(
    name = "test_SubmissionClassifier",
    timeout = "short",
    srcs = ["tests/test_SubmissionClassifier.py"],
    local = True,
    deps = [
        ":lib",
        "//libs/shared/pram:lib",
    ],
)

py_test(
    name = "test_SubmissionModerator",
    timeout = "short",
    srcs = ["tests/test_SubmissionModerator.py"],
    local = True,
    deps = [
        ":lib",
        "//libs/shared/pram:lib",
    ],
)

py_test(
    name = "test_praw_integration",
    timeout = "short",
    srcs = ["tests/test_praw_integration.py"],
    flaky = True,  # praw integration can fail
    local = False,
    deps = [
        ":lib",
        "//libs/shared/authpraw:lib",
    ],
)
