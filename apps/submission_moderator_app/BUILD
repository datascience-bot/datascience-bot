load("@rules_python//python:defs.bzl", "py_binary", "py_test")

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

py_test(
    name = "test",
    srcs = ["tests/test_bin.py"],
    data = [":bin"],
    main = "tests/test_bin.py",
    deps = ["//libs/shared/authpraw:lib"],
)

# TODO: instead of --build_python_zip, create the binary from our BUILD files
# load("@rules_pkg//:pkg.bzl", "pkg_zip")
# pkg_zip(
#     # pkg_zip does not include the binary's runfiles; this is known behavior
#     #     https://github.com/bazelbuild/rules_pkg/pull/127
#     # The experimental pkgfilegroup rule was PR'd in an effort to resolve this
#     #     https://github.com/bazelbuild/rules_pkg/pull/128
#     # This rule should work in bazelbuild/rules_pkg v0.2.5. It does not.
#     #     https://github.com/bazelbuild/rules_pkg/issues/104
#     # When the PR is merged, we should be able to create zips with the binary
#     # runfiles with the following statement
#     #     load("@rules_pkg//experimental:genpkg.bzl", "pkgfilegroup")
#     name = "lambda-zip",
#     srcs = [":bin"],
# )
