#!/usr/bin/env bash
# help configure vscode remote development

WORKING_DIR=$(dirname `pwd`)
DEVCONTAINER_DIR=${WORKING_DIR}/.devcontainer
DEVCONTAINER_JSON=${DEVCONTAINER_DIR}/devcontainer.json
ENV_FILE=${DEVCONTAINER_DIR}/dev.env

mkdir -p $DEVCONTAINER_DIR

if [ -e $DEVCONTAINER_JSON ]
then
echo "${DEVCONTAINER_JSON} already exists"
else
cat > $DEVCONTAINER_JSON << EOF
{
    "name": "datascience-bot",
    "dockerFile": "${WORKING_DIR}/Dockerfile",
    "context": "..",
    "runArgs": [
        "--volume",
        "~/.cache/vscode/remote-container/datascience-bot/.vscode-server:/root/.vscode-server",
        "--env-file",
        "${ENV_FILE}"
    ],
    "extensions": [
        "bazelbuild.vscode-bazel",
        "coenraads.bracket-pair-colorizer",
        "eamodio.gitlens",
        "ms-azuretools.vscode-docker",
        "ms-python.python",
        "sonarsource.sonarlint-vscode",
        "vscjava.vscode-java-pack"
    ]
}
EOF
echo "Created ${DEVCONTAINER_JSON}"
fi

if [ -e $ENV_FILE ]
then
echo "${ENV_FILE} already exists"
else
cat > $ENV_FILE << EOF
# ask vogt4nick for credentials
DATASCIENCE_BOT_USERNAME=datascience-bot
DATASCIENCE_BOT_PASSWORD=
DATASCIENCE_BOT_CLIENT_ID=
DATASCIENCE_BOT_CLIENT_SECRET=

# for integration tests
SUBREDDIT_NAME=datascience_bot_dev

SUBSTANTIALSTRAIN6_USERNAME=SubstantialStrain6
SUBSTANTIALSTRAIN6_PASSWORD=
SUBSTANTIALSTRAIN6_CLIENT_ID=
SUBSTANTIALSTRAIN6_CLIENT_SECRET=

B3405920_USERNAME=b3405920
B3405920_PASSWORD=
B3405920_CLIENT_ID=
B3405920_CLIENT_SECRET=
EOF
echo "Created ${ENV_FILE}"
fi
