"""
DataCleaner - Version 0.1
Copyright (c) 2017, Alexander Joseph Swanson Villares
"""

# TODO: Redefine implementation to force functions to work on given DataFrames, rather than always the base DataFrame.

# Import necessary modules.
from unidecode import unidecode

import pandas, numpy
# import pprint



# [Begin Class: DataCleaner] #

# noinspection PyCompatibility
class DataCleaner:
    """
    The DataCleaner class is purposed for the creation of a Pandas "Dataframe" composed of an aggregate of the
    data collected with 'DataCollector'.
    """


    """ Declare the class's fields. """
    dataframe: pandas.DataFrame
    super_dataframe: pandas.DataFrame

    dataframes: dict

    json_path: str
    default_json_path: str
    json_paths: dict



    def __init__(self, init_super_df: bool, json_path: str, submission_id: str):
        """
        Init.
        :param process:
        :param json_path:
        :param submission_id:
        """

        # Set the default JSON file location for testing and debugging.
        self.default_json_path = \
            '/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/Reddit/json_data/r-news/r(news)_submission-3b6zln.json'


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


        dataframe_columns = (
            'id', 'parent_id', 'submission_id', 'subreddit_name_prefixed',
            'body', 'ups', 'downs', 'score', 'controversiality',
            'created', 'date_created', 'time_created'
        )

        # Create base Dataframe.
        self.dataframe = pandas.DataFrame(data= numpy.zeros((0, len(dataframe_columns))), columns= dataframe_columns)


        # Confirm instantiation.
        print("DataCleaner instantiated.")


        # Clean the base DataFrame and set it to the 'super_dataframe' field in order to initialize the meta-DataFrame.
        if init_super_df:

            # Initialize the meta-Dataframe.
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

            content = (x.strip() for x in content)

            submission_ids = content


        # Define the JSON file locations dict.
        for submission_id in submission_ids:

            # Create dynamic suffix for each Submission.
            suffix = 'r(news)_submission-' + submission_id + '.json'


            # Define the correct absolute path.
            json_path = \
                '/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/Reddit/json_data/r-news/' + suffix


            # Append to JSON file locations dict.
            self.json_paths[submission_id] = json_path


        return self



    def view_dataframe(self, *args, view_super: bool):
        """
        Outputs the base Dataframe or meta-DataFrame.
            - Can specify row or cell for base DataFrame.

        :param args:
        :param view_super:
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

        # Output the meta-DataFrame.
        elif view_super:
            print(self.super_dataframe.to_string())


        return self



    def clean(self):
        """
        Handler method for all base Dataframe cleaning operations.
        Defaults 'clean_dataframe_rows()': 'inplace' to True.
        :return:
        """

        # Clean the base Dataframe.
        self.organize_dataframe_columns()
        self.clean_dataframe_rows(inplace= True)


        return self



    def organize_dataframe_columns(self):
        """
        Redefines the base Dataframe with the correct column organization.
        :return:
        """

        # Redefine Dataframe rows.
        self.dataframe = self.dataframe[(
             'id', 'parent_id', 'submission_id', 'subreddit_name_prefixed',
             'body', 'ups', 'downs', 'score', 'controversiality',
             'created', 'date_created', 'time_created'
        )]


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



    def process(self, with_last: bool, process_super: bool, verbose: bool):
        """
        Creates unique DataFrames for all data subsets and appends them to the 'dataframes' dict field. That is,
            the data for each "Submission" object recorded by 'DataCollector'.

        :param with_last: Append to 'dataframes' the last DataFrame created and recorded to the base DataFrame.
        :param process_super:
        :param verbose:
        :return:
        """

        # Output status if 'verbose' is True.
        if verbose:
            print('Processing DataFrames...')


        # Iterate 'json_paths' dict field and store the data in each file as a DataFrame in 'dataframes'.
        step_count = 0
        for key in self.json_paths:

            # Append 'dataframes' with newly recorded DataFrame.
            self.append_dataframe(step= step_count, subreddit_id= key, mount= True)


            # Output status if 'verbose' is True.
            if verbose:
                print('\t', step_count, self.dataframe.parent_id[0])


            # Increment loop step counter.
            step_count += 1


        # Append the last DataFrame created and recorded to the base DataFrame if 'with_last' is true.
        if with_last:

            # Retrieve the 'parent_id' field from the base DataFrame to be used as the key for the last value in
            # 'dataframes'.
            last_id = self.dataframe.parent_id[0]

            # Append the base DataFrame to 'dataframes'.
            self.dataframes[last_id] = self.dataframe


        # Correctly redefine the meta-DataFrame if 'process_super' is True.
        if process_super:

            self.process_super_dataframe()


        print('Finished.\n')


        return self



    def append_dataframe(self, step: int, subreddit_id: str, mount: bool):
        """
        Appends a new Dataframe to the 'dataframes' dict field.
            - Note: The first DataFrame appended to 'dataframes' is always the current base DataFrame.

        :param step:
        :param subreddit_id: The "Subreddit" object ID for mounting to base Dataframe.
        :param mount: Redefine base Dataframe.
        :param process: Clean the base Dataframe.
        :return:
        """

        # Get Submission ID in order to identify the Submission data to be appended.
        submission_id = list(self.json_paths.keys())[step]


        # Redefine the base Dataframe if 'mount' is true.
        if mount:
            self.load_new_dataframe(subreddit_id= subreddit_id)


        try:
            # Append to Dataframes dict.
            self.dataframes[submission_id] = self.dataframe

        except LookupError:

            print('Could not append DataFrame for Submission: ' + submission_id)


        return self



    def load_new_dataframe(self, subreddit_id: str):
        """
        Loads a new Dataframe into the base Dataframe.
        :return: pandas.Dataframe
        """

        try:
            # Define JSON path.
            path = self.json_paths[subreddit_id]


            # Redefine base Dataframe.
            self.dataframe = pandas.read_json(path)

        except ValueError:

            print(ValueError.__traceback__)


        # Clean the base Dataframe.
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

# [End Class: DataCleaner] #




def build_all(return_df: bool, record: bool):
    """
    Builds all base DataFrames and meta-DataFrames.
    :param return_df:
    :param record:
    :return:
    """

    # Instantiate DataCleaner
    data_clean = DataCleaner(
        init_super_df=True,
        json_path='default',
        submission_id='None'
    )


    # Build the workable Dataframe; process the dataframes.
    """ 
        Warning: Setting 'process_super' to True will cause a doubled DataFrame as 'process_super_dataframe()' is
        called below.
    """
    data_clean.process(with_last=True, process_super= False, verbose= False)


    # Clean up Dataframe. Remove rows where the 'body' column contains: "[deleted]" or "[removed]".
    data_clean.clean()


    # Process Super Dataframe.
    data_clean.process_super_dataframe()


    # Record the meta-DataFrame to a JSON file if 'record' is True.
    if record:

        # Define the file location.
        path = '/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/Reddit/json_data/meta-df.json'

        # Output to JSON file.
        data_clean.super_dataframe.to_json(path)


    # Return the meta-DataFrame if 'return_df' is True.
    if return_df:
        return data_clean.super_dataframe

    else:
        return 0



# noinspection PyCompatibility
def build_basic():
    """
    Builds the meta-DataFrame by loading from JSON file.
    :return: The meta-DataFrame.
    """

    # Load meta-DataFrame from JSON file.
    path = '/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/Reddit/json_data/meta-df.json'
    df: pandas.DataFrame = pandas.read_json(path)


    # Sort the DataFrame's index.
    df = df.sort_index(axis=0)


    df = df.drop_duplicates(subset='id', keep='first')


    # Sort the DataFrame's columns.
    df = df[(
        'id', 'parent_id', 'submission_id', 'subreddit_name_prefixed',
        'body', 'ups', 'downs', 'score', 'controversiality',
        'created', 'date_created', 'time_created'
    )]


    return df



def main():
    """

    :return:
    """

    # Builds and returns meta-DataFrame.
    df = build_all(return_df= True, record= False)


    # Build and records meta-DataFrame to JSON file.
    # build_all(return_df= False, record= True)


    #
    # df = build_basic()


    #
    print(df.info())

main()



# EOF
