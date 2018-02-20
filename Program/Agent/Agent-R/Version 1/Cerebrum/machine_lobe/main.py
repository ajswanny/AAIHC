from Cerebrum.machine_lobe.machine_lobe_h import MachineLobe
from pprint import pprint
import pandas
import json

def process():


    # Define the credentials for the Reddit object.
    reddit_parameters = ("YKsn6_Q_yaP46A",
                         "eygwAD8rMNEhFet0vLQmBqVPxbE",
                         "default_for_research",
                         "agent000001",
                         "S0awesome")


    # Define the MachineLobe with the desired Reddit credentials.
    machine = MachineLobe(
        platform= "Reddit",
        reddit_params= reddit_parameters,
        analyize_subm_links= False,
        main_df_archive_filepath= "Resources/_main_kwd_df/_r-politics_/2018-02-20_17-20/_main_kwd_df.json"
    )


    # Initialize the process.
    machine.start(override= True, work_subreddit= 'news', engage= True, subm_fetch_limit= None,
                  analyze_subm_articles= True, intersection_min_divider= 3)

    print(machine._main_kwd_df.to_string())


def get_datetime():

    from datetime import datetime

    x = str(datetime.now())

    print(x)



def main():

    # with open("Resources/_main_kwd_df/_r-worldnews_/2018-02-18_00-40/_main_kwd_df.json", "r") as fp:
    #
    #     x = json.load(fp)

    # r news 1:
    #   Resources/_main_kwd_df/_r-news_/2018-02-17_20-54/_main_kwd_df.json

    # r worldnews 1:
    #   Resources/_main_kwd_df/_r-worldnews_/2018-02-18_00-40/_main_kwd_df.json

    x: pandas.DataFrame = pandas.read_json(path_or_buf= "Resources/_main_kwd_df/_r-news_/2018-02-20_16-38/_main_kwd_df.json")



    print((x.loc[x.intersection_size > 1]).to_string())

    # print(x.head().to_string())



def f(x):

    if x == 1: process()

    elif x == 2: main()

    elif x == 3: get_datetime()


f(2)


def read_rpolitics_example_one():


    x: pandas.DataFrame = pandas.read_json(path_or_buf= "Resources/_main_kwd_df/_r-politics_/2018-02-20_17-20/_main_kwd_df.json")

    print((x.loc[x.intersection_size > 1]).to_string())



# read_rpolitics_example_one()