from Cerebrum.machine_lobe.machine_lobe_h import MachineLobe


reddit_parameters = ("YKsn6_Q_yaP46A",
                     "eygwAD8rMNEhFet0vLQmBqVPxbE",
                     "default_for_research",
                     "agent000001",
                     "S0awesome")


machine = MachineLobe(platform= "Reddit", reddit_params= reddit_parameters)


# x = machine.start(return_submissions= True)
#
#
# print(x)


array = machine.__generate_title_vector__()




