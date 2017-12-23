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


    """ Declare the class data fields. """
    # The base "DataFrame".
    DF = pandas.DataFrame

    # The shortened base DataFrame.
    SDF = pandas.DataFrame

    # The "Series" composed of the 'body' column of the base DataFrame 'DF'.
    body = pandas.Series
    short_body = pandas.Series

    # The DataFrame version of 'body'.
    body_df = pandas.DataFrame


    def __init__(self):
        """
        Defines the work data.
        :return:
        """

        # Generate the base DataFrame from 'DataCleaner'.
        self.DF = DataCleaner.build_basic(return_df= True)

        # Generate the shortened base DataFrame.
        self.SDF = self.DF.copy(deep= True)

        # Create a "Series" from the base DataFrame 'DF'.
        self.body = self.DF.body


        # Create a shortened Series.
        self.short_body = self.body[:5000]


        # Convert the 'body' Series into a workable DataFrame.
        self.body_df = self.short_body.to_frame()




    def categorize(self, which: str):
        """

        :param which:
        :return:
        """

        if which == 'base':

            for index, row in self.DF.iterrows():
                #
                try:

                    # Get the body text for classification.
                    text = self.DF.loc[index, 'body']


                    # Run [Google, Inc.]:'classify' to get Category and Sentiment evaluations.
                    classification = classify(text, verbose= False)


                    # Split the identified categories.
                    split_categories = split_labels(classification)


                    # Get first identified category. (Has max confidence)
                    first_category = next(iter(split_categories))

                    # Add category to dataframe.
                    self.DF.loc[index, 'category'] = first_category

                    # Add sentiment score.
                    self.DF.loc[index, 'sentiment_score'] = the_sentiment_score

                # Catch errors with the Google Cloud API.
                except:

                    #
                    try:
                        #
                        # print("Dropped a column")
                        self.DF.drop(index, inplace=True)

                        # print("Dropped index: ", index)

                    #
                    except IndexError:
                        #
                        print("Encountered DF end")
                        return

                    #
                    continue






def main():

    DataObserve = DataObserver()


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




# [START Google Work]

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


# {END Google Work]

def count_words():
    word_count = 0

    # for item in df_body_series:
    #     print(item)

    # for item in df_body_series[0]:
    #     print(item)

    # print(df_body_series[0].split())




main()

# EOF