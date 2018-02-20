import praw

# Define the credentials for the Reddit object.
reddit_params = ("sEX2amErEijiBg",
                     "BwKc0gvABKvEIR2kGAtHEjM0YN8",
                     "default_for_research",
                     "agent000001",
                     "S0awesome")


r = praw.Reddit(
            client_id= reddit_params[0],
            client_secret= reddit_params[1],
            user_agent= reddit_params[2],
            username= reddit_params[3],
            password= reddit_params[4]
        )


s = r.subreddit("news")


for submission in s.hot(limit= 1):

    print(submission.title)
    print(submission.url)

