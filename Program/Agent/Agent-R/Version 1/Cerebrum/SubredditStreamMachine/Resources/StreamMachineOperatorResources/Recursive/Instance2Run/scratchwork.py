from SubredditStreamMachine.subreddit_stream_machine_h import SubredditStreamMachine
import pandas
import indicoio

# df: pandas.DataFrame = pandas.read_json("/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/Agent/Agent-R/Version 1/Cerebrum/SubredditStreamMachine/Resources/StreamMachineOperatorResources/Recursive/Instance1Run/(Op_RECURSIVE_1)_main_df.json")
#
#
# df = df.truncate(after= 0)
#
# print(df.head().to_string())
#
# df.to_json("/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/Agent/Agent-R/Version 1/Cerebrum/SubredditStreamMachine/Resources/StreamMachineOperatorResources/Recursive/Instance2Run/scratchwork.json")


# dfx = pandas.read_json("/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Program/Agent/Agent-R/Version 1/Cerebrum/SubredditStreamMachine/Resources/StreamMachineOperatorResources/Recursive/Instance2Run/TEMP(Op_RECURSIVE_1)_main_df.json")
#
# print(dfx.head().to_string())


indicoio.config.api_key = "7dc1f325509757ba2e76e411beef646f"

print(indicoio.relevance("https://www.washingtonpost.com/national/if-anyone-can-hear-us--help-puerto-ricos-mayors-describe-widespread-devastation-from-hurricane-maria/2017/09/23/7ef5f6c4-a069-11e7-8ea1-ed975285475e_story.html?utm_term=.2cbe5dcd3e54",
                         "Humanitarian Crisis in Puerto Rico"))