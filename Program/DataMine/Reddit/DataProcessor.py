from Reddit import DataObserver

# Import SciKit Learn machine learning modules.
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import MultinomialNB
from matplotlib import pyplot as plt

from sklearn.model_selection import learning_curve

import numpy


df = DataObserver.major_df
df = df.loc[df['sentiment_score'] != 0]

# df = df.loc[df["category"] == ""]
# df = df.loc[df["sentiment_score"]]


# Set X and y.
dataframe_X = df["body"]
dataframe_y = df["sentiment_score"]

# Create feature vectors with a Term Frequency...
# Parameters borrowed from @bonzanini
vectorizer = TfidfVectorizer(min_df= 5,                 # Minimum frequency.
                             max_df = 0.8,              # Maximum frequency.
                             lowercase= True,
                             strip_accents= 'unicode',
                             stop_words= 'english',     # 'Are', 'you', etc.
                             sublinear_tf= True,
                             use_idf= True
                             )


# Split train and test data.
x_train, x_test, y_train, y_test = train_test_split(dataframe_X, dataframe_y, test_size=0.2, random_state=4)


# Convert y axis data to integers.
y_train = y_train.astype('int')
y_test = y_test.astype('int')
y_test_array = numpy.array(y_test)


# Vectorize the training and testing x axis.
train_vectors_X = vectorizer.fit_transform(x_train)
test_vectors_X = vectorizer.transform(x_test)


# Apply Naive Bayes...
Multinomial_NB = MultinomialNB()
Multinomial_NB.fit(train_vectors_X, y_train)


# Assess
assessment = Multinomial_NB.predict(test_vectors_X)
assessment_array = numpy.array(assessment)


# Identify accuracy.
n = 0
for i in range(len(assessment)):

    if assessment[i] == y_test_array[i]:
        n += 1


# Percentage accuracy.
# accuracy = n / len(assessment)

# print("Accuracy: ", accuracy)

# Credit to: Sci-Kit Learn Staff
def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None,
                        n_jobs=1, train_sizes=numpy.linspace(.1, 1.0, 5)):
    """
    Generate a simple plot of the test and training learning curve.

    Parameters
    ----------
    estimator : object type that implements the "fit" and "predict" methods
        An object of that type which is cloned for each validation.

    title : string
        Title for the chart.

    X : array-like, shape (n_samples, n_features)
        Training vector, where n_samples is the number of samples and
        n_features is the number of features.

    y : array-like, shape (n_samples) or (n_samples, n_features), optional
        Target relative to X for classification or regression;
        None for unsupervised learning.

    ylim : tuple, shape (ymin, ymax), optional
        Defines minimum and maximum yvalues plotted.

    cv : int, cross-validation generator or an iterable, optional
        Determines the cross-validation splitting strategy.
        Possible inputs for cv are:
          - None, to use the default 3-fold cross-validation,
          - integer, to specify the number of folds.
          - An object to be used as a cross-validation generator.
          - An iterable yielding train/test splits.

        For integer/None inputs, if ``y`` is binary or multiclass,
        :class:`StratifiedKFold` used. If the estimator is not a classifier
        or if ``y`` is neither binary nor multiclass, :class:`KFold` is used.

        Refer :ref:`User Guide <cross_validation>` for the various
        cross-validators that can be used here.

    n_jobs : integer, optional
        Number of jobs to run in parallel (default 1).
    """
    plt.figure()
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
    train_scores_mean = numpy.mean(train_scores, axis=1)
    train_scores_std = numpy.std(train_scores, axis=1)
    test_scores_mean = numpy.mean(test_scores, axis=1)
    test_scores_std = numpy.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.legend(loc="best")
    return plt


plt = plot_learning_curve(Multinomial_NB, "Multinomial Naive Bayes TF-IDF", train_vectors_X, y_train)
plt.show()
