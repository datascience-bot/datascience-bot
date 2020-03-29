# -*- coding: utf-8 -*-
import os
import subprocess
from time import sleep
import unittest

from authpraw import get_datascience_bot, get_SubstantialStrain6, get_b3405920


SUBREDDIT_NAME = "datascience_bot_dev"


class TestLiveScenario(unittest.TestCase):
    """Simulate a live scenario on r/datascience_bot_dev
    """

    @classmethod
    def setUpClass(cls):
        alex = get_SubstantialStrain6()
        bobby = get_datascience_bot()
        charlie = get_b3405920()

        for reddit in (alex, bobby, charlie):
            for submission in reddit.user.me().submissions.new():
                if submission.subreddit.display_name == SUBREDDIT_NAME:
                    print(
                        f"Delete '{submission.title}' "
                        f"by u/{submission.author.name} "
                        f"in r/{submission.subreddit.display_name} "
                        f"({submission.url})"
                    )
                    submission.delete()

    def setUp(self):
        self.alex = get_SubstantialStrain6()
        self.bobby = get_datascience_bot()
        self.charlie = get_b3405920()

    def tearDown(self):
        del self.alex
        del self.charlie

    def execute_bin(self):
        args = ("apps/submission_moderator_app/bin",)
        popen = subprocess.Popen(args, stdout=subprocess.PIPE)
        popen.wait()
        output = popen.stdout.read()

    def setup_blog_submission(self):
        return self.charlie.subreddit(SUBREDDIT_NAME).submit(
            title="No thank you, Mr. Pecker",
            url="https://medium.com/@jeffreypbezos/no-thank-you-mr-pecker-146e3922310f",
        )

    def setup_porn_submission(self):
        return self.charlie.subreddit(SUBREDDIT_NAME).submit(
            title="Porn porn porn", url="https://pornhub.com/",
        )

    def setup_valid_submission(self):
        return self.charlie.subreddit(SUBREDDIT_NAME).submit(
            title="What's the deal with ML engineering?",
            selftext="This is just a dummy post. I have nothing more to say.",
        )

    def setup_video_submission(self):
        return self.charlie.subreddit(SUBREDDIT_NAME).submit(
            title="80s Remix: Tronicbox 'Somebody That I Used To Know' Gotye",
            url="https://www.youtube.com/watch?v=-qstIEHDVRg",
        )

    def test_scenario(self):
        blog = self.setup_blog_submission()
        porn = self.setup_porn_submission()
        video = self.setup_video_submission()
        valid = self.setup_valid_submission()

        self.execute_bin()

        for banned_submission in (blog, porn, video):
            mod_view = self.bobby.submission(banned_submission.id)
            self.assertTrue(mod_view.approved is False)
            self.assertTrue(mod_view.spam is True or mod_view.removed is True)

        valid_mod_view = self.bobby.submission(valid.id)
        self.assertTrue(valid_mod_view.approved is True)
        self.assertTrue(valid_mod_view.banned_by is None)


if __name__ == "__main__":
    unittest.main()
