# BOF

#
# DataCollector - Version 0.1
# Copyright (c) 2017, Alexander Joseph Swanson Villares
#

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
        Init.
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
        Add a "Subreddit" object to the Reddit instance.
        :param p_subreddit_id:
        :return:
        """

        self.subreddits[p_subreddit_id] = self.reddit_instance.subreddit(p_subreddit_id)

        print("Successfully added subreddit: " + p_subreddit_id)

        self.subreddit_names.append(p_subreddit_id)


        return self



    def add_submissions(self, *args, subreddit_name: str, which: str, recursion: bool):
        """
        Adds the specified "Submission" objects to the Reddit instance.
        :param recursion:
        :param subreddit_name:
        :param which:
        :param args:
        :return:
        """

        # Output state.
        if not recursion:
            print("Adding Submissions...")

        # Add the specified Submission objects.
        if which == 'given':

            for arg in args:

                submission_name = subreddit_name + '-' + arg

                self.submissions[submission_name] = self.reddit_instance.submission(id=arg)

                print("\t" + submission_name)


        # Add the top 50 Submissions for the given Subreddit if 'which' is true.
        if which == 'full':

            # Add submissions.
            for submission in self.subreddits['news'].top(time_filter= 'all', limit= 50):

                submission_id = submission.id

                submission_name = subreddit_name + '-' + submission_id

                self.add_submissions(submission_id, subreddit_name= 'news', which= 'given', recursion= True)


        return self


    def prepare_build(self):
        """
        Handler method for any necessary pre-processing respective to: 'self.build_json_data()'.
        :return:
        """

        # Replace the "More" objects of each submission.
        print("Preparing for serialization...")

        count = 1

        for key in self.submissions:
            self.submissions[key].comments.replace_more(limit=0)

            print('\t', count, key)

            count += 1

        print('\tComplete.')


        return self



    def build_json_indexes(self):
        """
        Creates a file listing all "Submission" IDs for later reference.
        :return:
        """

        # Define the file location.
        path = '/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/Reddit/json_data/json_paths'

        # Open the file.
        with open(path, 'w+') as f:

            # Write each Submission's ID to the file.
            for key in self.submissions:

                f.write(self.submissions[key].id + '\n')


        return self



    def build_json_data(self):
        """
        Serializes "Comment" data structures for each "Submission" in the submissions dict.
        :return:
        """

        # Define list to filter data to be recorded.
        fields_for_comment_dict = (
            'id', 'parent_id', 'subreddit_name_prefixed', 'body', 'controversiality', 'ups', 'downs', 'score',
            'created')


        # Output process.
        print("Beginning serialization of Submission objects. \nSerializing...")

        # Serialize each Submission's comments to a JSON file, iterating through the 'submissions' dict.
        count = 1
        for key in self.submissions:

            # Ensure iteration of every comment. Replace the "More" objects of each submission.
            self.submissions[key].comments.replace_more(limit=0)


            # Create holder for dicts of comment data.
            list_of_items = []


            # Record desired data fields of each "Comment" object
            for comment in self.submissions[key].comments.list():

                try:

                    # Holder for all Comment data fields.
                    to_dict = vars(comment)


                    # Holder for selected data fields to be recorded.
                    sub_dict = {field: to_dict[field] for field in fields_for_comment_dict}


                    # Created recording for date and time of Comment creation.
                    date = str(datetime.fromtimestamp(vars(comment)['created_utc'])).split()
                    sub_dict['date_created'] = date[0]
                    sub_dict['time_created'] = date[1]


                    # Append constructed data structure to list for later JSON writing.
                    list_of_items.append(sub_dict)


                # Catch possible KeyError.
                except KeyError:

                    # Step for debugging checkpoint.
                    catalyst = comment


            # Define file location.
            suffix = 'r(news)_submission-' + self.submissions[key].id + '.json'
            write_path = '/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/Reddit/json_data/' + suffix


            # Write data to JSON file.
            try:
                # Write JSON object to file.
                with open(write_path, 'w+') as f:
                    json.dump(list_of_items, f, indent=2)

            # Catch possible IOError.
            except IOError:
                print("\tCould not locate JSON file.")


            # Output status.
            print('\t', count, key)
            count += 1


        # Output completion status.
        print('\tComplete.')

        return self




def main():
    """
    -main
    :return:
    """

    # Create an instance of the "DataMiner" class.
    data = DataCollector('hpTnFWPodmP85w', 'T2rZgWYrmqB_ULSOmIVZVn2ff8Q', "r/praw_tester's research_project")


    # Add the "news" subreddit to the Reddit instance of "data".
    data.add_subreddit('news')

    data.add_submissions(subreddit_name= 'news', which= 'full', recursion= False)

    # data.build_json_indexes()

    data.build_json_data()

    return 0



if __name__ == "__main__": main()








# EOF
