# BOF

import pandas, pprint
from unidecode import unidecode


# noinspection PyCompatibility
class DataCleaner:

    dataframe: pandas.DataFrame
    super_dataframe: pandas.DataFrame

    dataframes: dict

    json_path: str
    default_json_path: str
    json_paths: dict


    def __init__(self, submission_id: str, p_json_path: str, process: bool):
        """

        :param json_path:
        """

        # Set the default JSON file location.
        self.default_json_path = '/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/json_data/json_data.json'

        # Initialize JSON file locations map.
        self.json_paths = {}
        self.init_json_map()

        # Initialize meta-map.
        self.dataframes = {}

        #
        if p_json_path == 'default_path':
            self.json_path = self.default_json_path

        else:
            self.json_path = p_json_path
            self.json_paths[submission_id] = p_json_path

        # Create Dataframe.
        self.dataframe = pandas.read_json(self.json_path)

        # Confirm instantiation.
        print("DataCleaner instantiated.")

        if process:

            self.clean()

            # Instantiate aggregate Dataframe.
            self.super_dataframe = self.dataframe


    def init_json_map(self):
        """

        :return:
        """

        sub_ids = []

        with open('/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/json_data/json_paths') as f:

            content = f.readlines()

            content = [x.strip() for x in content]

            sub_ids = content

        for item in sub_ids:

            special = 'r(news)_submission-' + item + '.json'

            json_path = '/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/json_data/' + special

            self.json_paths[item] = json_path



        # self.json_paths['3b6zln'] \
        #     = '/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/json_data/r(news)_submission-3b6zln.json'
        # self.json_paths['5r5qx4'] \
        #     = '/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/json_data/r(news)_submission-5r5qx4.json'
        # self.json_paths['5vznv8'] \
        #     = '/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/json_data/r(news)_submission-5vznv8.json'
        # self.json_paths['6a8ji6'] \
        #     = '/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/json_data/r(news)_submission-6a8ji6.json'
        # self.json_paths['6oi3gu'] \
        #     = '/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/json_data/r(news)_submission-6oi3gu.json'
        # self.json_paths['6zw2mp'] \
        #     = '/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/json_data/r(news)_submission-6zw2mp.json'
        # self.json_paths['7ej943'] \
        #     = '/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/json_data/r(news)_submission-7ej943.json'
        # self.json_paths['7fwv10'] \
        #     = '/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/json_data/r(news)_submission-7fwv10.json'
        # self.json_paths['72xfdb'] \
        #     = '/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/json_data/r(news)_submission-72xfdb.json'
        # self.json_paths['79v2cg'] \
        #     = '/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/json_data/r(news)_submission-79v2cg.json'

    def view_dataframe(self, *args):
        """

        :param args:
        :return:
        """

        # Output entire Dataframe if no cell is specified.
        if not args:
            print(self.dataframe.to_string())

        # Output a column.
        elif len(args) == 1:
            print(self.dataframe[args[0]])

        # Output a cell.
        else:
            print(self.dataframe[args[0]][args[1]])


    # Builds a Dataframe with the correct column organization.
    def organize_dataframe(self):
        """

        :return:
        """

        self.dataframe = self.dataframe[
            ['id', 'parent_id', 'subreddit_name_prefixed', 'body', 'ups', 'downs', 'score', 'controversiality',
             'created', 'date_created', 'time_created']]


    def clean_dataframe_rows(self, inplace: bool):
        """

        :return:
        """

        # Remove Null-equivalent values.
        temp_df = self.dataframe.query("body != '[deleted]'")
        temp_df = temp_df.query("body != '[removed]'")

        # Reset the index.
        temp_df = temp_df.reset_index(drop=True)

        # Define and apply lambda function to decode possible unicode characters.
        temp_df['body'] = temp_df['body'].apply(lambda x: unidecode(x))

        # Drop duplicate rows.
        # In: 'body' column.
        # Keeping the first occurrence in the column.
        # Removing the row, instead of returning a boolean indicator.
        temp_df.drop_duplicates(subset='body', keep='first', inplace= False)

        self.dataframe = temp_df

        if not inplace:
            return temp_df

    def clean(self):
        """

        :return:
        """

        self.organize_dataframe()
        self.clean_dataframe_rows(inplace= True)


    def process(self, with_last: bool):
        """
        Create unique dataframes for all data subsets.
        :return:
        """

        for key in self.json_paths:

            self.new_dataframe(subreddit_id= key, mount= True, process= True)

        if with_last:

            self.dataframes['t3_79v2cg'] = self.dataframe


    def new_dataframe(self, subreddit_id: str, mount: bool, process: bool):
        """

        :param process:
        :param subreddit_id:
        :param mount:
        :return:
        """

        # Get Submission ID.
        submission_id = self.dataframe.parent_id[0]

        # Append to dataframe collection.
        self.dataframes[submission_id] = self.dataframe

        if mount:
            self.read_new_dataframe(subreddit_id=subreddit_id)

        if process:
            self.clean()


    def read_new_dataframe(self, subreddit_id: str):
        """

        :return: pandas.Dataframe
        """
        json_path = self.json_paths[subreddit_id]

        self.dataframe = pandas.read_json(json_path)

        self.clean()


    def init_super_dataframe(self):

        self.super_dataframe = self.clean_dataframe_rows(inplace= False)


    def append_super_dataframe(self, dataframe_to_append: pandas.DataFrame):

        self.super_dataframe = self.super_dataframe.append(dataframe_to_append)
        self.super_dataframe = self.super_dataframe.reset_index(drop= True)

    def process_super_dataframe(self):

        for key in self.dataframes:
            self.append_super_dataframe(self.dataframes[key])


def analyze():
    """

    :param series_cell:
    :return:
    """


def run_datacleaner():
    """

    :return:
    """

    # Instantiate DataCleaner
    data_clean = DataCleaner(submission_id='3b6zln', process= True,
        p_json_path='/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/json_data/r(news)_submission-3b6zln.json')

    # Build the workable Dataframe.
    # Clean up Dataframe. Remove rows with 'body' column containing "[deleted]" or "[removed]".
    data_clean.organize_dataframe()
    data_clean.clean_dataframe_rows(inplace= True)

    # Process the dataframes.
    data_clean.process(with_last= True)

    # Process Super Dataframe.
    data_clean.process_super_dataframe()

    return data_clean.super_dataframe


# EOF
