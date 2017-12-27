"""
DataCollector - Version 0.1
Copyright (c) 2017, Alexander Joseph Swanson Villares
"""

# TODO: Finish documentation.

import json
import praw
from datetime import datetime


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



    def add_subreddit(self, subreddit_id: str):
        """
        Add a "Subreddit" object to the Reddit instance.

        :param subreddit_id:
        :return:
        """

        self.subreddits[subreddit_id] = self.reddit_instance.subreddit(subreddit_id)

        print("Successfully added subreddit: " + subreddit_id)

        self.subreddit_names.append(subreddit_id)


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


        # Add the top 50 Submissions for the given Subreddit if 'which' is true.
        if which == 'full':

            # Add submissions.
            for submission in self.subreddits['news'].top(time_filter= 'all', limit= limit):

                # Define the ID of the Submission respective to the current loop step.
                submission_id = submission.id


                # Recursively call 'add_submissions' with " which= 'given' " in order to add all Submissions with the
                # given 'limit'.
                self.add_submissions(
                    submission_id,
                    subreddit_name= 'news',
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



    def build_json_indexes(self, file_path: str):
        """
        Creates a file listing all "Submission" IDs for later reference.

        :param file_path:
        :return:
        """

        # Define the file location.
        if file_path == 'default':
            path = \
                '/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/Reddit/json_data/json_paths_index_v0.txt'

        else:
            path = file_path


        # Open the file.
        with open(path, 'w+') as f:

            # Write each Submission's ID to the file.
            for key in self.submissions:

                f.write(self.submissions[key].id + '\n')


        return self



    def build_data(self):
        """
        Serializes "Comment" data structures for each "Submission" in the submissions dict.

        :return:
        """

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




def run_build():
    """
    Builds a general instance and the data.

    :return: 0
    """

    # Create an instance of the "DataMiner" class.
    data_collector = DataCollector('hpTnFWPodmP85w', 'T2rZgWYrmqB_ULSOmIVZVn2ff8Q', "r/praw_tester's research_project")


    # Add the "news" subreddit to the Reddit instance of "data".
    data_collector.add_subreddit('news')


    # Create a map of the Submissions in the 'news' Subreddit.
    data_collector.add_submissions(subreddit_name='news', which='full', limit= 100, recursion=False)


    # count = 0
    # for key in data_collector.submissions:
    #
    #     data_collector.submissions.pop(key)
    #
    #     count += 1
    #
    #     if count == 49: break



    # Create a reference to the used Submission object IDs for later reference.
    data_collector.build_json_indexes(file_path= 'default')


    # Collect the data.
    # data_collector.build_data()


    return 0



def main():
    """
    -main
    :return:
    """

    run_build()

    return 0



if __name__ == "__main__": main()








# EOF
