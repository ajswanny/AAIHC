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
        """

        :param p_client_id:
        :param p_client_secret:
        :param p_user_agent:
        """

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
        """

        :param p_subreddit_id:
        :return:
        """

        self.subreddits[p_subreddit_id] = self.reddit_instance.subreddit(p_subreddit_id)

        print("Successfully added subreddit: " + p_subreddit_id)

        self.subreddit_names.append(p_subreddit_id)



    def add_submissions(self, subreddit_name: str, which: str, *args):
        """

        :param subreddit_name:
        :param which:
        :param args:
        :return:
        """

        # Add the specified Submission objects.
        if which == 'given':

            for arg in args:

                submission_name = subreddit_name + '-' + arg

                self.submissions[submission_name] = self.reddit_instance.submission(id=arg)

                print("Successfully added submission: " + str(arg))

                self.submission_ids.append(arg)


        # Add the top 50 Submissions for the given Subreddit.
        if which == 'full':

            # Add submissions.
            for submission in self.subreddits['news'].top(time_filter= 'all', limit= 50):

                submission_name = subreddit_name + '-' + submission.id

                self.add_submissions('news', submission.id)

                work_id = 'news-' + submission.id

                self.build_json_data(json_path= 'respective', replace_more= True)



    def build_json_data(self, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """

        # Define parameters.
        json_path: str = kwargs['json_path']                        #

        replace_more: bool = kwargs['replace_more']                 #


        # Define list to filter data to be recorded.
        fields_for_comment_dict = (
            'id', 'parent_id', 'subreddit_name_prefixed', 'body', 'controversiality', 'ups', 'downs', 'score',
            'created')


        # Output process step.
        print("Beginning serialization of Submission objects.")

        for key in self.submissions:

            list_of_items = []


            print("\tSerializing: " + str(self.submissions[key]) + " ...")


            for comment in self.submissions[key].comments.list():

                to_dict = vars(comment)

                sub_dict = {field: to_dict[field] for field in fields_for_comment_dict}

                date = str(datetime.fromtimestamp(vars(comment)['created_utc'])).split()
                sub_dict['date_created'] = date[0]
                sub_dict['time_created'] = date[1]

                list_of_items.append(sub_dict)


            # Define default JSON file location.
            if json_path == 'respective':
                special = 'r(news)_submission-' + self.submissions[key].id + '.json'

                json_path = '/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/json_data/' + special


            try:

                # Write JSON object to file.
                with open(json_path, 'w') as f:
                    json.dump(list_of_items, f, indent=2)

            except IOError:
                print("Could not locate JSON file.")


        print("\t\tDone")



    def prepare_build(self):
        """
        Handler method for any necessary pre-processing respective to: 'self.build_json_data()'.
        :return:
        """


        # Replace the "More" objects of each submission.
        for key in self.submissions:
            self.submissions[key].comments.replace_more(limit=0)



    def build(self, sub_id: str):
        """
        Handler method for alternate building process.
        :param sub_id:
        :return:
        """

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



def main():
    """

    :return:
    """

    # Create an instance of the "DataMiner" class.
    data = DataCollector('hpTnFWPodmP85w', 'T2rZgWYrmqB_ULSOmIVZVn2ff8Q', "r/praw_tester's research_project")


    # Add the "news" subreddit to the Reddit instance of "data".
    data.add_subreddit('news')

    data.add_submissions(which= 'full')

    data.build_json_data(json_path= 'default', replace_more= True)


    return 0







if __name__ == "__main__": main()








# EOF
