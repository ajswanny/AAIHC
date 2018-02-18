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
        main_df_archive_filepath= "Resources/_main_kwd_df/_r-worldnews_/2018-02-18_00-40/_main_kwd_df.json"
    )


    # Initialize the process.
    machine.start(override= True, work_subreddit= 'worldnews', engage= False, subm_fetch_limit= None,
                  analyze_subm_articles= False, intersection_min_divider= 3)

    print(machine._main_kwd_df.to_string())


def get_datetime():

    from datetime import datetime

    x = str(datetime.now())

    print(x)



def main():

    # with open("Resources/_main_kwd_df/_r-worldnews_/2018-02-18_00-40/_main_kwd_df.json", "r") as fp:
    #
    #     x = json.load(fp)

    x = pandas.read_json(path_or_buf= "Resources/_main_kwd_df/_r-worldnews_/2018-02-18_00-40/_main_kwd_df.json")

    print(x.head().to_string())

# process()

main()

# get_datetime()