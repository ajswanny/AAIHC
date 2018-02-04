"""
Agent: Cerebrum::InputLobe
Copyright (c) 2018, Alexander Joseph Swanson Villares
"""


from Cerebrum.cerebrum import Cerebrum

import praw


class InputLobe(Cerebrum):
    """
    The Input Lobe, derivative of the Cerebrum.
    """


    def __init__(self, reddit_params: tuple):
        """

        :param reddit_params:
            The 5-tuple structure 'reddit_params' must always be provided in the order:
                client_id
                client_secret
                user_agent
                username
                password
        """

        reddit_instance = praw.Reddit(client_id= reddit_params[0],
                                      client_secret= reddit_params[1],
                                      user_agent= reddit_params[2],
                                      username= reddit_params[3],
                                      password= reddit_params[4])
