import unittest

from libs.wiki_moderator_app import WIKI_DIR


class TestWikiContent(unittest.TestCase):
    def test_markdown_suffix(self):
        for p in WIKI_DIR.glob("*"):
            if p.suffix != ".md":
                self.fail("Only markdown files will go be used to moderate the wiki")


if __name__ == "__main__":
    unittest.main()
