#!/usr/bin/env bash
# export BAZEL_FLAGS="--discard_analysis_cache --nokeep_state_after_build --notrack_incremental_state"
export OUTPUT_DIR=_output
export SUBMISSION_MODERATOR_APP_DIR=${OUTPUT_DIR}/submission_moderator_app
export ENTERING_AND_TRANSITIONING_APP_DIR=${OUTPUT_DIR}/entering_and_transitioning_app

# mkdir -p $OUTPUT_DIR
mkdir -p $SUBMISSION_MODERATOR_APP_DIR
mkdir -p $ENTERING_AND_TRANSITIONING_APP_DIR

bazel build //... ${BAZEL_FLAGS}

# make artifacts available to volume mounted to docker container
cp -f -r bazel-bin/apps/submission_moderator_app/lambda_pkg.zip ${SUBMISSION_MODERATOR_APP_DIR}/lambda_pkg.zip
cp -f -r bazel-bin/apps/entering_and_transitioning_app/lambda_pkg.zip ${ENTERING_AND_TRANSITIONING_APP_DIR}/lambda_pkg.zip
