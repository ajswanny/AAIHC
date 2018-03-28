from SubredditStreamMachine.subreddit_stream_machine_h import SubredditStreamMachine


class SubredditStreamMachineOperator:
    """
    A meta-Class for Stream Machine operation.

    ssm: Subreddit Stream Machine
    ssmp: Subreddit Stream Machine Stream Process

    """

    def __init__(
            self,
            instance_num: int,
            instance_id: str,
            operate_recursively: bool,
            FP_aggregate_archive_override: str,
            reddit_api_parameters: tuple,
            ssm__platform: str,
            ssmp__utterance_content: str,
            ssmp__keyboard_interrupt_save_file: str,
            ssmp__engage: bool,
            ssmp__work_subreddit: str,
            ssmp__relevance_clearance_threshold: float,
            problem_topic: str,
            **kwargs
    ):
        """

        """

        # Define the instance ID.
        self.instance_id = instance_id


        # Output instance details.
        print("Beginning Subreddit Stream Machine Operator | ID: ", instance_id)

        # Output process status.
        print("Entering process...")
        print("*" * 50)


        if "indicoio_api_key" in kwargs:

            # Create Subreddit Stream Machine.
            SSM = SubredditStreamMachine(
                operate_recursively=operate_recursively,
                instance_num=instance_num,
                instance_id=instance_id,
                platform= ssm__platform,
                reddit_params= reddit_api_parameters,
                problem_topic= problem_topic,
                indicoio_api_key= kwargs["indicoio_api_key"]
            )

        else:

            # Create Subreddit Stream Machine.
            SSM = SubredditStreamMachine(
                operate_recursively= operate_recursively,
                instance_num= instance_num,
                instance_id= instance_id,
                platform= ssm__platform,
                reddit_params= reddit_api_parameters,
                problem_topic= problem_topic
            )


        if operate_recursively:

            # Initiate the Submission Stream process.
            SSM.__recursive_stream_process__(
                utterance_content= ssmp__utterance_content,
                keyboard_interrupt_save_file= ssmp__keyboard_interrupt_save_file,
                FP_aggregate_archive_override= FP_aggregate_archive_override,
                engage= ssmp__engage,
                work_subreddit= ssmp__work_subreddit,
                relevance_clearance_threshold= ssmp__relevance_clearance_threshold
            )

        else:

            # Initiate the Submission Stream process.
            SSM.__stream_process__(
                utterance_content= ssmp__utterance_content,
                keyboard_interrupt_save_file= ssmp__keyboard_interrupt_save_file,
                engage= ssmp__engage,
                work_subreddit= ssmp__work_subreddit,
                relevance_clearance_threshold= ssmp__relevance_clearance_threshold
            )


        # Output process status.
        print("*" * 50)
        print("Process complete for SSM Operator ", instance_id)
