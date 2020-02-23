# -*- coding: utf-8 -*-
from collections import namedtuple
import pytest

from submission_moderator.api import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            yield client
