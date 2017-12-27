"""
DataProcessor - Version 0.2
Copyright (c) 2017, Alexander Joseph Swanson Villares
"""

# TODO: Finish documentation.

# Import dependencies.
from Reddit import DataCleaner

# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.naive_bayes import MultinomialNB
# from sklearn.model_selection import learning_curve

# from nltk.sentiment.vader import SentimentIntensityAnalyzer
"""
Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for
Sentiment Analysis of Social Media Text. Eighth International Conference on
Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
"""

from google.cloud import language
import google.api_core.exceptions

import numpy
import six
import pandas
import time


# class MachineLearningModel:
#
#     # TODO
#     # NOTE: MUST REDEFINE; DataObserver no longer provides this info; currently using empty DataFrame as template.
#     # df = DataObserver.major_df
#     df = pandas.DataFrame
#
#     df = df.loc[df['sentiment_score'] != 0]
#
#     # df = df.loc[df["category"] == ""]
#     # df = df.loc[df["sentiment_score"]]
#
#
#     # Set X and y.
#     dataframe_X = df["body"]
#     dataframe_y = df["sentiment_score"]
#
#     # Create feature vectors with a Term Frequency...
#     # Parameters borrowed from @bonzanini
#     vectorizer = TfidfVectorizer(min_df= 5,                 # Minimum frequency.
#                                  max_df = 0.8,              # Maximum frequency.
#                                  lowercase= True,
#                                  strip_accents= 'unicode',
#                                  stop_words= 'english',     # 'Are', 'you', etc.
#                                  sublinear_tf= True,
#                                  use_idf= True
#                                  )
#
#
#     # Split train and test data.
#     x_train, x_test, y_train, y_test = train_test_split(dataframe_X, dataframe_y, test_size=0.2, random_state=4)
#
#
#     # Convert y axis data to integers.
#     y_train = y_train.astype('int')
#     y_test = y_test.astype('int')
#     y_test_array = numpy.array(y_test)
#
#
#     # Vectorize the training and testing x axis.
#     train_vectors_X = vectorizer.fit_transform(x_train)
#     test_vectors_X = vectorizer.transform(x_test)
#
#
#     # Apply Naive Bayes...
#     Multinomial_NB = MultinomialNB()
#     Multinomial_NB.fit(train_vectors_X, y_train)
#
#
#     # Assess
#     assessment = Multinomial_NB.predict(test_vectors_X)
#     assessment_array = numpy.array(assessment)
#
#
#     # Identify accuracy.
#     n = 0
#     for i in range(len(assessment)):
#
#         if assessment[i] == y_test_array[i]:
#             n += 1
#
#
#     # Percentage accuracy.
#     # accuracy = n / len(assessment)
#
#     # print("Accuracy: ", accuracy)
#
#     # Credit to: Sci-Kit Learn Staff
#     def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None,
#                             n_jobs=1, train_sizes=numpy.linspace(.1, 1.0, 5)):
#         """
#         Generate a simple plot of the test and training learning curve.
#
#         Parameters
#         ----------
#         estimator : object type that implements the "fit" and "predict" methods
#             An object of that type which is cloned for each validation.
#
#         title : string
#             Title for the chart.
#
#         X : array-like, shape (n_samples, n_features)
#             Training vector, where n_samples is the number of samples and
#             n_features is the number of features.
#
#         y : array-like, shape (n_samples) or (n_samples, n_features), optional
#             Target relative to X for classification or regression;
#             None for unsupervised learning.
#
#         ylim : tuple, shape (ymin, ymax), optional
#             Defines minimum and maximum yvalues plotted.
#
#         cv : int, cross-validation generator or an iterable, optional
#             Determines the cross-validation splitting strategy.
#             Possible inputs for cv are:
#               - None, to use the default 3-fold cross-validation,
#               - integer, to specify the number of folds.
#               - An object to be used as a cross-validation generator.
#               - An iterable yielding train/test splits.
#
#             For integer/None inputs, if ``y`` is binary or multiclass,
#             :class:`StratifiedKFold` used. If the estimator is not a classifier
#             or if ``y`` is neither binary nor multiclass, :class:`KFold` is used.
#
#             Refer :ref:`User Guide <cross_validation>` for the various
#             cross-validators that can be used here.
#
#         n_jobs : integer, optional
#             Number of jobs to run in parallel (default 1).
#         """
#         plt.figure()
#         plt.title(title)
#         if ylim is not None:
#             plt.ylim(*ylim)
#         plt.xlabel("Training examples")
#         plt.ylabel("Score")
#         train_sizes, train_scores, test_scores = learning_curve(
#             estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
#         train_scores_mean = numpy.mean(train_scores, axis=1)
#         train_scores_std = numpy.std(train_scores, axis=1)
#         test_scores_mean = numpy.mean(test_scores, axis=1)
#         test_scores_std = numpy.std(test_scores, axis=1)
#         plt.grid()
#
#         plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
#                          train_scores_mean + train_scores_std, alpha=0.1,
#                          color="r")
#         plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
#                          test_scores_mean + test_scores_std, alpha=0.1, color="g")
#         plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
#                  label="Training score")
#         plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
#                  label="Cross-validation score")
#
#         plt.legend(loc="best")
#         return plt
#
#
#     plt = plot_learning_curve(Multinomial_NB, "Multinomial Naive Bayes TF-IDF", train_vectors_X, y_train)
#     plt.show()

