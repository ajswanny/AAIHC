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


    def __init__(self, reddit_instance: praw.Reddit):
        """

        """


        self.reddit_instance = reddit_instance

        self.__test_functionality__()




    #-}


    def __test_functionality__(self):


        print(self.reddit_instance.auth)

        submission = self.reddit_instance.submission(id="7v6jp6")

        print(submission.title)

        # for submission in self.reddit_instance.subreddit('news').hot(limit=10):
        #
        #     print(submission.id)


        return 0