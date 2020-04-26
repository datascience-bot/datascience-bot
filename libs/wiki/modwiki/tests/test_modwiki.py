# -*- coding: utf-8 -*-
"""Unit test modwiki module
"""
from collections import defaultdict
import os
import pathlib
import unittest
from unittest.mock import Mock, create_autospec

import praw

from libs.shared.pram import BaseTestCase
from libs.wiki.modwiki import (
    get_local_wiki,
    create_missing_wikipages,
    content_is_changed,
    update_wikipage,
    update_wiki,
)


SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME")


class TestModWiki(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.local_wiki_dir = "libs/wiki/modwiki/tests/testwiki"

    def setUp(self):
        super().setUp()
        self.wiki = create_autospec(praw.models.reddit.subreddit.SubredditWiki)
        self.wikipage = create_autospec(praw.models.WikiPage)

    def tearDown(self):
        super().tearDown()
        del self.wiki
        del self.wikipage

    def test_get_local_wiki(self):
        """Test behavior to parse the local wiki configuration
        """
        local_wiki = get_local_wiki(parent_dir=self.local_wiki_dir)

        self.assertIsInstance(local_wiki, defaultdict)

        index_name = "index"

        self.assertTrue(index_name in local_wiki.keys())
        self.assertIsInstance(local_wiki[index_name], str)
        self.assertTrue(len(local_wiki[index_name]) > 0)

        missing_page = "arbitrary name!"
        self.assertTrue(missing_page not in local_wiki.keys())
        self.assertTrue(local_wiki[missing_page] == "")

    def test_compare_wikipage_contents(self):
        """Test behavior to compare wiki pages for changes
        """
        result = content_is_changed(remote_md="", local_md="")
        self.assertIsInstance(result, bool)

        # ignore newlines that don't really matter
        result = content_is_changed(remote_md="", local_md="\n\n")
        self.assertIsInstance(result, bool)

    def test_create_missing_wikipages(self):
        local_wiki = defaultdict(str)
        local_wiki["index"] = "index page"
        create_missing_wikipages(self.wiki, local_wiki)

        self.wiki.create.assert_called_once()

    def test_update_wikipage(self):
        """Test behavior to update an individual wiki page
        """
        self.wikipage.content_md = ""
        result = update_wikipage(
            remote_wikipage=self.wikipage, local_md="arbitrary text"
        )

        self.wikipage.edit.assert_called_once()

        assert result is None

    def test_update_wiki_creates_pages(self):
        """Test behavior to update all wiki pages
        """
        local_wiki = get_local_wiki(self.local_wiki_dir)
        local_wiki = defaultdict(str)
        local_wiki["index"] = "arbitrary text"
        local_wiki["getting-started"] = "more arbitrary text"

        update_wiki(remote_wiki=self.wiki, local_wiki=local_wiki)

        self.assertTrue(self.wiki.create.call_count == len(local_wiki.keys()))

    def test_update_wiki_clears_deprecated_pages(self):
        """Test behavior to clear an individual wiki page
        """
        self.wikipage.name = "index"
        self.wikipage.content_md = "arbitrary text"
        self.wiki.__iter__ = Mock(return_value=[self.wikipage].__iter__())

        local_wiki = defaultdict(str)

        update_wiki(remote_wiki=self.wiki, local_wiki=local_wiki)

        self.wikipage.edit.assert_called_once_with(content="")

    def test_update_wiki_commits_only_changes(self):
        """Test that wiki pages are only modified if there is a change
        """
        self.wikipage.name = "index"
        self.wikipage.content_md = "arbitrary text"
        self.wiki.__iter__ = Mock(return_value=[self.wikipage].__iter__())

        local_wiki = defaultdict(str)
        local_wiki["index"] = "arbitrary text"

        update_wiki(remote_wiki=self.wiki, local_wiki=local_wiki)

        self.assertTrue(self.wikipage.edit.called is False)


if __name__ == "__main__":
    unittest.main()
