from Cerebrum.machine_lobe.machine_lobe_h import MachineLobe
from pprint import pprint
import pandas



# Define the credentials for the Reddit object.
reddit_parameters = ("YKsn6_Q_yaP46A",
                     "eygwAD8rMNEhFet0vLQmBqVPxbE",
                     "default_for_research",
                     "agent000001",
                     "S0awesome")


# Define the MachineLobe with the desired Reddit credentials.
machine = MachineLobe(platform= "Reddit", reddit_params= reddit_parameters)


# Initialize the process.
machine.start(override= True, work_subreddit= 'news', engage= True, subm_fetch_limit= None, intersection_min_divider= 3)


print(machine._main_kwd_df.to_string())

# machine._main_kwd_df.to_json("/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/Agent/Agent-R/Version 1/Cerebrum/machine_lobe/Resources/Program_Data_Fields/_main_kwd_df.json")

# machine.__test_functionality__()

def get_datetime():

    from datetime import datetime

    x = str(datetime.now())

    print(x)