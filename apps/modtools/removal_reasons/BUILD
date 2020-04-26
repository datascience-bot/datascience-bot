load("@rules_python//python:defs.bzl", "py_binary")

py_binary(
    name = "bin",
    srcs = ["__main__.py"],
    main = "__main__.py",
    deps = [
        "//libs/modtools/removal_reasons:lib",
        "//libs/shared/authpraw:lib",
    ],
)
