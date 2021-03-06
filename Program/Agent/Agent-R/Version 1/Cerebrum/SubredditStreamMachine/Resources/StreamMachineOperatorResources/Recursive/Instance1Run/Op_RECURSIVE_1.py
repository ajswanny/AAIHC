from SubredditStreamMachine.subreddit_stream_machine_operator_h import SubredditStreamMachineOperator


def R01():
    """
        Recursive!
        Operating with Reddit Account 1
        Using utterance 1
        Operating within Subreddit: r/news

    """

    reddit_parameters_2 = (
        "zO1z52xZNtdxrA",
        "VbAzyOfUcj-94a71j8V_6lUTyAM",
        "An observer of Subreddit Streams",
        "ssa1G",
        "subreddit.stream.agent.1.password"
    )

    OR1 = SubredditStreamMachineOperator(
        instance_num= 2,
        instance_id="(2-7-18_12-45)_R1",
        operate_recursively= True,
        FP_aggregate_archive_override= "/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/Agent/Agent-R/Version 1/Cerebrum/SubredditStreamMachine/Resources/StreamMachineOperatorResources/Recursive/Instance1Run/(Op_RECURSIVE_1)_main_df.json",
        reddit_api_parameters=reddit_parameters_2,
        ssm__platform= "Reddit",
        ssmp__utterance_content= "It's super concerning to see all thats happening in the world.. Earthquakes in Asia, diseases in Africa, even within the US, Puerto Ricans still living without electricity. And now this....",
        ssmp__keyboard_interrupt_save_file="Resources/StreamProcessDependencies/StreamProcessSubmData/kbd_interrupt_backup.json",
        ssmp__engage= True,
        ssmp__work_subreddit= "news",
        ssmp__relevance_clearance_threshold=0.5
    )

R01()