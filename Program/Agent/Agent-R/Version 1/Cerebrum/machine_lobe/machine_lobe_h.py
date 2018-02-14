"""
Agent: Cerebrum::MachineLobe
Copyright (c) 2018, Alexander Joseph Swanson Villares
"""



from Cerebrum.cerebrum import Cerebrum
from Cerebrum.input_lobe.input_lobe_h import InputLobe
from Cerebrum.output_lobe.output_lobe_h import OutputLobe

from datetime import datetime
import indicoio
import json
import pandas
from pprint import pprint
import praw
import praw.exceptions
import praw.models as reddit
import random
import time




class MachineLobe(Cerebrum):
    """
    The Machine Lobe, derivative of the Cerebrum.
    """

    # TODO: Declare all Class fields here.

    # Declare global boolean operation controllers.
    engage = bool()                 # A boolean value to indicate if the Agent is to engage in utterance with Submissions.
    start_menu_run = bool()         # A boolean value to indicate if the start menu is running.


    # TODO: Complete compilation of ptopic keywords.
    # The location of the collection of topic keywords relative to Puerto Rico and the humanitarian crisis.
    topic_keywords_bag_path = str()

    # The collection of ptopic keywords and their measured relevance to the document.
    __placer__ptopic_kwds__ = pandas.Series()

    # The collection of ptopic keywords.
    ptopic_kwds = tuple()

    # The collection of completed keyword analysis for Reddit Submissions.
    _main_kwd_df = pandas.DataFrame()


    # The tuple of sentences to be used for expression utterance.
    utterance_sentences = tuple(open("Resources/utterance_sentences_(manual).txt").read().splitlines())


    # The authentication for the Indico NLP API.
    indicoio.config.api_key = '43c624474f147b8b777a144807e7ca95'


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
        self.__init_kwd_process_metadata__()


    #-}



    def __init_operation_lobes__(self, work_subreddit: str):

        self._input_lobe = self.__new_InputLobe__(
            reddit_instance= self.reddit_instance,
            subreddit= work_subreddit
        )

        self._output_lobe = self.__new_OutputLobe__(
            reddit_instance= self.reddit_instance,
            subreddit= work_subreddit
        )



    def __init_kwd_process_metadata__(self):
        """
        Init method to initialize all necessary keyword-relative data fields.
        :return:
        """

        # TODO: Define the keywords collection.
        # A temporary definition of the collection of the topic keywords.
        # NOTE: CURRENTLY USING ONLY THE FIRST COLLECTION OF PROBLEM TOPIC KEYWORDS; STILL COMPILING FULL COLLECTION.
        with open("Resources/Problem_Topic_Keywords/v1/topic_keywords.json", 'r') as fp:

            self.__placer__ptopic_kwds__ = pandas.Series(json.load(fp))


        # TODO: Formally define each element.
        # Declare the main operation DataFrame.
        self._main_kwd_df = pandas.DataFrame(
            columns= [
                'document_kwds', 'intersection_size', 'keywords_intersection',
                'submission_id', 'submission_object', 'submission_title',
                'success_probability', 'utterance_content', 'engagement_time'
            ]
        )


        # Define location of the JSON file to periodically store '_main_kwd_df'.
        self.FILEPATH_main_kwd_df_ = "/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/Agent/Agent-R/Version 1/Cerebrum/machine_lobe/Resources/Program_Data_Fields/_main_kwd_df.json"


        return self



    def archive_dataframe(self):
        """
        Currently archives field: '_main_kwd_df'. Future development will see this method allow for the archival of
        any specified Class data field.
        # FIXME: Update.



        # FIXME: UNKNOWN ERROR.



        :return:
        """

        self._main_kwd_df.to_json(path_or_buf = self.FILEPATH_main_kwd_df_)


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
    def __new_OutputLobe__(reddit_instance: praw.Reddit, subreddit: str):
        """
        A method allowing for customizable creation of OutputLobe objects.

        :param reddit_instance:
        :param subreddit:
        :return:
        """

        return OutputLobe(reddit_instance= reddit_instance, subreddit= subreddit)



    @staticmethod
    def intersect(list_x: (list, tuple), list_y: (list, tuple)):
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

        # TODO: Substantial optimization.

        :return:
        """

        if method == "keyword":

            # Initialize a probability measure; this tuple index refers to the sum of the amount of values
            # in the intersection list. That is, the amount of keywords that intersected.
            success_probability = values[3]


            if normalize:

                # Return a probability measure normalized to a range of [0, 1].
                # TODO: Update maximum. This will be the amount of keywords we use for the problem topic.
                return self.normalize(success_probability, minimum= 0, maximum= 800)

            else:

                return success_probability



    def __test_functionality__(self):
        """

        :return:
        """

        print(type(self._main_kwd_df))

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

        # Define True condition for 'engage' if desired.
        if engage:

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


        # Command collection of Submission objects. Note: the '__collect_submissions__' method operates on the default
        # Subreddit for the InputLobe instance, which is defined by the 'work_subreddit' parameter for the call to
        # '__init_operation_lobes__' method.
        self.submission_objects = self._input_lobe.__collect_submissions__(return_objects= True, fetch_limit= 1)


        # Perform keyword-based success probability analysis, yielding a DataFrame with metadata respective analyses.
        self.__process_keyword_analysis__()


        if self.engage:

            # Perform engagement, determining for every Submission if it should be engaged and following through if so.
            self.__process_submission_engages__()


            # Redefine 'engage' boolean controller.
            self.engage = False


        # Archive '_main_kwd_df'.
        # FIXME: UNKNOWN ERROR.
        # self.archive_dataframe()


        return 0



    def __process_submission_engages__(self):
        """
        Conducts the engagement actions of the Agent.

        :return:
        """

        def out(x: tuple):

            self._output_lobe.submit_submission_expression(x[0], x[1])


        for index, row in self._main_kwd_df.iterrows():

            if self.__clearance__(self._main_kwd_df.loc[index]):

                # Generate the utterance message.
                utterance_message = self.__generate_utterance__(submission_data= self._main_kwd_df.loc[index])


                # Define container of data for operation of Submission engage.
                operation_fields = (self._main_kwd_df.submission_object[index], utterance_message)


                # Archive the utterance message content.
                self._main_kwd_df.at[index, "utterance_content"] = utterance_message


                try:

                    # Create and deliver a message for the respective Submission.
                    # We provide the Submission object as the actionable Submission and the Submission metadata.
                    out(operation_fields)

                except praw.exceptions.APIException as E:

                    # Output error details and delay operation.
                    print("Caught error: ", E.message, "\nWaiting...")
                    time.sleep(600)

                finally:

                    out(operation_fields)


                # Record the engagement time.
                self._main_kwd_df.at[index, "engagement_time"] = str(datetime.now())


                break


        return 0



    @staticmethod
    def __clearance__(submission_data: pandas.Series):
        """
        Determines if the Agent is to engage in a Submission, observing the Submission metadata.

        # TODO: Substantial optimization.

        :return:
        """

        # Initialize a clearance determination.
        clearance = False


        # Define clearance condition.
        # FIXME: Currently using a naive measure of success probability and an intersection size of
        # FIXME: greater than 1. Must determine the final versions of this part of the algorithm.
        if (submission_data.success_probability and submission_data.intersection_size) > 1:

            print(submission_data.success_probability)
            print(submission_data.intersection_size)
            clearance = True


        return clearance



    def __generate_utterance__(self, submission_data: pandas.Series):
        """
        Generates a message to be submitted to a Reddit Submission.

        Currently selecting a random choice, further versions will implement more intelligent utterance generation.

        # TODO: Substantial optimization.

        :return:
        """

        # Option:
        #   - Define utterance choice to be generated by considering which of the sample sentences are most similar to
        #     a respective Submission title.


        return random.choice(self.utterance_sentences)



    def __process_keyword_analysis__(self):
        """
        A mid-level management method for keyword-based success probability analysis.
        The purpose of this method is to allow for the monitoring of the keyword-based
        analysis loop and provide accessibility to intervention for optimization or
        modification.

        :return:
        """

        # Create temporary container for keyword analyses.
        __temp__keyword_analyses = []


        # Analyze every Submission collected, appending each analysis to '_main_kwd_df'.
        for submission in self.submission_objects:

            __temp__keyword_analyses.append(self.__analyze_subm_kwds__(submission))

            # FIXME: Break statement here to debug Indico API embedded functionality.
            break


        # Redefine the main KWD DataFrame to contain all keyword analyses.
        __temp__keyword_analyses = pandas.DataFrame(__temp__keyword_analyses)

        self._main_kwd_df = pandas.concat([self._main_kwd_df, __temp__keyword_analyses])


        return 0



    # noinspection PyDictCreation
    def __analyze_subm_kwds__(self, submission: reddit.Submission):
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
        # TODO: Select API.

        # TODO: Determine if we want to make use of the relevance to document of keywords provided by the Indico NLP API.
        # TODO: Determine if we want to implement use of the linked article.
        # TODO: Determine if we want to incorporate the use of "KEYWORD PHRASES," not just keywords.

        # TODO: Create normalization function for keyword collections.


        # Define the keywords for the given Submission title.
        # NOTE: CURRENTLY USING JUST THE KEYWORDS GIVEN; NOT INCLUDING THEIR LIKELY RELEVANCE.
        document_keyword_analysis = indicoio.keywords(submission.title)
        document_keywords = tuple(document_keyword_analysis.keys())



        # Define the intersection of the topic keywords bag and the Submission's keywords.
        intersection = self.intersect(self.ptopic_kwds, document_keywords)


        # Initialize the keyword intersection count.
        keywords_intersections_count = len(intersection)


        # Define a structure to contain all measures relevant to analysis.
        analysis = {
            "submission_id": submission.id,
            "submission_title": submission.title,
            "keywords_intersection": intersection,
            "intersection_size": keywords_intersections_count,
            "document_kwds": document_keywords
        }


        # Define a probability measure of success and append this to the 'analysis' dictionary.
        # This figure is used to determine whether or not the Agent will submit a textual expression
        # to a Reddit Submission.
        # TODO: This measure is to be optimized in the future.
        analysis["success_probability"] = self.probability(method= "keyword", values= tuple(analysis.values()))


        # Append Submission object to the analysis.
        analysis["submission_object"] = submission


        return analysis



    def __stream_process__(self):
        """

        :return:
        """

        print(self.reddit_instance)


        return 0
