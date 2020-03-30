# -*- coding: utf-8 -*-
"""Authenticate praw sessions for
- u/datascience-bot
- u/SubstantialStrain6
- u/b3405920
"""
import os
import praw


def get_datascience_bot():
    return praw.Reddit(
        username=os.getenv("DATASCIENCE_BOT_USERNAME"),
        password=os.getenv("DATASCIENCE_BOT_PASSWORD"),
        client_id=os.getenv("DATASCIENCE_BOT_CLIENT_ID"),
        client_secret=os.getenv("DATASCIENCE_BOT_CLIENT_SECRET"),
        user_agent="u/datascience-bot",
    )


def get_SubstantialStrain6():
    return praw.Reddit(
        username=os.getenv("SUBSTANTIALSTRAIN6_USERNAME"),
        password=os.getenv("SUBSTANTIALSTRAIN6_PASSWORD"),
        client_id=os.getenv("SUBSTANTIALSTRAIN6_CLIENT_ID"),
        client_secret=os.getenv("SUBSTANTIALSTRAIN6_CLIENT_SECRET"),
        user_agent="u/SubstantialStrain6",
    )


def get_b3405920():
    return praw.Reddit(
        username=os.getenv("B3405920_USERNAME"),
        password=os.getenv("B3405920_PASSWORD"),
        client_id=os.getenv("B3405920_CLIENT_ID"),
        client_secret=os.getenv("B3405920_CLIENT_SECRET"),
        user_agent="u/b3405920",
    )
