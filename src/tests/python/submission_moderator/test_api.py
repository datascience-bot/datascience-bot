# -*- coding: utf-8 -*-
"""Unit test submission_moderator REST API
"""
from packaging.version import parse

from submission_moderator import __version__
from submission_moderator.api import app, ROOT


def test_api(client):
    """Unit test expected behavior of submission_moderator API 
    status request
    """
    response = client.get(f"/{ROOT}")
    assert response.status_code == 200


def test_api_version(client):
    """Unit test expected behavior of submission_moderator API 
    version request
    """
    response = client.get(f"/{ROOT}/version")
    assert response.status_code == 200

    observed_version = parse(response.get_json()["version"])
    assert observed_version == __version__


def test_api_moderate(client):
    """Unit test expected behavior of submission_moderator API 
    moderate post request
    """
    response = client.post(
        f"/{ROOT}/moderate", json={"body": {"submission_id": "fhybn3"}}
    )
    assert response.status_code == 200
