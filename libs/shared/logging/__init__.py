# -*- coding: utf-8 -*-
import logging


def basicConfig(**kwargs):
    logging.basicConfig(
        format=("%(asctime)s.%(msecs)03d UTC | %(levelname)-8s | %(message)s"),
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        **kwargs
    )
