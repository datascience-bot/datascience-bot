# -*- coding: utf-8 -*-
"""Unit test removal reasons configuration
"""
import unittest
from unittest.mock import Mock, create_autospec

from praw.models.reddit.removal_reasons import RemovalReason, SubredditRemovalReasons

from libs.modtools.removal_reasons import (
    REMOVAL_REASONS_YAML,
    LocalRemovalReason,
    get_local_removal_reasons,
    add_removal_reasons,
    delete_removal_reasons,
)


class TestRemovalReasons(unittest.TestCase):
    def test_get_local_removal_reasons(self):
        reasons = get_local_removal_reasons(p=REMOVAL_REASONS_YAML)

        self.assertIsInstance(reasons, list)
        for reason in reasons:
            self.assertIsInstance(reason, LocalRemovalReason)

    def test_delete_removal_reasons(self):
        removal_reason = create_autospec(RemovalReason)
        removal_reasons = create_autospec(SubredditRemovalReasons)
        removal_reasons.__iter__ = Mock(return_value=[removal_reason].__iter__())

        delete_removal_reasons(remote=removal_reasons)

        removal_reason.delete.assert_called_once()

    def test_add_removal_reasons(self):
        removal_reasons = create_autospec(SubredditRemovalReasons)

        add_removal_reasons(
            remote=removal_reasons,
            reasons=[
                LocalRemovalReason(title="arbitrary title", message="arbitrary message")
            ],
        )

        self.assertTrue(removal_reasons.add.called is True)


if __name__ == "__main__":
    unittest.main()
