# BOF

# Import necessary modules.
# import DataProcessor
import pandas



class DataObserver:
    """
    The DataObserver class generates the data structures for appropriate observation and analysis.
    """

    df = pandas.DataFrame()

    def __init__(self):
        """
        Init.
        """




# noinspection PyCompatibility
def build_simply(file_path: str) -> pandas.DataFrame:
    """
    Builds a DataFrame with correct respective configurations by loading from JSON file.

    :origin: 'DataCleaner.py'. Modified.
    :return: The meta-DataFrame.
    """

    # Load meta-DataFrame from JSON file.
    df: pandas.DataFrame = pandas.read_json(file_path)


    # Define correct data types.
    # df = df.astype({'category': "category"})


    # Perform final check for duplicated DataFrame rows.
    df = df.drop_duplicates(subset='id', keep='first')


    # Perform final check for null values.
    # df = df.loc[df['sentiment_score'].notnull()]
    # df = df.loc[df['sentiment_magnitude'].notnull()]


    # Sort the DataFrame's index.
    df = df.sort_index(axis= 0)


    # Perform final check for Dataframe row organization.
    df = df.reindex_axis(
        (
            'id', 'parent_id', 'submission_id', 'subreddit_name_prefixed', 'body',
            'ups', 'downs', 'score', 'controversiality', 'category', 'sentiment_score', 'sentiment_magnitude',
            'created', 'date_created', 'time_created'
        ),
        axis= 1
    )


    return df



def placer():
    """
    A placer for processed DataFrame aggregation.
    :return:
    """

    # Import Frames
    x = build_simply(
        '/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/Reddit/json_data/Processed_DataFrames/r-worldnews/DF-version_0/DF_v0.json')
    y = pandas.read_json(
        '/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/Reddit/json_data/Processed_DataFrames/r-worldnews/DF-version_1/DF_v1.json')

    # Concatenate Frames.
    z = x.append(y)

    # Clean Frame.
    z.reset_index(drop=True, inplace=True)
    z.sort_index(inplace=True, axis=0)

    # Record Frame.
    z.to_json(
        path_or_buf='/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/Reddit/json_data/Processed_DataFrames/r-worldnews/DF-version_2/DF_v2.json')

    return 0



# noinspection PyCompatibility
def main():

    #
    # df = build_simply(file_path= '/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/Reddit/JSON_Data/Processed_DataFrames/r-worldnews/DF-version_2/DF_v2.json')
    #
    # df.drop(['body'], axis=1, inplace= True)
    # df = df.truncate(after= 1199)
    #
    #
    #
    # df.to_csv(path_or_buf='/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/Reddit/reddit_data.csv',
    #           na_rep= 'N/A'
    # )
    #
    #
    #
    #
    # print(df.info())



    return 0


# EOF
