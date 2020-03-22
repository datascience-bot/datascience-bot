load("@rules_python//python:defs.bzl", "py_binary", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

py_library(
    name = "lib",
    srcs = ["submission_moderator.py"],
    imports = ["."],
    deps = [
        "//libs/authpraw:lib",
        requirement("packaging"),
        requirement("praw"),
    ],
)

py_test(
    name = "SubmissionClassifier_test",
    srcs = [
        "tests/BaseTestCase.py",
        "tests/SubmissionClassifier_test.py",
    ],
    deps = [":lib"],
)

py_test(
    name = "SubmissionModerator_test",
    srcs = [
        "tests/BaseTestCase.py",
        "tests/SubmissionModerator_test.py",
    ],
    deps = [
        ":SubmissionClassifier_test",
        ":lib",
    ],
)

py_test(
    name = "get_submission_test",
    srcs = ["tests/get_submission_test.py"],
    deps = [
        ":lib",
        "//libs/authpraw:lib",
        requirement("praw"),
    ],
)

py_binary(
    name = "app",
    srcs = ["app.py"],
    deps = [
        ":lib",
        requirement("flask"),
        requirement("packaging"),
        requirement("waitress"),
    ],
)

py_test(
    name = "app_test",
    srcs = ["tests/app_test.py"],
    deps = [
        ":app",
        requirement("packaging"),
    ],
)
