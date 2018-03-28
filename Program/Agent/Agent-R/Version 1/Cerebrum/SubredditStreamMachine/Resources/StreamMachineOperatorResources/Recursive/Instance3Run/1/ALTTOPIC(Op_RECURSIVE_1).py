from SubredditStreamMachine.subreddit_stream_machine_operator_h import SubredditStreamMachineOperator



def ALTR01():
    """
        Recursive!
        Operating with Reddit Account 1
        Using utterance 1
        ALTR: Alternative Topic | Recursive
        Operating within Subreddit: r/news

    """

    reddit_parameters_1 = (
        "fkWcAvHpk9bYaw",
        "KCmNPZmD9MyLLspLJ2QuKk9sF4U",
        "research subreddit stream script",
        "ssata1",
        "subreddit.stream.alttopic.agent.1.password"
    )

    ALTOR1 = SubredditStreamMachineOperator(
        instance_num= 0,
        instance_id="(3-27-18_10-11)_ALTR1",
        operate_recursively= True,
        FP_aggregate_archive_override= "/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/Agent/Agent-R/Version 1/Cerebrum/SubredditStreamMachine/Resources/StreamMachineOperatorResources/Recursive/Instance3Run/1/ALTTOPIC(Op_RECURSIVE_1)_main_df.json",
        reddit_api_parameters= reddit_parameters_1,
        ssm__platform= "Reddit",
        ssmp__utterance_content= "Have you guys heard about the news with Roseanne? What are your thoughts?",
        ssmp__keyboard_interrupt_save_file= "Resources/StreamProcessDependencies/StreamProcessSubmData/kbd_interrupt_backup.json",
        ssmp__engage= True,
        ssmp__work_subreddit= "news",
        ssmp__relevance_clearance_threshold= 0.6,
        problem_topic= "Television Show Roseanne",
        indicoio_api_key= "7dc1f325509757ba2e76e411beef646f"
    )

ALTR01()