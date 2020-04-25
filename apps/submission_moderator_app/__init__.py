# -*- coding: utf-8 -*-
"""Fetch new submissions and moderate accordingly
"""
import logging

from libs.submission_moderator_app import main


logging.basicConfig(
    format=("%(asctime)s.%(msecs)03d UTC | %(levelname)-8s | %(message)s"),
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
