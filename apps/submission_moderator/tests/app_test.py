# -*- coding: utf-8 -*-
"""Unit test submission_moderator app
"""
import unittest

from packaging.version import parse

from submission_moderator import __version__
from app import app, ROOT


class AppTest(unittest.TestCase):
    """Unit test expected behavior of app
    """

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_api(self):
        """Unit test expected behavior of submission_moderator API
        status request
        """
        response = self.client.get(f"/{ROOT}")
        assert response.status_code == 200

    def test_api_version(self):
        """Unit test expected behavior of submission_moderator API
        version request
        """
        response = self.client.get(f"/{ROOT}/version")
        assert response.status_code == 200

        observed_version = parse(response.get_json()["version"])
        assert observed_version == __version__

    def test_api_moderate(self):
        """Unit test expected behavior of submission_moderator API
        moderate post request
        """
        response = self.client.post(
            f"/{ROOT}/moderate", json={"body": {"submission_id": "fhybn3"}}
        )
        assert response.status_code == 200


if __name__ == "__main__":
    unittest.main()
