"""
Agent: Cerebrum::MachineLobe
Copyright (c) 2018, Alexander Joseph Swanson Villares
"""


from Cerebrum.cerebrum import Cerebrum
from Cerebrum.input_lobe.input_lobe_h import InputLobe

import pandas
import praw
import praw.models as reddit



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


        # The current platform (i.e., Reddit, Facebook, etc.).
        self.working_platform = platform


        # The PRAW Reddit object.
        self.reddit_instance = praw.Reddit(client_id= reddit_params[0],
                                           client_secret= reddit_params[1],
                                           user_agent= reddit_params[2],
                                           username= reddit_params[3],
                                           password= reddit_params[4])


        # TODO: Define the keywords collection.
        # The collection of manually determined keywords.
        self.keywords = ["apples", "apples", "oranges"]
        self.keywords_container = pandas.Series(self.keywords)


        # TODO: Define the processing of the Standard Process applied to a Submission title and the Topic.
        #   1. Submission Title Keyword Correlation Score


    #-}


    @property
    def __working_platform__(self):
        """
        Provides essential information about the working platform for the instance of the MachineLobe object.

        :return:
        """

        print("The platform for this Agent instance is: Reddit.")

        return self.working_platform




    def __generate_title_vector__(self):
        """
        Generates the Submission title scoring vector.

        :return:
        """


        return 0



    # noinspection PyAttributeOutsideInit
    def start(self, return_submissions: bool= False, override: bool= False):
        """
        Begins the process of Work.

        :return:
        """

        # Quick process override.
        if override:

            self.__action_choice__()

            return self


        # Simply return the array of Submissions if 'return_submissions' is True.
        if return_submissions:

            self.input_lobe = self.__new_InputLobe__(reddit_instance=self.reddit_instance, subreddit="news")

            return self.input_lobe.__collect_submissions__()


        # Output status.
        print("\n", "-" * 100, '\n',
              "The Machine Lobe has been instantiated and initialized.", '\n\n',
              "\t[1] Begin process. \t\t [2] Exit.", '\n',
              )


        # Define True condition
        self.start_menu_run = True


        while self.start_menu_run:

            action_choice = input("Option: ")

            if action_choice:

                self.__action_choice__()

                break

            else:

                self.start_menu_run = False
                break


        return 0



    def __action_choice__(self):
        """

        :return:
        """


        self.start_menu_run = False
        self.__setup_process__(method="standard")


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

        # Command collection of Submission objects.
        self.submission_objects = self.input_lobe.__collect_submissions__(return_objects= True)


        return 0



    def __stream_process__(self):
        """

        :return:
        """

        print(self.reddit_instance)

        return 0



    @staticmethod
    def __new_InputLobe__(reddit_instance: praw.Reddit, subreddit: str):
        """
        A method allowing for customizable creation of InputLobe objects.

        :param reddit_instance:
        :param subreddit:
        :return:
        """

        return InputLobe(reddit_instance= reddit_instance, subreddit= subreddit)



    def __test_functionality__(self):


        self.__analyze_submission__()


        return 0



    def __analyze_submission__(self, submission: reddit.Submission = None):
        """

        :return:
        """

        x = self.submission_objects[0]

        print(vars(x))


        return 0



    def analyze_submissions(self):
        """

        :return:
        """


        for i, submission in self.submission_objects:





            break


        return 0



