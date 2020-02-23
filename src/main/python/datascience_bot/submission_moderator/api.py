# -*- coding: utf-8 -*-
"""API to the submission moderator
"""
import json
import os
from typing import Dict

import praw
from flask import Flask, jsonify, request, abort
from werkzeug.exceptions import BadRequest, InternalServerError

from datascience_bot.authpraw import get_datascience_bot
from . import moderate_submission

app = Flask(__name__)
ROOT = "/api/v0/submission-moderator"


@app.route(ROOT)
def is_available():
    return jsonify({"status": 200})


@app.route(f"{ROOT}/moderate-submission", methods=["POST"])
def moderate_submissions():
    if not request.is_json:
        abort(400, "Input needs to be JSON")

    try:
        print(request.json)
        submission_id = request.json["submission_id"]
    except BadRequest:
        abort(400, "Input needs to be valid json")

    bob = get_datascience_bot()
    submission = bob.submission(submission_id)

    try:
        moderate_submission(submission)
    except Exception as err:
        abort(500, f"Unknown Internal Error: {err}")
    else:
        return jsonify({"status": 200})
