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
    timeout = "short",
    srcs = ["tests/test_SubmissionAuthor.py"],
    data = ["data/selftext.md"],
    local = True,
    main = "tests/test_SubmissionAuthor.py",
    deps = [
        ":lib",
        "//libs/shared/pram:lib",
        requirement("praw"),
    ],
)

py_test(
    name = "test_CommentRemediator",
    timeout = "short",
    srcs = ["tests/test_CommentRemediator.py"],
    local = True,
    main = "tests/test_CommentRemediator.py",
    deps = [
        ":lib",
        "//libs/shared/pram:lib",
        requirement("praw"),
    ],
)

py_test(
    name = "test_validation",
    timeout = "short",
    srcs = ["tests/test_validation.py"],
    local = True,
    main = "tests/test_validation.py",
    deps = [
        ":lib",
        "//libs/shared/pram:lib",
    ],
)
