#!/usr/bin/env bash
# export BAZEL_FLAGS="--discard_analysis_cache --nokeep_state_after_build --notrack_incremental_state"
export OUTPUT_DIR=_output
export SUBMISSION_MODERATOR_APP_DIR=${OUTPUT_DIR}/submission_moderator_app

# mkdir -p $OUTPUT_DIR
mkdir -p $SUBMISSION_MODERATOR_APP_DIR

bazel build //... ${BAZEL_FLAGS}
bazel test //... ${BAZEL_FLAGS}

# make binaries available to volume mounted to docker container
cp -f -r bazel-bin/apps/submission_moderator_app/lambda_pkg.zip ${SUBMISSION_MODERATOR_APP_DIR}/lambda_pkg.zip

bazel clean
