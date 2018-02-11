"""
Agent: Cerebrum::OutputLobe
Copyright (c) 2018, Alexander Joseph Swanson Villares
"""


from Cerebrum.cerebrum import Cerebrum

import praw
import praw.models as reddit


class OutputLobe(Cerebrum):
    """
    The Output Lobe, derivative of the Cerebrum.
    """


    def __init__(self, reddit_instance: praw.Reddit, **kwargs):
        """

        :param reddit_instance:
        :param kwargs:
        """

        # Define the Reddit instance.
        self.reddit_instance = reddit_instance

        # Define default working Subreddit if provided in object instantiation.
        if "subreddit" in kwargs:

            self.default_subreddit = self.reddit_instance.subreddit(display_name=kwargs["subreddit"])

        else:

            self.default_subreddit = self.reddit_instance.subreddit("news")



    def submit_submission_expression(self, actionable_submission: reddit.Submission, content: str):
        """
        A high-level management function to oversee expression utterance for Reddit Submissions.

        :param actionable_submission:
        :param content:
        :return:
        """

        # Perform expression utterance to the given Reddit Submission.
        actionable_submission.reply(

            content

        )


        return self
