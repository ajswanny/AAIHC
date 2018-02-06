import praw
from pprint import pprint


def main():



    reddit = praw.Reddit(client_id= "YKsn6_Q_yaP46A",
                         client_secret= "eygwAD8rMNEhFet0vLQmBqVPxbE",
                         user_agent= "default_for_research",
                         username= "agent000001",
                         password= "S0awesome")


    subreddit = reddit.subreddit('AskReddit')
    # for submission in subreddit.stream.submissions():
    #     print(submission.title)

    submission = reddit.submission(id='3g1jfi')

    pprint(vars(submission))





    return 0




if __name__ == "__main__":
    main()