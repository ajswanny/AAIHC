import pprint
import praw


reddit = praw.Reddit(user_agent='Comment Extraction Test',
                     client_id='hpTnFWPodmP85w',
                     client_secret='T2rZgWYrmqB_ULSOmIVZVn2ff8Q')

subreddit = reddit.subreddit('redditdev')





submission = reddit.submission(id='3g1jfi')


submission.comments.replace_more(limit=0)
file = open('/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Scratchwork/praw_workspace/praw_comments.txt', 'w')

for comment in submission.comments:
    print((str(comment)))
    file.write(comment.body)
    file.write('//&//')
    file.write('\n')


print(file)

file.close()



# for top_level_comment in submission.comments:
#     print(top_level_comment.body)

# for top_level_comment in submission.comments:
#     for second_level_comments in top_level_comment.replies:
#         print(second_level_comments.body)


# submission.comments.replace_more(limit=0)
# comment_queue = submission.comments[:] # Seed with top-level
# while comment_queue:
#     comment = comment_queue.pop(0)
#     print(comment.body)
#     comment_queue.extend(comment.replies)




"""
reddit = praw.Reddit(client_id='hpTnFWPodmP85w',
                     client_secret='T2rZgWYrmqB_ULSOmIVZVn2ff8Q',
                     user_agent='testing')


print(reddit.read_only)

# for submission in reddit.subreddit('learnpython').hot(limit=10):
#     print(submission.title)

subreddit = reddit.subreddit('redditdev')

# print(subreddit.display_name)
# print(subreddit.title)
# print(subreddit.description)

# for submission in subreddit.hot(limit=10):
#     print(submission.title)
#     print(submission.score)
#     print(submission.id)
#     print(submission.url)
#     print("\n")

# submission = reddit.submission(id='39zje0')
# all_comments = submission.comments.list()
# print(all_comments[0])


submission = reddit.submission(id='39zje0')
print(submission.title)
pprint.pprint(vars(submission))
"""
