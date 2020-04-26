import unittest

from libs.shared.authpraw import get_datascience_bot
from libs.modtools.removal_reasons import main


class TestPrawIntegration(unittest.TestCase):
    def test_main(self):
        bobby = get_datascience_bot()
        subreddit = bobby.subreddit("datascience_bot_dev")
        main(subreddit=subreddit)


if __name__ == "__main__":
    unittest.main()
