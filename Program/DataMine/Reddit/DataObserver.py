# BOF

# Import necessary modules.
from google.cloud import language
from Reddit import DataCleaner

import pandas
import six



class DataObserver:
    """
    The DataObserver class generates the data structures for appropriate observation and analysis.
    """





# noinspection PyCompatibility
def main():

    # DataObserve = DataObserver()

    # Load meta-DataFrame from JSON file.
    path = '/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/Reddit/json_data/meta-df.json'
    df: pandas.DataFrame = pandas.read_json(path)


    # Sort the DataFrame's index.
    df = df.sort_index(axis= 0)


    # Sort the DataFrame's columns.
    df = df[['id', 'parent_id', 'subreddit_name_prefixed', 'body', 'ups', 'downs', 'score', 'controversiality',
             'created', 'date_created', 'time_created']]

    print(df.info())


    # The working aggregate Dataframe.
    # major_df = pandas.read_json(
    #     '/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/DataObserver_data/categorized_df-major.json')
    # major_df = major_df.reset_index()


    # Add the Category column.
    # SDataFrame["category"] = ""

    # tdf = pandas.read_json('/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/DataObserver_data/categorized_df-to5000.json')

    #
    # categorize()

    # major_df.to_json(
    #     "/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/DataObserver_data/categorized_df-major.json")

    # print(major_df.to_string())

    return 0





main()

# EOF