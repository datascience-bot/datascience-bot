# -*- coding: utf-8 -*-
from dataclasses import dataclass
import logging
import pathlib
from typing import Dict, List

import praw
from praw.models.reddit.removal_reasons import RemovalReason, SubredditRemovalReasons
import yaml


REMOVAL_REASONS_YAML: pathlib.Path = pathlib.Path(
    "libs/modtools/removal_reasons/data/removal-reasons.yaml"
)
logger = logging.getLogger(__name__)


@dataclass
class LocalRemovalReason:
    title: str
    message: str


def get_local_removal_reasons(p: pathlib.Path) -> List[Dict[str, str]]:
    p = pathlib.Path(p)
    with p.open("r") as ifile:
        removal_reasons = yaml.safe_load(ifile)

    for removal_reason in removal_reasons:
        for k, v in removal_reason.items():
            removal_reason[k] = v.rstrip().replace("\n", "\n\n")

    return [LocalRemovalReason(**r) for r in removal_reasons]


def add_removal_reasons(
    remote: SubredditRemovalReasons, reasons: List[LocalRemovalReason]
) -> SubredditRemovalReasons:
    for reason in reasons:
        remote.add(title=reason.title, message=reason.message)


def delete_removal_reasons(remote: SubredditRemovalReasons) -> SubredditRemovalReasons:
    for rr in remote:
        rr.delete()

    return remote


def main(subreddit: praw.models.Subreddit):
    logger.info(
        "Enter modtools.removal_reasons; "
        f"update removal reasons on r/{subreddit.display_name}"
    )

    local = get_local_removal_reasons(REMOVAL_REASONS_YAML)
    remote = subreddit.mod.removal_reasons

    logger.info("Delete existing removal reasons")
    delete_removal_reasons(remote)

    logger.info("Upload local removal reasons")
    add_removal_reasons(remote, reasons=local)
