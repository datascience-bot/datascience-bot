# -*- coding: utf-8 -*-
"""Test the moderate-submissions.py API
"""
from flask import jsonify
import pytest
from werkzeug.exceptions import BadRequest

from datascience_bot.submission_moderator.api import app, ROOT


def test__api(client):
    response = client.get(ROOT)
    assert response.status_code == 200


def test__json_only(client):
    response = client.post(
        "/".join([ROOT, "moderate-submission"]), data={"submission_id": "euot0h"}
    )
    assert response.status_code == 400

    response = client.post(
        "/".join([ROOT, "moderate-submission"]), json={"submission_id": "euot0h"}
    )
    assert response.status_code == 200


def test__moderation(client):
    response = client.post(
        "/".join([ROOT, "moderate-submission"]), json={"submission_id": "euot0h"}
    )
    assert response.status_code == 200
