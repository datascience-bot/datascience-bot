#!/usr/bin/env bash
# export BAZEL_FLAGS="--discard_analysis_cache --nokeep_state_after_build --notrack_incremental_state"
export OUTPUT_DIR=_output

mkdir -p $OUTPUT_DIR

bazel build //... ${BAZEL_FLAGS}
bazel test //... ${BAZEL_FLAGS}

# make binaries available to volume mounted to docker container
cp -f bazel-bin/apps/submission_moderator_app/bin.zip ${OUTPUT_DIR}/bin.zip

bazel clean
