# -*- coding: utf-8 -*-
"""Configure a REST API endpoint for submission_moderator
"""
from flask import Flask, jsonify, make_response, request

from authpraw import get_datascience_bot
from . import __version__, SubmissionModerator, get_submission

ROOT: str = "submission_moderator"
app = Flask(__name__)


@app.route(f"/{ROOT}")
def get_status():
    return "200 OK"


@app.route(f"/{ROOT}/version")
def get_version():
    return {"version": __version__.public}


@app.route(f"/{ROOT}/moderate", methods=["POST"])
def post_moderate_submission():
    submission_id = request.json["body"]["submission_id"]

    bob = get_datascience_bot()
    submission = get_submission(submission_id, bob)
    moderator = SubmissionModerator(bob)
    moderator.moderate(submission)

    return "200 OK"


if __name__ == "__main__":
    app.run()
