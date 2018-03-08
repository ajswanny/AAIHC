from Cerebrum.input_lobe.input_lobe_h import InputLobe
from Cerebrum.output_lobe.output_lobe_h import OutputLobe
from r_submission_h import RSubmission
from machine_lobe.Excpetions import SubmissionAnalysisError
from indicoio.utils.errors import IndicoError

import _pickle as pickle
import indicoio
import json
import pandas
import praw
import praw.exceptions
import praw.models as reddit
import time
from datetime import datetime
from indicoio.utils import errors as indicoio_errors
from pprint import pprint
from nltk.corpus import stopwords as nltk_stopwords


# noinspection PyCompatibility
class SubredditStreamMachine:
    """
    Allows for the handling of the Submission stream for a specified Subreddit.
    """

    # The DataFrame containing all current-work Submission data.
    main_df: pandas.DataFrame = pandas.DataFrame()

    # The DataFrame containing historical Submission data.
    historical_df = pandas.DataFrame()

    # The tuple containing English stop words.
    stop_words = tuple(nltk_stopwords.words('english'))

    # The authentication for the Indico NLP API.
    indicoio.config.api_key = '43c624474f147b8b777a144807e7ca95'

    # The filepath for the aggregate DataFrame.
    FP_aggregate_archive = \
        "/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/Agent/Agent-R/Version 1/Cerebrum/SubredditStreamMachine/Resources/StreamProcessDependencies/aggregate_archive.json"


    # The location for the final archive.
    FP_final_archive = str()


    def __init__(
            self,
            operate_recursively: bool,
            instance_id: str,
            instance_num: int,
            platform: str,
            reddit_params: tuple,
            task: str = "Keyword and Relevance Analysis and Expression"
    ):
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
            client_id=reddit_params[0],
            client_secret=reddit_params[1],
            user_agent=reddit_params[2],
            username=reddit_params[3],
            password=reddit_params[4]
        )


        self.instance_id = instance_id

        self.instance_num = instance_num

        self.operate_recursively = operate_recursively


        # Define dependencies.
        self.__define_stream_dependencies__()



    def __define_stream_dependencies__(self):
        """

        :return:
        """

        # A temporary definition of the collection of the topic keywords.
        # NOTE: CURRENTLY USING ONLY THE FIRST COLLECTION OF PROBLEM TOPIC KEYWORDS; STILL COMPILING FULL COLLECTION.
        with open("/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/Agent/Agent-R/Version 1/Cerebrum/machine_lobe/Resources/ProblemTopicKeywords/v1/topic_keywords.json", 'r') as fp:

            self.rated_ptopic_kwds = pandas.Series(json.load(fp))


        # Define the bag of words for the problem topic keyword data.
        self.ptopic_kwds_bag = tuple(self.rated_ptopic_kwds.index.values)


        # Normalize 'ptopic_kwds_bag', converting all keywords to lowercase strings.
        self.ptopic_kwds_bag = list(map(lambda x: x.lower(), self.ptopic_kwds_bag))


        # Remove stop words.
        self.ptopic_kwds_bag = self.remove_stopwords(self.ptopic_kwds_bag)


        # Define 'main_df'.
        self.main_df = pandas.read_json(self.FP_aggregate_archive)


        # Verify the integrity of 'main_df'.
        self.__verify_main_df_integrity__()


        #
        self.FP_final_archive = \
            "Resources/StreamMachineOperatorResources/Instance" + str(self.instance_num) + "Run/main_df-" + self.instance_id + ".json"


        return 0



    def __init_operation_lobes__(self, work_subreddit: str):
        """

        :param work_subreddit:
        :return:
        """

        self._input_lobe = self.__new_InputLobe__(
            reddit_instance= self.reddit_instance,
            subreddit= work_subreddit
        )

        self._output_lobe = self.__new_OutputLobe__(
            reddit_instance= self.reddit_instance,
            subreddit= work_subreddit
        )

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
    def __new_OutputLobe__(reddit_instance: praw.Reddit, subreddit: str):
        """
        A method allowing for customizable creation of OutputLobe objects.

        :param reddit_instance:
        :param subreddit:
        :return:
        """

        return OutputLobe(reddit_instance=reddit_instance, subreddit=subreddit)



    @staticmethod
    def intersect(list_x: (list, tuple), list_y: (list, tuple)):
        """

        :param list_x:
        :param list_y:
        :return:
        """

        return list(set(list_x) & set(list_y))



    def remove_stopwords(self, corpus: (list, tuple)):
        """
        Returns the given corpus restricted of English stopwords.

        :param corpus:
        :return:
        """

        return [word for word in corpus if word not in self.stop_words]



    # noinspection PyDictCreation
    def __analyze_subm_title_kwds__(self, submission: reddit.Submission, return_subm_obj: bool = True):
        """
        'Analyze Submission Keywords'

        Performs keyword intersection analysis for the topic keyword collection and a given Submission's title.

        :return:
        """

        # Define the keywords for the given Submission title.
        subm_title_keyword_analysis = indicoio.keywords(submission.title)
        subm_title_keywords = tuple(subm_title_keyword_analysis.keys())


        # Define a collection of the words in a Submission title.
        subm_title_tokens = tuple(map(lambda x: x.lower(), submission.title.split()))


        # Remove English stopwords from the Submission title word content set.
        subm_title_tokens = self.remove_stopwords(corpus= subm_title_tokens)


        # Define the intersection of the topic keywords bag and the Submission's title content.
        # FIXME Currently using the entire set of words from Submission titles -- this is naturally what we as people do
        # FIXME when reading documents to identify relevance to a certain topic.
        title_intxn = self.intersect(self.ptopic_kwds_bag, subm_title_tokens)


        # Initialize the keyword intersection count.
        keywords_intersections_count = len(title_intxn)


        # Define a structure to contain all measures relevant to analysis.
        analysis = {
            "submission_id": submission.id,
            "submission_title": submission.title,
            "title_intxn": title_intxn,
            "title_intxn_size": float(keywords_intersections_count),
            "title_kwds": subm_title_keywords
        }


        # Define a probability measure of success and append this to the 'analysis' dictionary.
        # This figure is used to determine whether or not the Agent will submit a textual expression
        # to a Reddit Submission.
        # TODO: This measure is to be optimized in the future.
        analysis["success_probability"] = self.probability(method="keyword", values=tuple(analysis.values()))


        if return_subm_obj:
            # Append Submission object to the analysis.
            # NOTE: Attempting to serialize the main DataFrame with this field as a member will cause an
            # overflow error.
            analysis["submission_object"] = submission


        return analysis



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
                # The determined max value is obtained from the amount of ptopic keywords.
                return self.normalize(success_probability, minimum= 0, maximum= 79)

            else:

                return success_probability



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



    def __analyze_subm_aurl_kwds__(self, submission: reddit.Submission):
        """
        Performs keyword intersection analysis on the ptopic keywords and a Submission's linked article accessed by an
        attached URL.

        This attached article for a Submission is referenced as "AURL".

        :return:
        """

        # Define alias to linked URL of the provided Submission.
        subm_url = submission.url


        # Generate keyword analysis for the AURL.
        subm_aurl_kwd_analysis = indicoio.keywords(subm_url)

        # Retrieve the exclusively the keywords identified for the AURL.
        subm_aurl_kwds = tuple(subm_aurl_kwd_analysis.keys())


        # Normalize all keywords to be lowercase.
        subm_aurl_kwds = tuple(map(lambda x: x.lower(), subm_aurl_kwds))


        # Define the intersection of the ptopic keywords and the AURL.
        subm_aurl_intxn = self.intersect(self.ptopic_kwds_bag, subm_aurl_kwds)


        # Initialize the keyword intersection count.
        subm_aurl_intxn_count = len(subm_aurl_intxn)


        # Define a structure to contain all measures relevant to analysis.
        analysis = {
            "aurl_kwd_intxn": subm_aurl_intxn,
            "aurl_kwd_intxn_size": float(subm_aurl_intxn_count),
            "subm_aurl_kwds": subm_aurl_kwds,
            "sub_aurl_url": subm_url
        }


        return analysis



    def __analyze_subm_relevance__(self, submission: reddit.Submission):
        """
        Generates a definition of relevance to the ptopic for a given Submission.

        :return:
        """

        # Define alias to linked URL of the provided Submission.
        subm_url = submission.url


        # Generate a relevance measure.
        relevance_analyses = indicoio.relevance(
            [submission.title, subm_url],
            [
                "Humanitarian Crisis in Puerto Rico",
                # "Humanitarian Crisis",
                # "Empathy",
                # "Anger"
            ]
        )


        # Convert "Anger" measures to negative values.
        # relevance_analyses[0][3] = -abs(relevance_analyses[0][3])
        # relevance_analyses[1][3] = -abs(relevance_analyses[1][3])


        return relevance_analyses



    @staticmethod
    def save_object(obj, save_file):

        with open(save_file, "w+") as file:

            json.dump(obj= obj, fp= file, indent=2)



    def __archive_subm_data__(self):
        """
        Records 'main_df': creates a temporary variable from the aggregate DataFrame, appends this to 'main_df', and
                           archives this aggregation.
        :return:
        """

        # Input aggregate archive.
        aggregate_in = pandas.read_json(self.FP_aggregate_archive)


        # Remove duplicate values from the aggregate DataFrame.
        aggregate_in.drop_duplicates(subset='id', inplace=True)


        # Aggregate aggregate DataFrame and 'main_df'.
        aggregation: pandas.DataFrame = pandas.concat([aggregate_in, self.main_df])


        # Remove duplicate values from the Aggregation.
        aggregation.drop_duplicates(subset= 'id', inplace= True)


        # Reset the index.
        aggregation.reset_index(drop= True, inplace= True)


        # Archive the DataFrame aggregation.
        aggregation.to_json(path_or_buf= self.FP_aggregate_archive)


        return 0




    def __update_main_df__(self, dict_list_in: list):
        """
        Appends current-work Submission data to 'main_df'.

        :return:
        """

        # Generate a DataFrame from the list of Dicts.
        T = pandas.DataFrame(dict_list_in)

        # Append 'T' to 'main_df'.
        self.main_df = pandas.concat([T, self.main_df])

        # Remove duplicate rows in 'body' column keeping the first occurrence.
        self.main_df.drop_duplicates(subset='id', keep='first', inplace= True)

        # Reset the index.
        self.main_df.reset_index(drop=True, inplace= True)


        return 0



    def __verify_main_df_integrity__(self):
        """
        A function to verify the integrity of 'main_df'; that is, remove duplicate values, etc.

        :return:
        """

        # Drop duplicate entries.
        self.main_df.drop_duplicates(subset= 'id', inplace= True)


        # Ensure appropriate indexing.
        self.main_df.reset_index(drop= True, inplace= True)


        return 0





    def __save_work__(self, dict_list_in: list):
        """
        Compiles and archives an aggregation of the 'update_main_df' and 'archive_subm_data' processes.

        :param dict_list_in:
        :return:
        """

        self.__verify_main_df_integrity__()

        self.__update_main_df__(dict_list_in)

        self.__archive_subm_data__()

        self.__perform_final_archive()

        return 0


    def __view_main_df__(self):
        """
        Allows for the observation of 'main_df' with parameters.

        :return:
        """

        print(self.main_df.to_string())


        return 0




    def __stream_process__(
            self,
            utterance_content: str,
            keyboard_interrupt_save_file: str,
            engage: bool = False,
            work_subreddit: str = "news",
            relevance_clearance_threshold: float = 0.5,
    ):
        """

        :return:
        """

        # Define iterator for Stream loop.
        stream_loop_i = 0

        # Create InputLobe object to produce Submission metadata for the "news" Subreddit.
        # Create OutputLobe object to handle expression utterance.
        self.__init_operation_lobes__(work_subreddit= work_subreddit)


        # Define a container for Submission objects.
        self.RedditSubmission_objects = pandas.DataFrame()


        RSubmissions = list()

        #
        for submission in self.reddit_instance.subreddit("news").stream.submissions(pause_after=0):

            # Attempt to catch KeyboardInterrupt, AttributeError
            try:

                # Generate metadata for Reddit Submission in preparation for RSubmission object creation.
                preliminary_subm_data = self.__process_submission__(
                    submission_obj= submission,
                    analyze_subm_title_kwds=True,
                    analyze_subm_article_kwds=True,
                    analyze_subm_relevance=True
                )

                try:

                    # Create RSubmission object with preliminary Submission metadata and analyses.
                    R_Submission = RSubmission(fields= preliminary_subm_data)


                    R_Submission.high_utterance_content = utterance_content


                except Exception as E:

                    stream_loop_i += 1

                    print(
                        "Error at index",
                        stream_loop_i,
                        "creating RSubmission object.",
                        E.__traceback__
                    )

                    continue


                if engage:

                    try:

                        # Test for clearance of engagement and and ensure that it has not already
                        # been engaged on; proceed if appropriate.
                        if (self.__STREAM_clearance__(R_Submission, "relevance", relevance_clearance_threshold) and
                                RSubmission.engaged_on is False):

                            self.__STREAM_engage_subm__(submission_obj= R_Submission, utterance_content= utterance_content)


                            # Set engagement status.
                            R_Submission.engaged_on = True


                            # Define time of engagement.
                            R_Submission.high_engagement_datetime = str(datetime.now())

                    except praw.exceptions.APIException as E:

                        print("Encountered comment creation limit...: ", E.message, "\nWaiting 520 seconds.")

                        # Wait out comment creation limit.
                        time.sleep(520)


                # Append the collection of fields for the RSubmission object to 'RSubmission' for later conversion
                #   to Pandas DataFrame.
                RSubmissions.append(vars(R_Submission))


                # Indicate clearance for data archival.
                archive = True


                # Increment stream loop counter.
                stream_loop_i += 1


                if stream_loop_i == 99:
                    # End process in anticipation of 100 Submission Stream limit.

                    # Save work data.
                    self.__save_work__(RSubmissions)

                    break



            except (KeyboardInterrupt, AttributeError, IndicoError) as Error:

                if AttributeError:

                    print(AttributeError.__cause__, " at index: ", stream_loop_i)

                    stream_loop_i += 1

                    continue


                if IndicoError:

                    print(IndicoError, " at index: ", stream_loop_i)

                    stream_loop_i += 1

                    continue


                if KeyboardInterrupt:
                    # Indicates user process termination.

                    with open(keyboard_interrupt_save_file, "w+") as file:

                        json.dump(RSubmissions, file, indent=2)

                        self.__save_work__(RSubmissions)


                    return 0


                else:

                    print("Unknown error. Exiting and saving data...")

                    self.__save_work__(RSubmissions)


            finally:

                if archive:
                    # FIXME: Currently feeding every single RSubmission object and its analysis. Must optimize in order
                    # FIXME  to feed just the current RSubmission.


                    # Store the most recently processed RSubmission.
                    self.__save_work__(RSubmissions)


        return 0

    def __recursive_stream_process__(
            self,
            utterance_content: str,
            keyboard_interrupt_save_file: str,
            FP_aggregate_archive_override: str,
            engage: bool = False,
            work_subreddit: str = "news",
            relevance_clearance_threshold: float = 0.5,
    ):
        """

        :return:
        """

        # Override the aggregate archive for 'main_df' file-path.
        # TODO: Make this more concrete.
        self.FP_aggregate_archive = FP_aggregate_archive_override
        self.FP_final_archive = FP_aggregate_archive_override


        # Define iterator for Stream loop.
        stream_loop_i = 0

        # Create InputLobe object to produce Submission metadata for the "news" Subreddit.
        # Create OutputLobe object to handle expression utterance.
        self.__init_operation_lobes__(work_subreddit=work_subreddit)

        # Define a container for Submission objects.
        self.RedditSubmission_objects = pandas.DataFrame()

        # Container for increasing list of RSubmissions and their analyses.
        RSubmissions = list()

        # Define controller for infinite loop.
        do_work = 1



        for submission in self.reddit_instance.subreddit("news").stream.submissions(pause_after=0):


            # Attempt to catch KeyboardInterrupt, AttributeError
            try:

                # Generate metadata for Reddit Submission in preparation for RSubmission object creation.
                preliminary_subm_data = self.__process_submission__(
                    submission_obj=submission,
                    analyze_subm_title_kwds=True,
                    analyze_subm_article_kwds=True,
                    analyze_subm_relevance=True
                )

                try:

                    # Create RSubmission object with preliminary Submission metadata and analyses.
                    R_Submission = RSubmission(fields=preliminary_subm_data)

                    R_Submission.high_utterance_content = utterance_content


                except Exception as E:

                    stream_loop_i += 1

                    print(
                        "Error at index",
                        stream_loop_i,
                        "creating RSubmission object.",
                        E.__traceback__
                    )

                    print("Analyzed: ", stream_loop_i)

                    continue

                if engage:

                    try:

                        # Test for clearance of engagement and and ensure that it has not already
                        # been engaged on; proceed if appropriate.
                        if (self.__STREAM_clearance__(R_Submission, "relevance", relevance_clearance_threshold) and
                                RSubmission.engaged_on is False):

                            self.__STREAM_engage_subm__(submission_obj=R_Submission,
                                                        utterance_content=utterance_content)

                            # Define time of engagement.
                            R_Submission.high_engagement_datetime = str(datetime.now())

                    except praw.exceptions.APIException as E:

                        print("Encountered comment creation limit: ", E.message, "\nWaiting 620 seconds...\n")

                        # Wait out comment creation limit.
                        time.sleep(520)

                        print("Continuing...")

                # Append the collection of fields for the RSubmission object to 'RSubmission' for later conversion
                #   to Pandas DataFrame.
                RSubmissions.append(vars(R_Submission))

                # Indicate clearance for data archival.
                archive = True

                # Increment stream loop counter.
                stream_loop_i += 1

                print("Analyzed: ", stream_loop_i)


                # FIXME: Remove! This creates a single netry for a json file so that the initial archive step does not
                # FIXME     read an empty JSON file and return an error.
                # self.main_df.iloc[0].to_json(self.FP_final_archive)


                if stream_loop_i == 99:
                    # Anticipate reach of 100 Submission Stream limit.

                    # Save work data.
                    self.__save_work__(RSubmissions)

                    print("*" * 20)
                    print("ENTERING ADDITIONAL RECURSION LEVEL")
                    print("*" * 20)


                    # Call recursively to continue process.
                    self.__recursive_stream_process__(

                        utterance_content,
                        keyboard_interrupt_save_file,
                        FP_aggregate_archive_override,
                        engage,
                        work_subreddit,
                        relevance_clearance_threshold

                    )


            except (KeyboardInterrupt, AttributeError, IndicoError) as Error:

                if AttributeError:
                    print(AttributeError.__cause__, " at index: ", stream_loop_i)

                    stream_loop_i += 1

                    print("Analyzed: ", stream_loop_i)


                    continue

                if IndicoError:
                    print(IndicoError, " at index: ", stream_loop_i)

                    stream_loop_i += 1

                    print("Analyzed: ", stream_loop_i)


                    continue

                else:

                    print("Unknown error. Exiting and saving data...")

                    self.__save_work__(RSubmissions)

            except KeyboardInterrupt:
                # Indicates user process termination.

                with open(keyboard_interrupt_save_file, "w+") as file:

                    json.dump(RSubmissions, file, indent=2)

                    self.__save_work__(RSubmissions)

                return 0


            finally:

                if archive:
                    # FIXME: Currently feeding every single RSubmission object and its analysis. Must optimize in order
                    # FIXME  to feed just the current RSubmission.

                    # Store the most recently processed RSubmission.
                    self.__save_work__(RSubmissions)



        return 0



    def __perform_final_archive(self):
        """
        Performs final archival of 'main_df' to a temporally identified file.

        :return:
        """

        self.main_df.to_json(path_or_buf= self.FP_final_archive)


        return 0



    def __STREAM_engage_subm__(
            self,
            submission_obj: RSubmission,
            utterance_content: str
    ):
        """
        Submits comment to Submission with provided Submission ID and utterance content.

        :param submission_obj:
        :param utterance_content:
        :return:
        """

        # Perform engagement in a Submission with provided utterance content.
        self._output_lobe.submit_submission_expression(

            self.reddit_instance.submission(submission_obj.id),
            utterance_content=utterance_content

        )

        # Define True engaged-on state.
        submission_obj.engaged_on = True

        return 0



    @staticmethod
    def __STREAM_clearance__(
            submission_obj: RSubmission,
            clearance_method: str,
            relevance_clearance_threshold: float = 0.5,
    ):
        """
        Determines if the Agent is to engage in a Submission, observing the RSubmission metadata.

        # TODO: Substantial optimization.

        :return:
        """

        # # Initialize a clearance determination.
        # clearance = False

        if clearance_method == "keywords":

            # Determine clearance status.
            # Clearance evaluates as true if the magnitude of the intersection is greater than
            # or equal to a quarter of the length of the Submission title.
            if (submission_obj.title_kwd_intxn_size or submission_obj.aurl_kwd_intxn_size) >= int(
                    len(submission_obj.title) / 4):
                submission_obj.engagement_clearance = True

                return True

        if clearance_method == "relevance":

            # Clearance evaluates as true if the Indico Relevance measure of the Submission AURL is above a magnitude of 4.5.
            if sum(submission_obj.iIO_aurl_relevance_scores) > relevance_clearance_threshold:
                submission_obj.engagement_clearance = True

                return True



    def __process_submission__(
            self,
            submission_obj: reddit.Submission,
            analyze_subm_title_kwds: bool,
            analyze_subm_article_kwds: bool,
            analyze_subm_relevance: bool
    ):
        """
        Performs Keyword and Relevance analysis for a single Submission.

        :return:
        """

        # Define alias to Indico API scraping error.
        indico_scraping_error = indicoio_errors.IndicoError

        # Define container for Submission title and AURL analyses.
        analysis = {}

        # Update 'analysis' with Submission metadata.
        submission_obj.comments.replace_more(limit=0)

        analysis["comment_amount"] = len(submission_obj.comments.list())
        analysis["subm_title"] = submission_obj.title

        if analyze_subm_title_kwds:
            # Perform Submission title keyword analysis.
            analysis.update(self.__analyze_subm_title_kwds__(submission_obj))

        if analyze_subm_article_kwds:

            # Perform Submission AURL keyword analysis.
            analysis.update(self.__analyze_subm_aurl_kwds__(submission_obj))


        if analyze_subm_relevance:

            # Perform relevance measurement.
            analysis["subm_relevance_scores"] = self.__analyze_subm_relevance__(submission_obj)


        return tuple(analysis.values())
