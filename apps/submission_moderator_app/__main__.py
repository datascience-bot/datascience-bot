# -*- coding: utf-8 -*-
import logging

from libs.submission_moderator_app import main
from libs.shared.authpraw import get_datascience_bot


logging.basicConfig(
    format=("%(asctime)s.%(msecs)03d UTC | %(levelname)-8s | %(message)s"),
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info("Enter submission_moderator_app")
    reddit = get_datascience_bot()
    main(reddit=reddit)
