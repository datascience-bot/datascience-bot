# -*- coding: utf-8 -*-
"""Test authpraw.py module
"""
import unittest

from authpraw import get_datascience_bot


class TestGetUser(unittest.TestCase):
    """Unit test expected behavior to get user profiles
    """

    def test_get_datascience_bot(self):
        redditor = get_datascience_bot()
        self.assertEqual(redditor.user.me(), "datascience-bot")


if __name__ == "__main__":
    unittest.main()
