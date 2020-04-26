# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from time import sleep
import unittest

from libs.entering_and_transitioning_app import (
    SubmissionAuthor,
    main,
)
from libs.shared.authpraw import (
    get_datascience_bot,
    get_SubstantialStrain6,
    get_b3405920,
)


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
        del self.bobby
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

    def setup_last_thread(self, time: datetime):
        subreddit = self.bobby.subreddit(SUBREDDIT_NAME)
        author = SubmissionAuthor(subreddit)

        submission = author.submit_thread(time)

        # setup comment with replies
        comment = self.charlie.submission(submission.id).reply(
            "What should I major in?"
        )
        self.alex.comment(comment.id).reply("CS or something")

        # setup comment with no replies
        self.alex.submission(submission.id).reply("How do I become a data scientist?")

    def test_scenario(self):
        time = datetime.strptime("2019-07-07", "%Y-%m-%d")
        self.setup_last_thread(time)

        sleep(3)  # give a fews secs for Reddit's servers to update

        main(
            reddit=self.bobby,
            subreddit_name=SUBREDDIT_NAME,
            time=(time + timedelta(days=7)),
            validate=False,
        )


if __name__ == "__main__":
    unittest.main()
