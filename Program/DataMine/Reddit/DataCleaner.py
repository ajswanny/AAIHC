# BOF

import pandas, pprint
from unidecode import unidecode


# noinspection PyCompatibility
class DataCleaner:
    """
    The DataCleaner class is purposed for the creation of a Pandas "Dataframe" composed of an aggregate of the
    data collected with 'DataCollector'.
    """

    # Declare the class's fields.
    dataframe: pandas.DataFrame
    super_dataframe: pandas.DataFrame

    dataframes: dict

    json_path: str
    default_json_path: str
    json_paths: dict
    # ---


    def __init__(self, process: bool, json_path: str, submission_id: str):
        """
        Init.
        :param json_path:
        :param process:
        :param submission_id:
        """

        # Set the default JSON file location.
        self.default_json_path = \
            '/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/Reddit/json_data/json_data.json'


        # Initialize JSON file locations map.
        self.json_paths = {}
        self.init_json_map()


        # Initialize DataFrames collection dict.
        self.dataframes = {}


        # Define default JSON file location.
        if json_path == 'default':
            self.json_path = self.default_json_path

        # Define "Submission" object-specific JSON file location; append to the 'json_paths' dict field.
        else:
            self.json_path = json_path
            self.json_paths[submission_id] = json_path


        # Create base Dataframe.
        self.dataframe = pandas.read_json(self.json_path)


        # Confirm instantiation.
        print("DataCleaner instantiated.")


        # Clean the base DataFrame and set it to the 'super_dataframe' field.
        if process:

            self.clean()

            # Instantiate meta-Dataframe.
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


        return self



    def view_dataframe(self, *args):
        """
        Allows viewing of the base Dataframe with specified rows or cells.
        :param args:
        :return:
        """

        # Output entire base Dataframe if no cell is specified.
        if not args:
            print(self.dataframe.to_string())

        # Output a column.
        elif len(args) == 1:
            print(self.dataframe[args[0]])

        # Output a cell.
        elif len(args) == 2:
            print(self.dataframe[args[0]][args[1]])


        return self



    def clean(self):
        """
        Handler method for all base Dataframe cleaning operations.
        Defaults 'clean_dataframe_rows()': 'inplace' to True.
        :return:
        """

        # Clean the base Dataframe.
        self.organize_dataframe()
        self.clean_dataframe_rows(inplace= True)


        return self



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


        return self



    def clean_dataframe_rows(self, inplace: bool):
        """
        Cleans the base Dataframe's rows.
        Removes duplicate rows, null values, etc.
        :return:
        """

        # Define a temporary work Dataframe.
        temp_df = self.dataframe.copy(deep= True)


        # Remove null values.
        temp_df = temp_df.query("body != '[deleted]'")
        temp_df = temp_df.query("body != '[removed]'")


        # Reset the index.
        temp_df = temp_df.reset_index(drop= True)


        # Define and apply lambda function to decode possible unicode characters.
        temp_df['body'] = temp_df['body'].apply(lambda x: unidecode(x))


        # Remove duplicate rows in 'body' column keeping the first occurrence.
        temp_df.drop_duplicates(subset= 'body', keep= 'first', inplace= False)


        # Redefine base Dataframe if 'inplace' is true.
        if inplace:
            self.dataframe = temp_df


        # Return work Dataframe if 'inplace' is false.
        if not inplace:
            return temp_df


        return self



    def process(self, with_last: bool):
        """
        Creates unique DataFrames for all data subsets.
        :return:
        """

        # Iterate 'json_paths' dict field and store the data in each file as a DataFrame in the 'dataframes' dict field.
        for key in self.json_paths:

            # Append 'dataframes' with newly recorded DataFrame.
            self.append_dataframe(subreddit_id= key, mount= True, process= True)

        if with_last:

            self.dataframes['t3_79v2cg'] = self.dataframe



    def load_new_dataframe(self, subreddit_id: str):
        """
        Loads a new Dataframe into the base Dataframe.
        :return: pandas.Dataframe
        """

        # Define JSON path.
        path = self.json_paths[subreddit_id]


        # Redefine base Dataframe.
        self.dataframe = pandas.read_json(path)


        # Clean the base Dataframe.
        self.clean()


        return self



    def append_dataframe(self, subreddit_id: str, mount: bool, process: bool):
        """
        Appends a new Dataframe to the 'dataframes' dict field.
        :param subreddit_id: The "Subreddit" object ID for mounting to base Dataframe.
        :param mount: Redefine base Dataframe.
        :param process: Clean the base Dataframe.
        :return:
        """

        # Get Submission ID.
        submission_id = self.dataframe.parent_id[0]


        # Append to Dataframes dict.
        self.dataframes[submission_id] = self.dataframe


        # Redefine base Dataframe if 'mount' is true.
        if mount:
            self.load_new_dataframe(subreddit_id= subreddit_id)


        # Clean the base Dataframe if 'process' true.
        if process:
            self.clean()


        return self



    def append_super_dataframe(self, df_to_append: pandas.DataFrame):
        """
        Appends a new Dataframe to the meta-DataFrame.
        :param df_to_append:
        :return:
        """

        # Append 'super_dataframe'; reset the index.
        self.super_dataframe = self.super_dataframe.append(df_to_append)
        self.super_dataframe = self.super_dataframe.reset_index(drop= True)


        return self



    def process_super_dataframe(self):
        """
        Handler for processing of meta-Dataframe.
            1. Appends each Dataframe in 'dataframes' field to the meta-Dataframe.

        :return:
        """

        # Iterate 'dataframes' dict field and append each value to the meta-DataFrame.
        for key in self.dataframes:
            self.append_super_dataframe(self.dataframes[key])


        return self





def main():
    """

    :return:
    """

    # Instantiate DataCleaner
    data_clean = DataCleaner(
        process= False,
        json_path= 'default',
        submission_id = 'None')


    # Build the workable Dataframe.
    # Clean up Dataframe. Remove rows where the 'body' column contains: "[deleted]" or "[removed]".
    data_clean.clean().view_dataframe()


    # Process the dataframes.
    # data_clean.process(with_last= True)


    # Process Super Dataframe.
    data_clean.process_super_dataframe()

main()

# EOF
