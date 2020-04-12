load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "rules_python",
    sha256 = "aa96a691d3a8177f3215b14b0edc9641787abaaa30363a080165d06ab65e1161",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.0.1/rules_python-0.0.1.tar.gz",
)

load("@rules_python//python:repositories.bzl", "py_repositories")

# keep `py_repositories` to make it less likely we need to update the
# WORKSPACE file, in case this function is changed in the future.
# https://github.com/bazelbuild/rules_python/blob/748aa53d7701e71101dfd15d800e100f6ff8e5d1/python/repositories.bzl#L9-L12
py_repositories()

# >>> fetch and define transitive python dependencies ------------------------
rules_python_external_version = "b98194454d5fd06828bb3f5bf54fb77ab26b571d"

http_archive(
    name = "rules_python_external",
    sha256 = "90c77f24c93464520481ec5140d416498475568326ba60a049274e85cacaa027",
    strip_prefix = "rules_python_external-{version}".format(version = rules_python_external_version),
    url = "https://github.com/dillon-giacoppo/rules_python_external/archive/{version}.zip".format(version = rules_python_external_version),
)

load("@rules_python_external//:repositories.bzl", "rules_python_external_dependencies")
load("@rules_python_external//:defs.bzl", "pip_install")

rules_python_external_dependencies()

pip_install(
    name = "py_deps",
    requirements = "python/requirements.txt",
)
# <<< fetch and define transitive python dependencies ------------------------
