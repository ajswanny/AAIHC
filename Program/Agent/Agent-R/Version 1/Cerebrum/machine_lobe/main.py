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
machine.start(override= True, work_subreddit= 'news', engage= True)

print(machine.__main_kwd_df__.loc[0])
print("\n\n\n", machine.__main_kwd_df__)

machine.__main_kwd_df__.to_json("/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/Agent/Agent-R/Version 1/Cerebrum/machine_lobe/Resources/Program_Data_Fields/__main_kwd_df__.json")

# machine.__test_functionality__()


