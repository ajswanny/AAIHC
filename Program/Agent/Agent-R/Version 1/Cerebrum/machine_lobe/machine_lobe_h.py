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

        # The current platform (i.e., Reddit, Facebook, etc.).
        self.working_platform = platform


        # The PRAW Reddit object.
        self.reddit_instance = praw.Reddit(
            client_id= reddit_params[0],
            client_secret= reddit_params[1],
            user_agent= reddit_params[2],
            username= reddit_params[3],
            password= reddit_params[4]
        )


        # Initialize dependencies for keyword analysis.
        self.__init_keyword_metadata__()


    #-}



    def __init_keyword_metadata__(self):
        """
        Init method to initialize all necessary keyword-relative data fields.
        :return:
        """

        # TODO: Define the keywords collection.
        # A temporary definition of the collection of the topic keywords.
        df = pandas.read_csv("Resources/topic_keywords.csv")
        self.placer__keywords_bag = tuple(df.columns.values)


        # Declare new list to contain all keyword analyses for Submissions.
        self.keyword_analyses = []


        return 0



    @staticmethod
    def __new_InputLobe__(reddit_instance: praw.Reddit, subreddit: str):
        """
        A method allowing for customizable creation of InputLobe objects.

        :param reddit_instance:
        :param subreddit:
        :return:
        """

        return InputLobe(reddit_instance=reddit_instance, subreddit=subreddit)



    @staticmethod
    def intersect(list_x: (list, tuple), list_y: list):
        """

        :param list_x:
        :param list_y:
        :return:
        """

        return list(set(list_x) & set(list_y))



    @staticmethod
    def normalize(value, minimum, maximum):
        """

        :param value:
        :param minimum:
        :param maximum:
        :return:
        """

        numerator = value - minimum
        denominator = maximum - minimum


        return numerator / denominator



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



    def __test_functionality__(self):
        """

        :return:
        """


        return 0



    # noinspection PyAttributeOutsideInit
    def start(self, return_submissions: bool= False, override: bool= False):
        """
        Begins the process of Work.

        :return:
        """

        # Quick formal process override.
        if override:

            self.__action_choice__()

            return self


        # Simply return the array of Submissions if 'return_submissions' is True.
        if return_submissions:

            self.__input_lobe__ = self.__new_InputLobe__(reddit_instance= self.reddit_instance, subreddit="news")

            return self.__input_lobe__.__collect_submissions__()


        # Output status.
        print("\n", "-" * 100, '\n',
              "The Machine Lobe has been instantiated and initialized.", '\n\n',
              "\t[1] Begin KeywordWork process. \t\t [2] Exit.", '\n',
              )


        # Define True condition for start menu run-state.
        self.start_menu_run = True


        while self.start_menu_run:

            action_choice = input("Option: ")

            if action_choice is 1:

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
            pass


        return 0



    def __standard_process__(self):
        """
        Begin work using a standard Submission object retrieval using the "hot" listing type.

        :return:
        """

        # Create InputLobe object to produce Submission metadata.
        self.__input_lobe__ = self.__new_InputLobe__(reddit_instance= self.reddit_instance, subreddit="news")


        # Command collection of Submission objects.
        self.submission_objects = self.__input_lobe__.__collect_submissions__(return_objects= True)


        # Perform keyword-based success probability analysis.
        self.__process_keyword_analysis__()


        return 0



    def __stream_process__(self):
        """

        :return:
        """

        print(self.reddit_instance)


        return 0



    def __process_keyword_analysis__(self):
        """
        A mid-level management method for keyword-based success probability analysis.
        The purpose of this method is to allow for the monitoring of the keyword-based
        analysis loop and provide accessibility to intervention for optimization or
        modification.

        :return:
        """

        # Analyze every Submission collected, appending each analysis to 'keyword_analyses'.
        for submission in self.submission_objects:

            self.keyword_analyses.append(self.__analyze_subm_keywords__(submission))


        return 0



    def __analyze_subm_keywords__(self, submission: reddit.Submission):
        """
        Performs keyword intersection analysis for the topic keyword collection and a given Submission's keywords.

        :return:
        """

        """
        Although we do not know which specific API to use for keyword analysis, we know that the 
        actionable data provided will be a sequence of identified keywords. Thus, a placer list is defined
        for temporary use.
        """

        #-
        __placer__keywords = ["alpha", "beta", "omega", "charlie", "foxtrot"]
        #-


        # Define the intersection of the topic keywords bag and the Submission's keywords.
        intersection = self.intersect(self.placer__keywords_bag, __placer__keywords)


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
