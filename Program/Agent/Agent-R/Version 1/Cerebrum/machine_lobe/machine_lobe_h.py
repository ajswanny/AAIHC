"""
Agent: Cerebrum::MachineLobe
Copyright (c) 2018, Alexander Joseph Swanson Villares
"""


from Cerebrum.cerebrum import Cerebrum
from Cerebrum.input_lobe.input_lobe_h import InputLobe
from Cerebrum.output_lobe.output_lobe_h import OutputLobe

import pandas
import praw
import praw.models as reddit
from pprint import pprint



# TODO: Implement use of InputLobe, processing, and OutputLobe.

class MachineLobe(Cerebrum):
    """
    The Machine Lobe, derivative of the Cerebrum.
    """


    # Declare global boolean operation controllers.
    engage = bool()
    start_menu_run = bool()


    topic_keywords_bag_path = "Resources/topic_keywords.csv"


    def __init__(self, platform: str, reddit_params: tuple, task: str = "Keyword Analysis and Expression"):
        """

        :param reddit_params:
            The 5-tuple structure 'reddit_params' must always be provided in the order:
                client_id
                client_secret
                user_agent
                username
                password
        """

        # Define the Agent's purpose.
        self.purpose = task


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



    def __init_operation_lobes__(self, work_subreddit: str):

        self.__input_lobe__ = self.__new_InputLobe__(
            reddit_instance= self.reddit_instance,
            subreddit= work_subreddit
        )

        self.__output_lobe__ = self.__new_OutputLobe__(
            reddit_instance= self.reddit_instance,
            subreddit= work_subreddit
        )



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


        return self



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
    def __new_OutputLobe__(reddit_instance: praw.Reddit, subreddit: str):
        """
        A method allowing for customizable creation of OutputLobe objects.

        :param reddit_instance:
        :param subreddit:
        :return:
        """

        return OutputLobe(reddit_instance= reddit_instance, subreddit= subreddit)



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
    def start(self, work_subreddit: str, engage: bool, override: bool= False):
        """
        Begins the process of Work.

        Workflow for KeywordWork algorithm:
            1.  __init_keyword_workflow__
            2.  __setup_process__
                3.  __standard_process__
                    4.  __process_keyword_analysis__

                3.  __stream_process__
                    ...


        :return:
        """

        # Define True condition for 'engage'.
        self.engage = True

        # Define True condition for start menu run-state.
        self.start_menu_run = True


        # Quick formal process override.
        if override:

            self.__init_keyword_workflow__(work_subreddit= work_subreddit)

            return self


        # Output status.
        print("\n", "-" * 100, '\n',
              "The Machine Lobe has been instantiated and initialized.", '\n\n',
              "\t[1] Begin KeywordWork process. \t\t [2] Exit.", '\n',
              )


        while self.start_menu_run:

            # Prompt for desired operation.
            action_choice = input("Option: ")

            if action_choice is 1:

                # Initialize keyword analysis workflow.
                self.__init_keyword_workflow__(work_subreddit= work_subreddit)

                break

            if action_choice is 2:

                # Future implementation.
                pass

            else:

                # Exit program.
                self.start_menu_run = False
                break


        return 0



    def __init_keyword_workflow__(self, work_subreddit: str):
        """

        :return:
        """

        self.start_menu_run = False
        self.__setup_process__(method="standard", work_subreddit= work_subreddit)


        return 0



    def __setup_process__(self, method: str, work_subreddit: str):
        """
        Standard: collect 'hot' Submissions.

        Stream: continuously collect Submissions, perform analysis, and conduct utterance.

        :param method:
        :return:
        """

        if method == "standard":

            self.__standard_process__(work_subreddit= work_subreddit)

        elif method == "stream":

            # Unimplemented.
            pass


        return 0



    def __standard_process__(self, work_subreddit: str):
        """
        Begin work using a standard Submission object retrieval using the "hot" listing type.

        :return:
        """

        # Create InputLobe object to produce Submission metadata for the "news" Subreddit.
        # Create OutputLobe object to handle expression utterance.
        self.__init_operation_lobes__(work_subreddit= work_subreddit)


        # Command collection of Submission objects.
        self.submission_objects = self.__input_lobe__.__collect_submissions__(return_objects= True)


        # Perform keyword-based success probability analysis, yielding a DataFrame with metadata respective analyses.
        self.__process_keyword_analysis__()


        # Perform engagement.
        self.__process_submission_engages__()



        return 0



    def __process_submission_engages__(self):
        """
        Conducts the engagement actions of the Agent.

        :return:
        """

        for index, row in self.keyword_analyses.iterrows():

            if self.__clearance__(self.keyword_analyses.loc[index]):

                # Create and deliver a message for the respective Submission.
                # We provide the Submission object as the actionable Submission and the Submission metadata.
                self.__output_lobe__.submit_submission_expression(
                    actionable_submission= self.keyword_analyses.submission_object[index],
                    content= self.__generate_utterance__(submission_data= self.keyword_analyses.loc[index])
                )





        return 0



    def __clearance__(self, submission_data: pandas.Series):
        """
        Determines if the Agent is to engage in a Submission.

        :return:
        """

        # Initialize a clearance determination.
        clearance = False


        # TODO: Substantial optimization required.
        # Define clearance condition.
        if (submission_data.success_probability and submission_data.intersection_size) > 1:

            print(submission_data.success_probability)
            print(submission_data.intersection_size)
            clearance = True


        return clearance



    def __generate_utterance__(self, submission_data: pandas.Series):
        """
        Generates a message to be submitted to a Reddit Submission.

        :return:
        """



        return str()





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


        self.keyword_analyses = pandas.DataFrame(self.keyword_analyses)


        return 0

    # noinspection PyDictCreation
    def __analyze_subm_keywords__(self, submission: reddit.Submission):
        """
        'Analyze Submission Keywords'

        Performs keyword intersection analysis for the topic keyword collection and a given Submission's keywords.

        :return:
        """

        """
        Although we do not know which specific API to use for keyword analysis, we know that the 
        actionable data provided will be a sequence of identified keywords. Thus, a placer list is defined
        for temporary use.
        """

        # TODO: Implement reliable collection of keywords.

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
        analysis["success_probability"] = self.probability(method= "keyword", values= tuple(analysis.values()))


        # Append Submission object to the analysis.
        analysis["submission_object"] = submission

        # pprint(analysis)


        return analysis



    def __stream_process__(self):
        """

        :return:
        """

        print(self.reddit_instance)


        return 0

