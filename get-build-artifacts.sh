#!/usr/bin/env bash
# make artifacts available to volume mounted to docker container
export OUTPUT_DIR=_output
bazel build //...
cp -f -a bazel-bin/apps ${OUTPUT_DIR}
