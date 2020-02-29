# -*- coding: utf-8 -*-
"""Authenticate u/datascience-bot with praw
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


