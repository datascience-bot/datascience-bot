load("@rules_python//python:defs.bzl", "py_binary")

py_binary(
    name = "bin",
    srcs = ["__main__.py"],
    main = "__main__.py",
    deps = [
        "//libs/modtools/site_admin:lib",
        "//libs/shared/authpraw:lib",
        "//libs/shared/logging:lib",
    ],
)
