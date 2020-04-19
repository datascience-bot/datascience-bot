load("@rules_python//python:defs.bzl", "py_binary", "py_library", "py_test")
load("@py_deps//:requirements.bzl", "requirement")

py_library(
    name = "lib",
    srcs = ["__init__.py"],
    deps = [
        "//libs/shared/models/novice_submission_classifier/dataset:lib",
        requirement("pandas"),
        requirement("scikit-learn"),
    ],
)

py_binary(
    name = "fit_classifier",
    srcs = ["__main__.py"],
    data = ["data/novice_submission_labels.csv"],
    main = "__main__.py",
    deps = [
        ":lib",
        requirement("joblib"),
        requirement("scikit-learn"),
    ],
)