# [Begin Class: DataCleaner] #

class DataProcessor:
    """
    The DataProcessor class prepares data for observation and analysis.
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
        Init.
        :return:
        """

        # Generate the base DataFrame from 'DataCleaner'.
        self.DF = DataCleaner.build_simply()


        # Generate the shortened base DataFrame.
        self.SDF = self.DF.copy(deep=True)


        # Create a "Series" from the base DataFrame 'DF'.
        self.body = self.DF.body


        # Create a shortened Series.
        self.short_body = self.body[:5000]


        # Convert the 'body' Series into a workable DataFrame.
        self.body_df = self.short_body.to_frame()




    def view_dataframe(self, *args):
        """
        Outputs 'DF' in a formatted matter.
            - Can specify row or cell.

        Origin: 'DataCleaner.py'

        :param args:
        :return:
        """

        # Output entirety of 'DF' if no cell is specified.
        if not args:
            print(self.DF.to_string())

        # Output a column by index.
        elif len(args) == 1:
            print(self.DF[args[0]])

        # Output a cell.
        elif len(args) == 2:
            print(self.DF[args[0]][args[1]])


        return self



    def resize_dataframe(self, index_cap: int):
        """
        Re-sizes 'DF', including all data with index below 'index_cap'.
        :param index_cap:
        :return:
        """

        # Resize 'DF'.
        self.DF = self.DF.truncate(after= index_cap)


        return self



    def organize_dataframe(self, action: str):
        """
        Performs organizational actions on 'DF'.
        :param action:
            - reindex:
        :return:
        """

        # Reorganize the index.
        if action == 'reindex':
            self.DF.reset_index(drop= True, inplace= True)


        return self



    def prepare_dataframe(self):
        """
        Performs any pre-processing on 'DF' needed.
        :return:
        """

        # Define the columns.
        columns = (
                'id', 'parent_id', 'submission_id', 'subreddit_name_prefixed', 'body',
                'ups', 'downs', 'score', 'controversiality', 'category', 'sentiment_score', 'sentiment_magnitude',
                'created', 'date_created', 'time_created'
        )


        # Add new columns to 'DF'.
        self.DF = self.DF.reindex(columns= columns)


        return self



    @staticmethod
    def generate_sentiment(text: str, verbose: bool):
        """
        Generates the sentiment analysis of a given corpus with the Google Cloud Natural Language API.
        :return:
        """

        # Define access to the Google Cloud Natural Language API.
        language_client = language.LanguageServiceClient()


        # Define the 'Document' object to be analyzed.
        document = language.types.Document(
            content=text,
            type=language.enums.Document.Type.PLAIN_TEXT
        )


        # Analyze & record the sentiment of the text
        sentiment = language_client.analyze_sentiment(document=document).document_sentiment


        # Store the sentiment analysis data as Numpy array.
        #   - Organization: ('Score', 'Magnitude')
        result = numpy.array((sentiment.score, sentiment.magnitude))


        # Output sentiment analysis if 'verbose' is true...
        if verbose:
            print(u'=' * 20)
            print('Sentiment: {}, {}'.format(result[0], result[1]))


        return result



    """ [Begin: 'Google, Inc.' Work] """

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

    @staticmethod
    def generate_category(text: str, verbose: bool):
        """Classify the input text into categories. """

        # Define dict to hold result of analysis.
        result = dict()


        # Define access to the Google Cloud Natural Language API.
        language_client = language.LanguageServiceClient()


        # Define the 'Document' object to be analyzed.
        document = language.types.Document(
            content= text,
            type= language.enums.Document.Type.PLAIN_TEXT
        )


        # Get the response.
        response = language_client.classify_text(document)


        # Get the categories.
        categories = response.categories


        # Organize the category(ies) in a dict.
        for category in categories:
            # Turn the categories into a dictionary of the form:
            # {category.name: category.confidence}, so that they can
            # be treated as a sparse vector.
            result[category.name] = category.confidence


        # Output analysis is 'verbose' is True.
        if verbose:

            for category in categories:

                print(u'=' * 20)
                # print('Text: {}'.format(text))
                print(u'{:<16}: {}'.format('category', category.name))
                print(u'{:<16}: {}'.format('confidence', category.confidence))


        return result



    @staticmethod
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

    """ {End: 'Google, Inc.' Work] """



    @staticmethod
    def init_google_lang_api():
        """
        Initiates and authenticates access to the Google Natural Language API.
        :return:
        """

        # Define access to the Google Cloud Natural Language API.
        language_client = language.LanguageServiceClient()


        return language_client



    def define_categories(self, which: str):
        """
        Iterates the meta-DataFrame 'DF' and generates text general category classification.
            - Drops rows in DF that cannot be analyzed by the API.
        Moreover, records the amount of time the process took to complete.

        :param which:
        :return:
        """

        # Initiate the timer.
        clock_start = time.time()


        if which == 'base':

            # Initiate the Google Natural Language API.
            language_client = self.init_google_lang_api()


            # Output status.
            print('Defining categories...')
            print('\tDropped indexes:')

            # Iterate 'DF' to generate the category analysis with the Google Cloud API.
            #   - Note: 'row' necessary for functional iteration (12/24/17).
            for index, row in self.DF.iterrows():

                try:

                    # Get the body text for classification.
                    text = self.DF.loc[index, 'body']


                    # Define the 'Document' object to be analyzed.
                    document = language.types.Document(
                        content=text,
                        type=language.enums.Document.Type.PLAIN_TEXT
                    )


                    # Generate the classification analysis.
                    category_analysis = language_client.classify_text(document)


                    # Record the identified Categories.
                    categories = category_analysis.categories


                    # Define a dict to hold the Categories identified.
                    result = dict()


                    # Organize the category(ies) in a dict.
                    for category in categories:
                        # Turn the categories into a dictionary of the form:
                        # {category.name: category.confidence}, so that they can
                        # be treated as a sparse vector.
                        result[category.name] = category.confidence


                    # Run classify() to get 'Category' analysis.
                    # classification = self.generate_category(text, verbose=False)


                    # Split the identified categories.
                    split_classification = self.split_labels(result)


                    # Get firstly identified category.
                    #   - This firstly identified category is the one with the most confidence.
                    first_category = next(iter(split_classification))


                    # Add category to dataframe.
                    self.DF.loc[index, 'category'] = first_category

                # Catch 'InvalidArgument' errors caused by arguments of insufficient length or 'StopIteration'.
                except (google.api_core.exceptions.InvalidArgument, StopIteration):

                    # Drop the index of the argument that raised the exception.
                    self.DF.drop(index, inplace=True)


                    # Output status.
                    print('\t\t', index)


                    # Continue loop.
                    continue


        # End the timer.
        clock_end = time.time()


        # Output status.
        print('Finished in: ' + str(clock_end - clock_start) + ' seconds.\n')


        return self



    # TODO: Fix. Not updated for use of a single access to the Google Natural Language API.
    def define_sentiment(self, which: str):
        """
        Iterates the meta-DataFrame 'DF' and generates text general category classification and sentiment analysis.
            - Drops rows in DF that cannot be analyzed by the API.

        :param which:
        :return:
        """

        # Initiate timer.
        clock_start = time.time()


        if which == 'base':

            # Output status.
            print('Defining sentiment...')
            print('\tDropped indexes:')

            # Iterate 'DF' to generate the sentiment analysis with the Google Cloud API.
            #   - Note: 'row' necessary for functional iteration (12/24/17).
            drop_count = 0
            for index, row in self.DF.iterrows():

                try:

                    # Define the corpus.
                    text = self.DF.loc[index, 'body']


                    # Generate and record the sentiment analysis.
                    sentiment_analysis = self.generate_sentiment(text= text, verbose= False)


                    # Append sentiment score 'DF'.
                    self.DF.loc[index, 'sentiment_score'] = sentiment_analysis[0]


                    # Append sentiment magnitude to 'DF'.
                    self.DF.loc[index, 'sentiment_magnitude'] = sentiment_analysis[1]

                # Catch 'InvalidArgument' errors.
                except google.api_core.exceptions.InvalidArgument:

                    # Drop the index of the argument that raised the exception.
                    self.DF.drop(index, inplace=True)


                    # Increment row-drop counter.
                    drop_count += 1


                    # Output status.
                    print('\t\t', index)


                    # Continue loop.
                    continue


            # If no indexes were dropped, output status.
            if drop_count == 0:
                print('\t\tNone')


        # End timer.
        clock_end = time.time()


        # Output status.
        print('Finished in: ' + str(clock_end - clock_start) + ' seconds.\n')


        return self



    # TODO: Substantial optimization required.
    def process_dataframe(self, which: str):
        """
        Processes the entire base DataFrame: 'DF'. Using the Google Natural Language API, 'process_dataframe' generates
        Category classification and Sentiment analysis for each value of the 'body' Series and appends it to 'DF'
        inplace. Moreover, the algorithm run-time is recorded and displayed upon completion.

        :return:
        """

        # Initiate the timer.
        clock_start = time.time()


        # Define constants.
        INITIAL_DF_SIZE = 24062
        FINAL_DF_SIZE = 0
        DROP_COUNT = 0


        if which == 'base':

            # Initiate the Google Natural Language API.
            language_client = self.init_google_lang_api()

            # Output status.
            print('Defining Categories and Sentiment for \'DF\'...')
            print('\tDropped indexes:')

            # Iterate 'DF' to generate the category analysis with the Google Cloud API.
            #   - Note: 'row' necessary for functional iteration (12/24/17).
            for index, row in self.DF.iterrows():

                try:

                    # Get the body text for classification.
                    text = self.DF.loc[index, 'body']


                    # Define the 'Document' object to be analyzed.
                    document = language.types.Document(
                        content=text,
                        type=language.enums.Document.Type.PLAIN_TEXT
                    )


                    """ Define Categories for 'DF' """

                    # Generate the classification analysis.
                    category_analysis = language_client.classify_text(document)


                    # Record the identified Categories.
                    categories = category_analysis.categories


                    # Define a dict to hold the Categories identified.
                    result = dict()


                    # Organize the category(ies) in a dict.
                    for category in categories:
                        # Turn the categories into a dictionary of the form:
                        # {category.name: category.confidence}, so that they can
                        # be treated as a sparse vector.
                        result[category.name] = category.confidence


                    # Split the identified categories.
                    split_classification = self.split_labels(result)


                    # Get firstly identified category.
                    #   - This firstly identified category is the one with the most confidence.
                    first_category = next(iter(split_classification))


                    # Add category to dataframe.
                    self.DF.loc[index, 'category'] = first_category


                    """ Define Sentiment for 'DF' """

                    # Analyze & record the sentiment of the text
                    sentiment = language_client.analyze_sentiment(document=document).document_sentiment


                    # Store the sentiment analysis data as Numpy array.
                    #   - Organization: ('Score', 'Magnitude')
                    sentiment_analysis = numpy.array((sentiment.score, sentiment.magnitude))


                    # Append sentiment score 'DF'.
                    self.DF.loc[index, 'sentiment_score'] = sentiment_analysis[0]


                    # Append sentiment magnitude to 'DF'.
                    self.DF.loc[index, 'sentiment_magnitude'] = sentiment_analysis[1]

                # Catch 'InvalidArgument' errors caused by arguments of insufficient length or 'StopIteration'.
                except (google.api_core.exceptions.InvalidArgument, StopIteration):

                    # Increment 'DROP_COUNT' to record new row-drop.
                    DROP_COUNT += 1

                    # Drop the index of the argument that raised the exception.
                    self.DF.drop(index, inplace=True)


                    # Output status.
                    print('\t\t', index)


                    # Continue loop.
                    continue


        # End the timer.
        clock_end = time.time()


        # Output status.
        print('Finished in: ' + str(clock_end - clock_start) + ' seconds.\n')


        # Output status.
        print('Finished.\n')


        return self

    # [End Class: DataProcessor] #





def main():
    """

    :return:
    """


    dp = DataProcessor().prepare_dataframe()


    df = dp.DF


    # dp.process_dataframe(which= 'base').organize_dataframe(action='reindex')


    # dp.view_dataframe()




    return 0






main()
