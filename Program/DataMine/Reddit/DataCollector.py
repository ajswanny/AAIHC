"""
DataCollector - Version 0.1
Copyright (c) 2018, Alexander Joseph Swanson Villares
"""

# BOF

# TODO: Finish documentation.

import json
import time
from datetime import datetime

import praw
import prawcore.exceptions


# For Raspberry Pi integration:
#   - Continuous retrieval, organization, and sorting of data


# noinspection PyCompatibility
class DataCollector:

    """ Declare the class data fields. """
    reddit_instance: praw.Reddit

    subreddits: dict
    subreddit_names: list

    submissions: dict
    submission_ids: list



    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        """
        Init.

        :param client_id:
        :param client_secret:
        :param user_agent:
        """

        self.reddit_instance = praw.Reddit(client_id=client_id,
                                           client_secret=client_secret,
                                           user_agent=user_agent)

        # Initialize fields.
        self.subreddits = dict()
        self.subreddit_names = list()

        self.submissions = dict()
        self.submission_ids = list()

        # Confirm instantiation.
        print("DataCollector instantiated.")



    def add_subreddit(self, subreddit_name: str):
        """
        Add a "Subreddit" object to the Reddit instance.

        :param subreddit_id:
        :return:
        """

        self.subreddits[subreddit_name] = self.reddit_instance.subreddit(subreddit_name)

        print("Successfully added subreddit: " + subreddit_name)

        self.subreddit_names.append(subreddit_name)


        return self



    def add_submissions(self, *args, subreddit_name: str, limit: int, which: str, recursion: bool):
        """
        Adds the specified "Submission" objects from the Top: All Time category to the Reddit instance.

        :param recursion:
        :param subreddit_name:
        :param limit:
        :param which:
        :param args: The IDs of the Submission objects to be added to 'submissions'.
        :return:
        """

        #
        complete = False


        # Output state.
        if not recursion:
            print("Adding Submissions...")

        # Add the specified Submission objects.
        if which == 'given':

            for arg in args:

                #
                submission_name = subreddit_name + '-' + arg

                #
                self.submissions[submission_name] = self.reddit_instance.submission(id=arg)


                # Output status.
                print("\t" + submission_name)


        # Add the Top: All Time Submissions for the given Subreddit if 'which' is true; amount determined by the
        # parameter 'limit'.
        if which == 'full':

            # Add submissions.
            for submission in self.subreddits[subreddit_name].top(time_filter= 'all', limit= limit):

                # Define the ID of the Submission respective to the current loop step.
                submission_id = submission.id


                # Recursively call 'add_submissions' with " which= 'given' " in order to add all Submissions with the
                # given 'limit'.
                self.add_submissions(
                    submission_id,
                    subreddit_name= subreddit_name,
                    which= 'given',
                    limit= limit,
                    recursion= True
                )


            # Set completion status.
            complete = True


        if complete:

            # Output completion status.
            print('Finished.\n')


        return self



    def prepare_build(self):
        """
        Handler method for any necessary pre-processing respective to: 'self.build_data()'.

        :return:
        """

        # Replace the "praw.MoreComments" objects of each submission.
        print("Preparing for serialization...")

        count = 1

        for key in self.submissions:
            self.submissions[key].comments.replace_more(limit=0)

            print('\t', count, key)

            count += 1

        print('\tComplete.')


        return self



    def build_json_indexes(self, build_version: str):
        """
        Creates a file listing all "Submission" IDs for later reference.

        :param build_version:
        :return:
        """

        # Define the file location.
        base = '/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/Reddit/json_data/json_paths_index_v'

        path = base + build_version + '.txt'


        # Open the file.
        with open(path, 'w+') as f:

            # Write each Submission's ID to the file.
            for key in self.submissions:

                f.write(self.submissions[key].id + '\n')


        return self



    def build_data(self, subreddit_name: str):
        """
        Serializes "Comment" data structures for each "Submission" in the submissions dict.

        :return:
        """

        global list_of_items


        # Define list to filter data to be recorded.
        fields_for_comment_dict = (
            'id', 'parent_id', 'subreddit_name_prefixed',
            'body',
            'controversiality', 'ups', 'downs', 'score', 'created'
        )


        # Output process.
        print("Beginning serialization of Submission objects. \nSerializing...")


        # Serialize each Submission's comments to a JSON file, iterating through the 'submissions' dict.
        count = 1
        for key in self.submissions:

            try:

                # Ensure iteration of every comment. Replace the "More" objects of each submission.
                self.submissions[key].comments.replace_more(limit=0)


                # Create holder for dicts of comment data.
                list_of_items = []


                # Record desired data fields of each "Comment" object
                for comment in self.submissions[key].comments.list():

                    # Holder for all Comment data fields.
                    to_dict = vars(comment)


                    # Holder for selected data fields to be recorded.
                    sub_dict = {field: to_dict[field] for field in fields_for_comment_dict}


                    # Created recording for date and time of Comment creation.
                    date = str(datetime.fromtimestamp(vars(comment)['created_utc'])).split()
                    sub_dict['date_created'] = date[0]
                    sub_dict['time_created'] = date[1]


                    # Define 'submission_id' field.
                    sub_dict['submission_id'] = key


                    # Append constructed data structure to list for later JSON writing.
                    list_of_items.append(sub_dict)

            # Catch 'timeout' exception; delay processing.
            except prawcore.exceptions.RequestException:

                time.sleep(60)


            # Define file location.
            suffix = 'r(' + subreddit_name + ')_submission-' + self.submissions[key].id + '.json'
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




def run_build(build_version: str, build_subreddit: str):
    """
    Builds a general instance and the data.

    :return: 0
    """

    # Create an instance of the "DataMiner" class.
    data_collector = DataCollector(client_id= 'hpTnFWPodmP85w',
                                   client_secret= 'T2rZgWYrmqB_ULSOmIVZVn2ff8Q',
                                   user_agent= "r/praw_tester's research_project")


    # Add the specified Subreddit to the Reddit instance of "data".
    data_collector.add_subreddit(subreddit_name= build_subreddit)


    # Create a dict of the Submissions in the specified Subreddit.
    data_collector.add_submissions(subreddit_name= build_subreddit, which= 'full', limit= 100, recursion= False)


    # Create a reference to the used Submission object IDs for later reference.
    data_collector.build_json_indexes(build_version= build_version)


    # Collect the data.
    data_collector.build_data(subreddit_name= build_subreddit)


    return 0



def main():
    """
    main.
    :return:
    """

    """ Official Program Run Command """
    # run_build(build_version= '1', build_subreddit= 'ukpolitics')



    # Create an instance of the "DataMiner" class.
    data_collector = DataCollector(client_id='hpTnFWPodmP85w',
                                   client_secret='T2rZgWYrmqB_ULSOmIVZVn2ff8Q',
                                   user_agent="r/praw_tester's research_project")

    data_collector.add_subreddit(subreddit_name='news')


    return 0



if __name__ == "__main__": main()



# EOF
