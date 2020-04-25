load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

py_library(
    name = "lib",
    srcs = ["__init__.py"],
    data = glob(["wiki/*.md"]),
    visibility = ["//:wiki_moderator_app"],
    deps = [
        "//libs/shared/authpraw:lib",
        "//libs/shared/modwiki:lib",
        requirement("praw"),
    ],
)

py_test(
    name = "test_wiki_moderator_app",
    timeout = "short",
    srcs = ["tests/test_wiki_moderator_app.py"],
    local = True,
    deps = [":lib"],
)
