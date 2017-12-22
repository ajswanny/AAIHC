# BOF

import json
import praw
import pprint
from datetime import datetime


# For Raspberry Pi integration:
#   - Continuous retrieval, organization, and sorting of data


# noinspection PyCompatibility
class DataCollector:
    # Prefix 'p' = 'parameter'.

    reddit_instance: praw.Reddit

    subreddits: dict
    subreddit_names: list

    submissions: dict
    submission_ids: list

    def __init__(self, p_client_id: str, p_client_secret: str, p_user_agent: str):

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

    def build_json_data(self, *args, **kwargs):

        which_to_serialize: str = kwargs['which']
        json_path: str = kwargs['json_path']
        absolute_amount: bool = kwargs['entire_comment_tree']

        all_ids: list = []
        for key in self.submissions:
            all_ids.append(key)

        # Begin collecting data from the previously added "Submission".

        fields_for_comment_dict = (
            'id', 'parent_id', 'subreddit_name_prefixed', 'body', 'controversiality', 'ups', 'downs', 'score',
            'created')

        #
        for arg in self.submissions:
            self.submissions[arg].comments.replace_more(limit=0)

        print(args)

        # Iterate for 'all' condition.
        print("Serializing Submission objects.")
        if which_to_serialize == 'all':

            for arg in args:

                list_of_items = []

                print("\tSerializing: " + str(self.submissions[arg]) + " ...")

                for comment in self.submissions[arg].comments.list():
                    to_dict = vars(comment)

                    sub_dict = {field: to_dict[field] for field in fields_for_comment_dict}

                    date = str(datetime.fromtimestamp(vars(comment)['created_utc'])).split()
                    sub_dict['date_created'] = date[0]
                    sub_dict['time_created'] = date[1]

                    list_of_items.append(sub_dict)

                # Define default JSON file location.
                if json_path == 'respective':
                    special = 'r(news)_submission-' + self.submissions[arg].id + '.json'

                    json_path = '/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/json_data/' + special

                try:

                    # Write JSON object to file.
                    with open(json_path, 'w') as f:
                        json.dump(list_of_items, f, indent=2)

                except IOError:
                    print("Could not locate JSON file.")

            print("\t\tDone")


#TODO: Clean up
def run():
    # Create an instance of the "DataMiner" class.
    data = DataCollector('hpTnFWPodmP85w', 'T2rZgWYrmqB_ULSOmIVZVn2ff8Q', "r/praw_tester's research_project")


    # Add the "news" subreddit to the Reddit instance of "data".
    data.add_subreddit('news')

    work_ids = []


    for submission in data.subreddits['news'].top(time_filter='all', limit= 50):

        #TODO: Clean up
        work_id = 'news-' + submission.id

        work_ids.append(submission.id)

    # with open('/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/json_data/json_paths', 'w') as f:
    #
    #     for id in work_ids:
    #
    #         f.write(id + '\n')


    print()

run()






#TODO: Determine incorporation
def build(data: DataCollector, sub_id: str):

    # Add submissions.
    for submission in data.subreddits['news'].top(time_filter='all', limit=50):

        data.add_submissions('news', submission.id)

        work_id = 'news-' + submission.id

        data.build_json_data(work_id, which='all', json_path='respective', entire_comment_tree=True)

    # data.build_json_data('news-7ej943', which='all', json_path='respective', entire_comment_tree=True)
    # data.build_json_data('news-79v2cg', which='all', json_path='respective', entire_comment_tree=True)
    # data.build_json_data('news-6oi3gu', which='all', json_path='respective', entire_comment_tree=True)
    # data.build_json_data('news-5r5qx4', which='all', json_path='respective', entire_comment_tree=True)
    # data.build_json_data('news-7fwv10', which='all', json_path='respective', entire_comment_tree=True)
    # data.build_json_data('news-6a8ji6', which='all', json_path='respective', entire_comment_tree=True)
    # data.build_json_data('news-72xfdb', which='all', json_path='respective', entire_comment_tree=True)
    # data.build_json_data('news-3b6zln', which='all', json_path='respective', entire_comment_tree=True)
    # data.build_json_data('news-6zw2mp', which='all', json_path='respective', entire_comment_tree=True)
    # data.build_json_data('news-5vznv8', which='all', json_path='respective', entire_comment_tree=True)

    return 0

# EOF
