"""
Agent: Cerebrum::MachineLobe
Copyright (c) 2018, Alexander Joseph Swanson Villares
"""


from Cerebrum.cerebrum import Cerebrum
from Cerebrum.input_lobe.input_lobe_h import InputLobe

import pandas
import praw
from os import system


# TODO: Implement use of InputLobe, processing, and OutputLobe.

class MachineLobe(Cerebrum):
    """
    The Machine Lobe, derivative of the Cerebrum.
    """


    def __init__(self, platform: str, reddit_params: tuple):
        """

        :param reddit_params:
            The 5-tuple structure 'reddit_params' must always be provided in the order:
                client_id
                client_secret
                user_agent
                username
                password
        """


        self.working_platform = platform


        self.reddit_instance = praw.Reddit(client_id= reddit_params[0],
                                           client_secret= reddit_params[1],
                                           user_agent= reddit_params[2],
                                           username= reddit_params[3],
                                           password= reddit_params[4])

    #-}


    @property
    def __working_platform__(self):
        """
        Provides essential information about the working platform for the instance of the MachineLobe object.

        :return:
        """

        return self.working_platform



    def start(self):
        """

        :return:
        """


        print("\n", "-" * 100, '\n',
              "The Machine Lobe has been instantiated and initialized.", '\n\n',
              "\t[1] Begin process. \t\t [2] Exit.", '\n',
              )


        start_menu_run = True


        while start_menu_run:

            action_choice = input("Option: ")

            if action_choice:

                start_menu_run = False
                self.__setup_process__(method= "standard")

                break

            else:

                start_menu_run = False
                break


        return 0


    def __setup_process__(self, method: str):
        """

        :param method:
        :return:
        """

        if method == "standard":

            self.__standard_process__()

        elif method == "stream":

            # Unimplemented.
            return


        return 0


    def __standard_process__(self):
        """
        Begin work using a standard Submission object retrieval using the "hot" listing type.

        :return:
        """


        # Create InputLobe object to produce Submission metadata.
        self.input_lobe = self.__new_InputLobe__(reddit_instance= self.reddit_instance, subreddit= "news")


        # Retrieve


        return 0



    def __stream_process__(self):
        """

        :return:
        """

        return 0



    @staticmethod
    def __new_InputLobe__(reddit_instance, subreddit):
        """
        A method allowing for customizable creation of InputLobe objects.

        :param reddit_instance:
        :param subreddit:
        :return:
        """

        return InputLobe(reddit_instance= reddit_instance, subreddit= subreddit)
