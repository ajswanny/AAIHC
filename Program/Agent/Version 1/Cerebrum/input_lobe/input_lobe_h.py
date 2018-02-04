"""
Agent: Cerebrum::InputLobe
Copyright (c) 2018, Alexander Joseph Swanson Villares
"""


from Cerebrum.cerebrum import Cerebrum

import praw


# TODO: Implement data input.

class InputLobe(Cerebrum):
    """
    The Input Lobe, derivative of the Cerebrum.
    """


    def __init__(self, reddit_instance: praw.Reddit, **kwargs):
        """

        """

        # Define the Reddit instance.
        self.reddit_instance = reddit_instance


        # Define default working Subreddit if provided in object instantiation.
        if "subreddit" in kwargs:

            self.default_subreddit = reddit_instance.subreddit(display_name= kwargs["subreddit"])


        self.__test_functionality__()




    #-}


    def __test_functionality__(self):


        print(self.reddit_instance.auth)

        submission = self.reddit_instance.submission(id="7v6jp6")

        print(submission.title)

        # for submission in self.reddit_instance.subreddit('news').hot(limit=10):
        #
        #     print(submission.id)

        for submission in self.default_subreddit.hot():
            print(submission.title)


        return 0

    def __collect_submission_ids__(self, listing_type: str):






        return 0