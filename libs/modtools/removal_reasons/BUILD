load("@rules_python//python:defs.bzl", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

py_library(
    name = "lib",
    srcs = ["__init__.py"],
    data = ["data/removal-reasons.yaml"],
    visibility = ["//:modtools"],
    deps = [
        requirement("praw"),
        requirement("pyyaml"),
    ],
)

py_test(
    name = "test_removal_reasons",
    timeout = "short",
    srcs = ["tests/test_removal_reasons.py"],
    local = True,
    deps = [":lib"],
)

py_test(
    name = "test_praw_integration",
    timeout = "short",
    srcs = ["tests/test_praw_integration.py"],
    flaky = True,
    local = False,
    deps = [
        ":lib",
        "//libs/shared/authpraw:lib",
    ],
)
