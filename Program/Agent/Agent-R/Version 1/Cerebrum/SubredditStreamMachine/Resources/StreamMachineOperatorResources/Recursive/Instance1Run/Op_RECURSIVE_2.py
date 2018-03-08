from SubredditStreamMachine.subreddit_stream_machine_operator_h import SubredditStreamMachineOperator


def R02():
    """
        Recursive!
        Operating with Reddit Account 1
        Using utterance 1
        Operating within Subreddit: r/worldnews

    """

    reddit_parameters_2 = (
        "zO1z52xZNtdxrA",
        "VbAzyOfUcj-94a71j8V_6lUTyAM",
        "An observer of Subreddit Streams",
        "ssa1G",
        "subreddit.stream.agent.1.password"
    )

    OR2 = SubredditStreamMachineOperator(
        instance_num= 2,
        instance_id="(2-7-18_12-45)_R2",
        operate_recursively= True,
        FP_aggregate_archive_override= "/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/Agent/Agent-R/Version 1/Cerebrum/SubredditStreamMachine/Resources/StreamMachineOperatorResources/Recursive/Instance1Run/(Op_RECURSIVE_2)_main_df.json",
        reddit_api_parameters=reddit_parameters_2,
        ssm__platform= "Reddit",
        ssmp__utterance_content= "It's super concerning to see all thats happening in the world.. Earthquakes in Asia, diseases in Africa, even within the US, Puerto Ricans still living without electricity. And now this....",
        ssmp__keyboard_interrupt_save_file="Resources/StreamProcessDependencies/StreamProcessSubmData/kbd_interrupt_backup.json",
        ssmp__engage= True,
        ssmp__work_subreddit= "worldnews",
        ssmp__relevance_clearance_threshold= 0.5
    )

R02()