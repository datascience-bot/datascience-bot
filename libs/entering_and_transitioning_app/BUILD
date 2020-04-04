load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

py_library(
    name = "lib",
    srcs = ["__init__.py"],
    data = ["data/selftext.md"],
    visibility = ["//:entering_and_transitioning_app"],
    deps = [requirement("praw")],
)

py_test(
    name = "test_SubmissionAuthor",
    srcs = ["tests/test_SubmissionAuthor.py"],
    data = ["data/selftext.md"],
    main = "tests/test_SubmissionAuthor.py",
    deps = [
        ":lib",
        "//libs/shared/pram:lib",
        requirement("praw"),
    ],
)

py_test(
    name = "test_CommentRemediator",
    srcs = ["tests/test_CommentRemediator.py"],
    main = "tests/test_CommentRemediator.py",
    deps = [
        ":lib",
        "//libs/shared/pram:lib",
        requirement("praw"),
    ],
)

py_test(
    name = "test_validation",
    srcs = ["tests/test_validation.py"],
    main = "tests/test_validation.py",
    deps = [
        ":lib",
        "//libs/shared/pram:lib",
    ],
)
