"""
Recorded: November 29, 2017
"""


# Beginning of Record
"""
# BOF
import praw
import json
import pandas
import pprint
from datetime import datetime


###


# noinspection PyCompatibility
class DataCollector:
    # Prefix 'p' = 'parameter'.

    reddit_instance: praw.Reddit

    subreddits: dict
    subreddit_names: list

    submissions: dict
    submission_ids: list

    def __init__(self, p_client_id, p_client_secret, p_user_agent):

        self.reddit_instance = praw.Reddit(client_id=p_client_id,
                                           client_secret=p_client_secret,
                                           user_agent=p_user_agent)

        # Initialize fields.
        self.subreddits = {}
        self.subreddit_names = []

        self.submissions = {}
        self.submission_ids = []

        # Confirm instantiation.
        print("DataCollector instantiated.")


    def add_subreddit(self, p_subreddit_id: str):

        self.subreddits[p_subreddit_id] = self.reddit_instance.subreddit(p_subreddit_id)

        print("Successfully added subreddit: " + p_subreddit_id)

        self.subreddit_names.append(p_subreddit_id)


    def add_submissions(self, p_subreddit_name: str, *args):

        for arg in args:
            name = p_subreddit_name + '-' + arg

            self.submissions[name] = self.reddit_instance.submission(id=arg)

            print("Successfully added submission: " + str(arg))

            self.submission_ids.append(arg)


    def build_data(self, submission_to_serialize):

        try:
            # Begin collecting data from the previously added "Submission".
            list_of_items = []

            fields_for_comment_dict = ('id', 'subreddit_name_prefixed', 'body', 'controversiality', 'ups', 'downs', 'score',
                                       'created')

            # Replace "More_Comments" objects to prevent errors.
            self.submissions[submission_to_serialize].comments.replace_more(limit=0)

            # Iterate
            for comment in self.submissions[submission_to_serialize].comments.list():
                # pprint.pprint(vars(comment))

                to_dict = vars(comment)

                sub_dict = {field: to_dict[field] for field in fields_for_comment_dict}

                date = str(datetime.fromtimestamp(vars(comment)['created_utc']))
                sub_dict['created_datetime'] = date

                list_of_items.append(sub_dict)

            # Write JSON object to file.
            # CURRENTLY USING DEFAULT PATH
            # TODO: Implement file location optioning.
            with open('json_data.json', 'w') as f:
                json.dump(list_of_items, f)

        except IOError:
            print("Could not locate JSON file.")



# noinspection PyCompatibility
class DataCleaner:

    dataframe: pandas.DataFrame

    json_path: str
    default_json_path: str


    def __init__(self, json_path):

        # Set the default JSON file location.
        self.default_json_path = '/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/json_data/json_data.json'

        #
        if json_path == 'default_path':
            self.json_path = self.default_json_path

        #
        self.dataframe = pandas.read_json(self.json_path)

        # Confirm instantiation.
        print("DataCleaner instantiated.")


    def view_dataframe(self):

        print(self.dataframe.to_string())


    # Builds a Dataframe with the correct column organization.
    def organize_dataframe(self):

        self.dataframe = self.dataframe[
            ['id', 'subreddit_name_prefixed', 'body', 'ups', 'downs', 'score', 'controversiality',
             'created', 'created_datetime']]


    def clean_dataframe_rows(self):

        temp_df = self.dataframe.query("body != '[deleted]'")
        temp_df = temp_df.query("body != '[removed]'")

        local_df = temp_df.reset_index(drop=True)

        self.dataframe = local_df



# Create an instance of the "DataMiner" class.
data = DataMiner('hpTnFWPodmP85w', 'T2rZgWYrmqB_ULSOmIVZVn2ff8Q', 'test')

# Add the "news" subreddit to the Reddit instance of "data".
data.add_subreddit('news')

# Add submission.
data.add_submissions('news', '79v2cg')

data.build_data(submission_to_serialize='news-79v2cg')


print('\n\n')


# Instantiate DataCleaner
data_clean = DataCleaner('default_path')

# Build the workable Dataframe.
data_clean.organize_dataframe()

# Clean up Dataframe. Remove rows with 'body' column containing "[deleted]" or "[removed]".
data_clean.clean_dataframe_rows()

# View the Dataframe.
data_clean.view_dataframe()




# EOF

"""
# End of Record
