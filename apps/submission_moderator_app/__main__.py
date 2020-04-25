# -*- coding: utf-8 -*-
import argparse
import logging

from apps.submission_moderator_app import main
from libs.shared.authpraw import get_datascience_bot


logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info("Enter submission_moderator_app")
    reddit = get_datascience_bot()
    main(reddit=reddit)
