# -*- coding: utf-8 -*-
"""Wiki Moderator Application
"""
import logging

from libs.wiki_moderator_app import main


logging.basicConfig(
    format=("%(asctime)s.%(msecs)03d UTC | %(levelname)-8s | %(message)s"),
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
