# -*- coding: utf-8 -*-
import os
import subprocess
from time import sleep
import unittest

from libs.shared.authpraw import (
    get_datascience_bot,
    get_SubstantialStrain6,
    get_b3405920,
)
from libs.submission_moderator_app import main


SUBREDDIT_NAME = "datascience_bot_dev"


class TestLiveScenario(unittest.TestCase):
    """Simulate a live scenario on r/datascience_bot_dev
    """

    def setUp(self):
        self.alex = get_SubstantialStrain6()
        self.bobby = get_datascience_bot()
        self.charlie = get_b3405920()
        self.bots = [self.alex, self.bobby, self.charlie]

        print(">>> Set up tests", "-" * 60)
        self.delete_existing_submissions()
        self.delete_existing_comments()
        print("<<< Set up tests", "-" * 60)

    def tearDown(self):
        del self.alex
        del self.charlie

    def delete_existing_submissions(self):
        for reddit in self.bots:
            for submission in reddit.user.me().submissions.new():
                if submission.subreddit.display_name == SUBREDDIT_NAME:
                    print(
                        f"Delete submission '{submission.title}' "
                        f"by u/{submission.author.name} "
                        f"in r/{submission.subreddit.display_name} "
                        f"({submission.permalink})"
                    )
                    submission.delete()

    def delete_existing_comments(self):
        for reddit in self.bots:
            for comment in reddit.user.me().comments.new():
                if comment.subreddit.display_name == SUBREDDIT_NAME:
                    print(
                        f"Delete comment '{comment.body}' "
                        f"by u/{comment.author.name} "
                        f"in r/{comment.subreddit.display_name} "
                        f"({comment.permalink})"
                    )
                    comment.delete()

    def execute_bin(self):
        main(reddit=self.bobby)

    def setup_blog_submission(self):
        return self.charlie.subreddit(SUBREDDIT_NAME).submit(
            title="No thank you, Mr. Pecker",
            url="https://medium.com/@jeffreypbezos/no-thank-you-mr-pecker-146e3922310f",
        )

    def setup_porn_submission(self):
        return self.charlie.subreddit(SUBREDDIT_NAME).submit(
            title="Porn porn porn", url="https://pornhub.com/",
        )

    def setup_troll_submission(self):
        return self.alex.subreddit(SUBREDDIT_NAME).submit(
            title="What should I major in?",
            selftext="This is just a dummy post. I have nothing more to say.",
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
        troll = self.setup_troll_submission()
        video = self.setup_video_submission()
        valid = self.setup_valid_submission()

        self.execute_bin()

        for banned_submission in (blog, porn, troll, video):
            mod_view = self.bobby.submission(banned_submission.id)
            self.assertTrue(mod_view.approved is False)
            self.assertTrue(mod_view.spam is True or mod_view.removed is True)

        valid_mod_view = self.bobby.submission(valid.id)
        self.assertTrue(valid_mod_view.approved is True)
        self.assertTrue(valid_mod_view.banned_by is None)


if __name__ == "__main__":
    unittest.main()
