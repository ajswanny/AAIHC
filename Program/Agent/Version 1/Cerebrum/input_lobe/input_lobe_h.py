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


    #-}



