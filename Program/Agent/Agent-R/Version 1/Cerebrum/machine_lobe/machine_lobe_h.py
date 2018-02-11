"""
Agent: Cerebrum::MachineLobe
Copyright (c) 2018, Alexander Joseph Swanson Villares
"""


from Cerebrum.cerebrum import Cerebrum
from Cerebrum.input_lobe.input_lobe_h import InputLobe

import pandas
import praw
import praw.models as reddit
from pprint import pprint



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

        # TODO: Define the keywords collection.
        # A temporary definition of the collection of the topic keywords.
        self.placer__keywords_bag = ["alpha", "beta", "omega"]


        # The current platform (i.e., Reddit, Facebook, etc.).
        self.working_platform = platform


        # The PRAW Reddit object.
        self.reddit_instance = praw.Reddit(client_id= reddit_params[0],
                                           client_secret= reddit_params[1],
                                           user_agent= reddit_params[2],
                                           username= reddit_params[3],
                                           password= reddit_params[4])


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



    def __test_functionality__(self):
        """

        :return:
        """


        return 0



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

        # Perform keyword-based success probability analysis.
        self.__process_keyword_analysis__()


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



    @staticmethod
    def __intersect__(list_x: list, list_y: list):
        """

        :param list_x:
        :param list_y:
        :return:
        """

        return list(set(list_x) & set(list_y))



    @staticmethod
    def normalize(value, minimum, maximum):


        numerator = value - minimum
        denominator = maximum - minimum


        return numerator/denominator



    def probability(self, method: str, values: tuple, normalize: bool= True):
        """
        Calculates the probability of success, judging this measure with respect to the intersection
        of keywords of the base keyword set and a given Submission title's keywords.

        At the moment, this measure is obtained simply and naively from the length of the intersection
        of the base keyword set and a given Submission title's keyword set.

        :return:
        """

        # TODO: Perform substantial optimization.


        if method == "keyword":

            # Initialize a probability measure; this tuple index refers to the sum of the amount of values
            # in the intersection list. That is, the amount of keywords that intersected.
            success_probability = values[3]


            if normalize:

                # Return a probability measure normalized to a range of [0, 1].
                return self.normalize(success_probability, minimum= 0, maximum= 800)

            else:

                return success_probability



    def __keyword_analysis__(self):
        """
        A high-level management method for keyword-based success probability analysis.

        :return:
        """

        # Call loop-handler for keyword-based analysis.
        self.__process_keyword_analysis__()

        return self



    def __process_keyword_analysis__(self):
        """
        A mid-level management method for keyword-based success probability analysis.
        The purpose of this method is to allow for the monitoring of the keyword-based
        analysis loop and provide accessibility to intervention for optimization or
        modification.

        :return:
        """

        # Declare new field to contain all keyword analyses for Submissions.
        self.keyword_analyses = []


        # Analyze every Submission collected, appending each analysis to 'analyses'.
        for submission in self.submission_objects:

            self.keyword_analyses.append(self.__analyze_submission_keywords__(submission))


        return 0



    def __analyze_submission_keywords__(self, submission: reddit.Submission):
        """

        :return:
        """

        """
        Although we do not know which specific API to use for keywords analysis, we know that the 
        actionable data provided will be a sequence of identified keywords. Thus, a placer list is defined
        for temporary use.
        """

        #-
        __placer__keywords = ["alpha", "beta", "omega", "charlie", "foxtrot"]
        #-


        # Define the intersection of the topic keywords bag and the Submission's keywords.
        intersection = self.__intersect__(self.placer__keywords_bag, __placer__keywords)


        # Initialize the keyword intersection count.
        keywords_intersections_count = len(intersection)


        # Define a structure to contain all measures relevant to analysis.
        analysis = {
            "submission_id": submission.id,
            "submission_title": submission.title,
            "keywords_intersection": intersection,
            "intersection_size": keywords_intersections_count,
        }


        # Define a probability measure of success and append this to the 'analysis' dictionary.
        # This figure is used to determine whether or not the Agent will submit a textual expression
        # to a Reddit Submission.
        analysis["success_probability"] = self.probability(tuple(analysis.values()))


        # pprint(analysis)


        return analysis



