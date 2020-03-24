# -*- coding: utf-8 -*-
"""Test authpraw.py module
"""
import unittest

from authpraw import get_datascience_bot, get_SubstantialStrain6, get_b3405920


class TestGetUser(unittest.TestCase):
    """Unit test expected behavior to get user profiles
    """

    def get_datascience_bot_test(self):
        redditor = get_datascience_bot()
        self.assertEqual(redditor.user.me(), "datascience-bot")

    def get_SubstantialStrain6_test(self):
        redditor = get_SubstantialStrain6()
        self.assertEqual(redditor.user.me(), "SubstantialStrain6")

    def get_b3405920_test(self):
        redditor = get_b3405920()
        self.assertEqual(redditor.user.me(), "b3405920")


if __name__ == "__main__":
    unittest.main()
