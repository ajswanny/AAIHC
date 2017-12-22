import DataCleaner
import pandas
import os

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import argparse

import numpy
import six

# [END Imports]


# [START Define Working Data]
# Define working data.

# DF is DataCleaner.run_datacleaner return value.
# major_df = DataCleaner.run_datacleaner()

#
# SDF_Body_series = major_df.body
# small_df_body_series = SDF_Body_series[:5000]

#
# SDataFrame = small_df_body_series.to_frame()
count = 24116

#
# CAT_DF = pandas.read_json('/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/DataObserver_data/categorized_df-to5000.json')

# The working aggregate Dataframe.
# major_df = major_df[:5000]
major_df = pandas.read_json('/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/DataObserver_data/categorized_df-major.json')
major_df = major_df.reset_index()


# Delete the base Dataframe.
# del base_DF
# Set the categories column.
# major_df["category"] = ""
# major_df["sentiment_score"] = ""
# the_sentiment_score = 0

# Training data sets.
# df_body_series_train = pd.Series()
# df_body_series_test = pd.Series()


# [END Define Working Data]

# [START Work]
def main():

    # Add the Category column.
    # SDataFrame["category"] = ""

    # tdf = pandas.read_json('/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/DataObserver_data/categorized_df-to5000.json')

    #
    # categorize()

    # major_df.to_json(
    #     "/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/DataMine/DataObserver_data/categorized_df-major.json")

    # print(major_df.to_string())

    return 0


def categorize():

    # Debug
    # print(major_df)

    for index, row in major_df.iterrows():
        #
        try:
            # Get the classification.
            text = major_df.loc[index, 'body']
            # Debug
            # print(text)
            classification = classify(text, verbose=False)
            # Split the categories identified.
            split_categories = split_labels(classification)
            # Get first identified category. (Has max confidence)
            first_category = next(iter(split_categories))

            # Add category to dataframe.
            major_df.loc[index, 'category'] = first_category

            # Add sentiment score.
            major_df.loc[index, 'sentiment_score'] = the_sentiment_score

        except:

            #
            try:
                #
                # print("Dropped a column")
                major_df.drop(index, inplace=True)

                # print("Dropped index: ", index)

            #
            except IndexError:
                #
                print("Encountered DF end")
                return

            #
            continue


# [STARTGoogleWork]
# Copyright 2017, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START def_classify]
    # MOD
def classify(text, verbose: bool):
    # MOD
    """Classify the input text into categories. """

    global the_sentiment_score

    # MOD
    global category
    # MOD
    language_client = language.LanguageServiceClient()

    document = language.types.Document(
        content=text,
        type=language.enums.Document.Type.PLAIN_TEXT)

    # Get the response.
    response = language_client.classify_text(document)
    # Get the "categories.
    categories = response.categories

    # Detect & record the sentiment of the text
    sentiment = language_client.analyze_sentiment(document=document).document_sentiment
    the_sentiment_score = sentiment.score

    # print('Text: {}'.format(text))
    # print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))

    result = {}

    for category in categories:
        # Turn the categories into a dictionary of the form:
        # {category.name: category.confidence}, so that they can
        # be treated as a sparse vector.
        result[category.name] = category.confidence

    if verbose:
        # MOD
        # print(text)
        # MOD
        for category in categories:

            print(u'=' * 20)
            print(u'{:<16}: {}'.format('category', category.name))
            print(u'{:<16}: {}'.format('confidence', category.confidence))


    # MOD
    if result[category.name] is None:
        return "RESULT-NA"
    # MOD

    return result


# [END def_classify]


# [START def_split_labels]
def split_labels(categories):
    """The category labels are of the form "/a/b/c" up to three levels,
    for example "/Computers & Electronics/Software", and these labels
    are used as keys in the categories dictionary, whose values are
    confidence scores.
    The split_labels function splits the keys into individual levels
    while duplicating the confidence score, which allows a natural
    boost in how we calculate similarity when more levels are in common.
    Example:
    If we have
    x = {"/a/b/c": 0.5}
    y = {"/a/b": 0.5}
    z = {"/a": 0.5}
    Then x and y are considered more similar than y and z.
    """
    _categories = {}
    for name, confidence in six.iteritems(categories):
        labels = [label for label in name.split('/') if label]
        for label in labels:
            _categories[label] = confidence

    return _categories

# [END def_split_labels]

# {ENDGoogleWork]

def count_words():
    word_count = 0

    # for item in df_body_series:
    #     print(item)

    # for item in df_body_series[0]:
    #     print(item)

    # print(df_body_series[0].split())


def clip():
    # df_body_series_train = SDF_Body_series[:22000]
    # print(df_body_series_train .tail())

    # Define
    # df_body_series_test = SDF_Body_series[22000:]
    # print(df_body_series_test.head())
    return


def length():
    # print(SDF_Body_series.describe())
    return


main()

# [END Work]
