from SubredditStreamMachine.subreddit_stream_machine_h import SubredditStreamMachine
from SubredditStreamMachine.subreddit_stream_machine_operator_h import SubredditStreamMachineOperator

def initiate_O1():

    reddit_parameters_1 = (
        "YKsn6_Q_yaP46A",
         "eygwAD8rMNEhFet0vLQmBqVPxbE",
         "default_for_research",
         "agent000001",
         "S0awesome"
    )

    O1 = SubredditStreamMachineOperator(
        instance_num= 1,
        instance_id= "(2-6-18_12-21)_1",
        operate_recursively= False,
        reddit_api_parameters= reddit_parameters_1,
        ssm__platform= "Reddit",
        ssmp__utterance_content= "It's super concerning to see all thats happening in the world.. Earthquakes in Asia, diseases in Africa, even within the US, Puerto Ricans still living without electricity. And now this....",
        ssmp__keyboard_interrupt_save_file= "Resources/StreamProcessDependencies/StreamProcessSubmData/kbd_interrupt_backup.json",
        ssmp__engage= True,
        ssmp__work_subreddit= "politics",
        ssmp__relevance_clearance_threshold= 0.5
    )


def initiate_O2():

    reddit_parameters_2 = (
        "zO1z52xZNtdxrA",
         "VbAzyOfUcj-94a71j8V_6lUTyAM",
         "An observer of Subreddit Streams",
         "ssa1G",
         "subreddit.stream.agent.1.password"
    )

    O2 = SubredditStreamMachineOperator(
        instance_num= 2,
        instance_id= "(2-6-18_20-25)_2",
        operate_recursively= False,
        reddit_api_parameters= reddit_parameters_2,
        ssm__platform= "Reddit",
        ssmp__utterance_content= "It's super concerning to see all thats happening in the world.. Earthquakes in Asia, diseases in Africa, even within the US, Puerto Ricans still living without electricity. And now this....",
        ssmp__keyboard_interrupt_save_file= "Resources/StreamProcessDependencies/StreamProcessSubmData/kbd_interrupt_backup.json",
        ssmp__engage= True,
        ssmp__work_subreddit= "politics",
        ssmp__relevance_clearance_threshold= 0.5
    )


def initiate_R01():
    """ Recursive version. """

    reddit_parameters_2 = (
        "zO1z52xZNtdxrA",
        "VbAzyOfUcj-94a71j8V_6lUTyAM",
        "An observer of Subreddit Streams",
        "ssa1G",
        "subreddit.stream.agent.1.password"
    )

    OR1 = SubredditStreamMachineOperator(
        instance_num= 2,
        instance_id="(2-7-18_10-11)_R1",
        operate_recursively= True,
        FP_aggregate_archive_override= "",
        reddit_api_parameters=reddit_parameters_2,
        ssm__platform="Reddit",
        ssmp__utterance_content="It's super concerning to see all thats happening in the world.. Earthquakes in Asia, diseases in Africa, even within the US, Puerto Ricans still living without electricity. And now this....",
        ssmp__keyboard_interrupt_save_file="Resources/StreamProcessDependencies/StreamProcessSubmData/kbd_interrupt_backup.json",
        ssmp__engage=True,
        ssmp__work_subreddit="politics",
        ssmp__relevance_clearance_threshold=0.5
    )


initiate_O2()