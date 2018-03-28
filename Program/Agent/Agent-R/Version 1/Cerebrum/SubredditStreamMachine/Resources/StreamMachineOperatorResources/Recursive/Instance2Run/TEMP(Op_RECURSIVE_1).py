from SubredditStreamMachine.subreddit_stream_machine_operator_h import SubredditStreamMachineOperator


def RT01():
    """
        Recursive!
        Operating with Reddit Account 2
        Using utterance 3
        Operating within Subreddit: r/news

    """

    reddit_parameters_2 = (
        "zO1z52xZNtdxrA",
        "VbAzyOfUcj-94a71j8V_6lUTyAM",
        "An observer of Subreddit Streams",
        "ssa1G",
        "subreddit.stream.agent.1.password"
    )

    OR2 = SubredditStreamMachineOperator(
        instance_num= 0,
        instance_id="(3-17-18_19-37)_RT1",
        operate_recursively= True,
        FP_aggregate_archive_override= "/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/Agent/Agent-R/Version 1/Cerebrum/SubredditStreamMachine/Resources/StreamMachineOperatorResources/Recursive/Instance2Run/TEMP(Op_RECURSIVE_1)_main_df.json",
        reddit_api_parameters=reddit_parameters_2,
        ssm__platform= "Reddit",
        ssmp__utterance_content= "It's super concerning to see all thats happening in the world.. Earthquakes in Asia, diseases in Africa, even within the US, Puerto Ricans still living without electricity. And now this.. What can be done?",
        ssmp__keyboard_interrupt_save_file= "Resources/StreamProcessDependencies/StreamProcessSubmData/kbd_interrupt_backup.json",
        ssmp__engage= True,
        ssmp__work_subreddit= "news",
        ssmp__relevance_clearance_threshold= 0.5,
        indicoio_api_key= "7dc1f325509757ba2e76e411beef646f"
    )

RT01()