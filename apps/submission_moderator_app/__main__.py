# -*- coding: utf-8 -*-
import logging

from apps.submission_moderator_app import main


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


if __name__ == "__main__":
    main()
