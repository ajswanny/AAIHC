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


    def __init__(self, submission_id: str, json_path: str, process: bool):
        """
        Init.
        :param submission_id:
        :param json_path:
        :param process:
        """

        # Set the default JSON file location.
        self.default_json_path = '/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/json_data/json_data.json'

        # Initialize JSON file locations map.
        self.json_paths = {}
        self.init_json_map()

        # Initialize meta map.
        self.dataframes = {}

        # Define JSON file locations.
        if json_path == 'default_path':
            self.json_path = self.default_json_path

        else:
            self.json_path = json_path
            self.json_paths[submission_id] = json_path

        # Create base Dataframe.
        self.dataframe = pandas.read_json(self.json_path)

        # Confirm instantiation.
        print("DataCleaner instantiated.")

        if process:

            self.clean()

            # Instantiate aggregate Dataframe.
            self.super_dataframe = self.dataframe



    def init_json_map(self):
        """
         Defines the JSON file locations respective to each "Submission" object.
        :return:
        """

        submission_ids = []

        # Read the JSON file locations from the source file.
        with open('/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/Reddit/json_data/json_paths') as f:

            # Read, organize, and record input.
            content = f.readlines()

            content = [x.strip() for x in content]

            submission_ids = content


        # Define the JSON file locations dict.
        for submission_id in submission_ids:

            # Create dynamic suffix for each Submission.
            suffix = 'r(news)_submission-' + submission_id + '.json'

            # Define the correct absolute path.
            json_path = '/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/Reddit/json_data/' + suffix

            # Append to JSON file locations dict.
            self.json_paths[submission_id] = json_path


        return 0



    def view_dataframe(self, *args):
        """
        Allows viewing of the base Dataframe with specified rows or cells.
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


        return 0



    def clean(self):
        """
        Handler method for all base Dataframe cleaning operations.
        :return:
        """

        # Clean the base Dataframe.
        self.organize_dataframe()
        self.clean_dataframe_rows(inplace= True)


        return 0



    def organize_dataframe(self):
        """
        Redefines the base Dataframe with the correct column organization.
        :return:
        """

        # Redefine Dataframe rows.
        self.dataframe = self.dataframe[
            ['id', 'parent_id', 'subreddit_name_prefixed',
             'body', 'ups', 'downs', 'score', 'controversiality',
             'created', 'date_created', 'time_created']]


        return 0



    def clean_dataframe_rows(self, inplace: bool):
        """
        Cleans the base Dataframe's rows.
        Removes duplicate rows, null values, etc.
        :return:
        """

        # Define a temporary working Dataframe.
        temp_df = self.dataframe.copy(deep= True)


        # Remove null values.
        temp_df = temp_df.query("body != '[deleted]'")
        temp_df = temp_df.query("body != '[removed]'")


        # Reset the index.
        temp_df = temp_df.reset_index(drop= True)


        # Define and apply lambda function to decode possible unicode characters.
        temp_df['body'] = temp_df['body'].apply(lambda x: unidecode(x))


        # Drop duplicate rows in 'body' column keeping the first occurrence.
        # Remove duplicate rows.
        temp_df.drop_duplicates(subset= 'body', keep= 'first', inplace= False)


        # Redefine Dataframe if 'inplace' is true.
        if inplace:
            self.dataframe = temp_df


        # Return placer Dataframe if 'inplace' is false.
        if not inplace:
            return temp_df


        return 0



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
        :param mount: Redefines base Dataframe if true.
        :return:
        """

        # Get Submission ID.
        submission_id = self.dataframe.parent_id[0]

        # Append to Dataframe collection.
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
        """

        :return:
        """

        self.super_dataframe = self.clean_dataframe_rows(inplace= False)



    def append_super_dataframe(self, dataframe_to_append: pandas.DataFrame):
        """

        :param dataframe_to_append:
        :return:
        """

        self.super_dataframe = self.super_dataframe.append(dataframe_to_append)
        self.super_dataframe = self.super_dataframe.reset_index(drop= True)


    def process_super_dataframe(self):
        """

        :return:
        """

        for key in self.dataframes:
            self.append_super_dataframe(self.dataframes[key])


def main():
    """

    :return:
    """

    # Instantiate DataCleaner
    data_clean = DataCleaner(submission_id='3b6zln', process= True,
        json_path='/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/json_data/r(news)_submission-3b6zln.json')

    # Build the workable Dataframe.
    # Clean up Dataframe. Remove rows with 'body' column containing "[deleted]" or "[removed]".
    data_clean.organize_dataframe()
    data_clean.clean_dataframe_rows(inplace= True)

    # Process the dataframes.
    data_clean.process(with_last= True)

    # Process Super Dataframe.
    data_clean.process_super_dataframe()



# EOF
