import gcp_authentication
import dialogflow
import praw
import time
import google




"""

Parameters: 

    - Submission
    - Running-Time
    - Reddit Account
    - GCP Project ID
    - GCP Session ID
    - GCP Language Code
    - Topic ( For future )

"""


class DF_Agent:


    def __init__(
            self,
            reddit_parameters: tuple,
            submission: str,
            running_time: int,
            gcp_project_id: str = "cs-196",
            gcp_session_id: str = "dialogflow\reddit\moderation\agent",
            gcp_language_code: str = "en"
    ):

        # Define the Reddit instance with the specified parameters.
        self.reddit_instance = praw.Reddit(
            client_id=reddit_parameters[0],
            client_secret=reddit_parameters[1],
            user_agent=reddit_parameters[2],
            username=reddit_parameters[3],
            password=reddit_parameters[4]
        )


        # Define the Subreddit for work.
        self.submission = self.reddit_instance.submission(id= submission)


        # Define the running-time.
        self.meta_running_time = running_time


        # Define Google Cloud Platform (GCP) Parameters.
        self.gcp_project_id = gcp_project_id

        self.gcp_session_id = gcp_session_id

        self.gcp_language_code = gcp_language_code

        self.gcp_session_client = dialogflow.SessionsClient()

        self.gcp_session = self.gcp_session_client.session_path(self.gcp_project_id, self.gcp_session_id)



    def print_subm_comments(self):
        """

        :return:
        """

        # Define list of all Comment objects from the specified Submission.
        self.submission.comments.replace_more(limit= 0)
        submission_comments = self.submission.comments.list()


        for comment in submission_comments:

            print(
                comment.body,
                "\n",
                '=' * 30,
                "\n"
            )



        return self



    def run_main_process(
            self,
            verbose: bool = False
    ):
        """

        :return:
        """

        time_0 = time.time()

        time_1 = 0


        # Define list of all Comment objects from the specified Submission.
        self.submission.comments.replace_more(limit= 0)
        submission_comments = self.submission.comments.list()


        # Define list of all Comments that have been engaged-on.
        engaged_comments = []


        # Run for the specified amount of time.
        while time_0 - time_1 != self.meta_running_time:

            # Consider every Comment for a response.
            for comment in submission_comments:

                # Define container for the Comment context (body).
                comment_body = comment.body


                try:

                    # Ignore Comment is the context length is less than 3 (three words).
                    if len(comment_body.split()) < 3:

                        print(
                            "Encountered Comment of insufficient context length.",
                            "Adding Comment to 'engaged_comments' and continuing process.",
                            "\n"
                        )

                        # Archive Comment object to 'engaged_comments'.
                        engaged_comments.append(comment)


                        # Update time record.
                        time_1 = time.time()

                        continue

                    # Ignore Comment if it has already been processed.
                    elif comment in engaged_comments:

                        print(
                            "Encountered Comment which has already been processed.",
                            "Continuing process.",
                            "\n"
                        )


                        # Update time record.
                        time_1 = time.time()

                        continue

                    else:

                        if verbose: print(comment_body)


                        # Obtain response to the Comment context using the DialogFlow API.
                        text_input = dialogflow.types.TextInput(
                            text= comment_body,
                            language_code= self.gcp_language_code
                        )

                        query_input = dialogflow.types.QueryInput(text= text_input)

                        response = self.gcp_session_client.detect_intent(
                            session= self.gcp_session,
                            query_input= query_input
                        )


                        # Create a response to the Comment with a body generated by the DialogFlow API.
                        comment.reply(body= response.query_result.fulfillment_text)


                        # Archive to 'engaged_comments'.
                        engaged_comments.append(comment)


                        # Stall process continuation in order to account for Reddit Comment creation rules and to
                        # ensure desirable perception of the Agent on Reddit.
                        print(
                            "Created response to Comment: \n",
                            "\t\t",
                            comment_body,
                            "Beginning process stall for 10 minutes."
                        )

                        time.sleep(600)


                        # Update time record.
                        time_1 = time.time()

                        continue


                # Catch exception for invalid input to the GCP API.
                except google.api_core.exceptions.InvalidArgument:

                    print(
                        "Encountered invalid GCP API argument.",
                        "Comment context length is likely too large.",
                        "Adding Comment to 'engaged_comments' and continuing process.",
                        "\n"
                    )

                    # Archive Comment object to 'engaged_comments'.
                    engaged_comments.append(comment)


                    # Update time record.
                    time_1 = time.time()

                    continue

                # Catch Reddit API server-side error.
                except praw.exceptions.APIException:

                    print(
                        "Encountered Reddit Comment creation limit.",
                        "Adding Comment to 'engaged_comments' and continuing process.",
                        "\n"
                    )

                    # Archive Comment object to 'engaged_comments'.
                    engaged_comments.append(comment)


                    # Update time record.
                    time_1 = time.time()

                    continue


            # Create delay to wait for creation of more Comments.
            time.sleep(600)


            # Update time record.
            time_1 = time.time()


        return self

