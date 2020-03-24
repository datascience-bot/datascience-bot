load("@rules_python//python:defs.bzl", "py_binary", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

py_library(
    name = "app",
    srcs = ["app/__init__.py"],
    imports = ["."],
    deps = [
        requirement("flask"),
        requirement("packaging"),
        requirement("waitress"),
        "//libs/submission_moderator_app/submission_moderator:lib",
    ],
)

py_test(
    name = "test",
    srcs = ["tests/test_app.py"],
    main = "tests/test_app.py",
    deps = [
        ":app",
        requirement("packaging"),
    ],
)

py_binary(
    name = "bin",
    srcs = [
        "app/__init__.py",
        "app/__main__.py",
    ],
    main = "__main__.py",
    deps = [
        ":app",
        "//libs/submission_moderator_app/submission_moderator:lib",
        requirement("flask"),
        requirement("packaging"),
        requirement("waitress"),
    ],
)
