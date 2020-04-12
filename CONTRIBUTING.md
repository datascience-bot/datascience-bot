# Contributing

When contributing to this repository, please first [create an issue](https://github.com/datascience-bot/datascience-bot/issues) to discuss the change you wish to make with the owners of this repository before making a change.

Please note we have a [code of conduct](CODE_OF_CONDUCT.md). Please follow it in all your interactions with the project.

In this document we cover some topics to help you get started:

1. Setup Your Local Development Environment
1. Monitor Builds in the CI/CD Pipeline


## Setup Your Local Development Environment

We maintain a consistent development environment across contributors with development images. The only software requirement for your local machine is [Docker](https://www.docker.com/).

```bash
$ docker build -t datascience-bot/dev .  # this will take a few minutes

$ docker run -it -v=$(pwd):/workspaces/datascience-bot datascience-bot/dev

root@1234567890:/workspaces/datascience-bot$ ls
BUILD  CODE_OF_CONDUCT.md  CONTRIBUTING.md  Dockerfile  LICENSE  README.md  WORKSPACE  apps  external  get-build-artifacts.sh  libs  tools

root@1234567890:/workspaces/datascience-bot$ bazel test //libs/submission_moderator_app:all
INFO: Invocation ID: fa66f96b-a8a4-4d62-9aa7-2153b60bd8cf
INFO: Analyzed 4 targets (0 packages loaded, 8 targets configured).
INFO: Found 1 target and 3 test targets...
INFO: Elapsed time: 2.922s, Critical Path: 2.66s
INFO: 6 processes: 6 processwrapper-sandbox.
INFO: Build completed successfully, 4 total actions
//libs/submission_moderator_app:test_SubmissionArbiter                   PASSED in 2.1s
//libs/submission_moderator_app:test_SubmissionClassifier                PASSED in 1.5s
//libs/submission_moderator_app:test_SubmissionModerator                 PASSED in 2.6s

INFO: Build completed successfully, 4 total actions
```

Now you can change files locally and run commands in the container without installing a specific version of Bazel, Java, Go, Python, etc.

### Setup VS Code Remote Containers

The trouble with development containers is that your IDE can't connect to it, making many of its features useless (e.g. Intellisense). VS Code helps navigate this problem with the [Remote Development Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack).

The `tools/gen-vscode-devcontainer-config.sh` helps you get started:

```bash
$ cd tools
$ bash gen-vscode-devcontainer-config.sh
Created /Users/nick.vogt/dev/datascience-bot/datascience-bot/.devcontainer/devcontainer.json
Created /Users/nick.vogt/dev/datascience-bot/datascience-bot/.devcontainer/dev.env
```

The rest is up to you!

**Resources:**

* [Docker Volumes](https://docs.docker.com/storage/volumes/)
* [VS Code Remote Development](https://code.visualstudio.com/docs/remote/remote-overview)


## Monitor Builds in the CI/CD Pipeline

Anyone can monitor our CI/CD Pipeline [here](https://travis-ci.com/datascience-bot/datascience-bot).

Without all the requisite credentials, you won't be able to run the integration tests. The best alternative is to monitor builds in the CI/CD pipeline which has all credentials necessary to make tests pass. Our build process needs work; each build takes 7-8 minutes, and most of that time is spent rebuilding an image that rarely changes.

Fortunately, you shouldn't have to unless you're developing some brand new behavior. We'll work something out in that case.
