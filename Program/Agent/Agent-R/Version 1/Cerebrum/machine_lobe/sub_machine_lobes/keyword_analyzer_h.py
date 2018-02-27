"""
Agent: Cerebrum::MachineLobe:: keyword_analyzer_h.py
Copyright (c) 2018, Alexander Joseph Swanson Villares
"""


import machine_lobe_h
import praw



class KeywordProcessingMachine():


    def __init__(self, reddit_instance: praw.Reddit, **kwargs):
        """
        Creates an instance of 'KeywordProcessingMachine' used to generate keywords analysis for a collection
        of Reddit Submissions.

        """

        # Define the Reddit instance.
        self.reddit_instance = reddit_instance


        # Define default working Subreddit if provided in object instantiation.
        if "subreddit" in kwargs:

            self.default_subreddit = self.reddit_instance.subreddit(display_name=kwargs["subreddit"])

        else:

            self.default_subreddit = self.reddit_instance.subreddit("news")

