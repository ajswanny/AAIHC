from Cerebrum.machine_lobe.machine_lobe_h import MachineLobe
from pprint import pprint


# Define the credentials for the Reddit object.
reddit_parameters = ("YKsn6_Q_yaP46A",
                     "eygwAD8rMNEhFet0vLQmBqVPxbE",
                     "default_for_research",
                     "agent000001",
                     "S0awesome")


# Define the MachineLobe with the desired Reddit credentials.
machine = MachineLobe(platform= "Reddit", reddit_params= reddit_parameters)


# Initialize the process.
machine.start(override= True)





import pandas


x = pandas.DataFrame(machine.keyword_analyses)


print(x.head().to_string())








