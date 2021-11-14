import praw

reddit = praw.Reddit(
    client_id="KI3xrA2NAM7JmwoSq5pTUg",
    client_secret="mbnSdxDFvmzNmUUZzxflyFgktzkX7Q",
    user_agent="pythonpraw",
)

def get_subreddit():
    submissions = reddit.subreddit('all').new()
    post_to_pick = 2
    links = []
    for i in range(0, post_to_pick):
    		submission = next(x for x in submissions if not x.stickied)
    		links.append('https://www.reddit.com/r/' + str(submission.subreddit) + '/top/?t=all')
    return links
