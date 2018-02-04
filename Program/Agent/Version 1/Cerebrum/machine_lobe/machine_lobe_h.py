"""
Agent: Cerebrum::MachineLobe
Copyright (c) 2018, Alexander Joseph Swanson Villares
"""


from Cerebrum.cerebrum import Cerebrum

import praw
from os import system


# TODO: Implement use of InputLobe, processing, and OutputLobe.

class MachineLobe(Cerebrum):
    """
    The Machine Lobe, derivative of the Cerebrum.
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

    #-}



    def start(self):
        """

        :return:
        """


        print("\n", "-" * 100, '\n',
              "The Machine Lobe has been instantiated and initialized.", '\n\n',
              "\t[1] Begin process. \t\t [2] Exit.", '\n',
              )


        action_choice = int()


        while 1:

            int_in = input(" Make a selection: ")
            action_choice = int_in

            if action_choice == 1:

                self.setup_process(method= "standard")

                break

            elif action_choice == 2:

                break


        return 0


    def setup_process(self, method: str):
        """

        :param method:
        :return:
        """

        if method == "standard":

            self.standard_process()

        elif method == "stream":

            # Unimplemented.
            return


        return 0


    def standard_process(self):
        """
        Begin work using a standard Submission object retrieval using the "hot" listing type.

        :return:
        """





        return 0


    def stream_process(self):
        """

        :return:
        """

        return 0