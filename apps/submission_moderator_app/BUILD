load("@rules_python//python:defs.bzl", "py_binary")

py_binary(
    name = "bin",
    srcs = ["app.py"],
    main = "app.py",
    deps = [
        "//libs/shared/authpraw:lib",
        "//libs/shared/monitor:lib",
        "//libs/submission_moderator_app/submission_moderator:lib",
    ],
)
