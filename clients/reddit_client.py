import praw

class RedditClient:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id="KI3xrA2NAM7JmwoSq5pTUg",
            client_secret="mbnSdxDFvmzNmUUZzxflyFgktzkX7Q",
            user_agent="BaumBot",
            check_for_async=False #yeah fuck you
        )
        self.max_responses = 20

    def get_random_subreddit(self, NSFW="yes", count=1, sort='/top/?t=all'):
        count = self._check_max_count(count)
        subreddit = self.reddit.subreddit('all').new()

        result = ""
        for i in range(0, count):
            submission = self._get_nsfw_submission(subreddit, NSFW)
            print("Subreddit: " + str(submission.subreddit))
            result += '<https://www.reddit.com/r/' + str(submission.subreddit) + sort + '>\n'
        result = self._check_answer(result)
        return result

    def get_random_post(self, NSFW="yes", count=1, images="only", spoilers="no"):
        count = self._check_max_count(count)
        subreddit = self.reddit.subreddit('all').new()

        result = ""
        current_result = ""
        for i in range(0, count):
            submission = self._get_nsfw_submission(subreddit, NSFW)

            if images == "only":
                while True:
                    if "jpg" in submission.url or "png" in submission.url or "gif" in submission.url:
                        current_result = submission.url
                        break
                    else:
                        submission = self._get_nsfw_submission(subreddit, NSFW)
                        count -= 1
            elif images == "no":
                pass

            if spoilers == "no" and submission.spoiler:
                count -= 1
            else:
                print("Post: " + submission.url)
                result += submission.url + '\n'

        result = self._check_answer(result)
        return result

    def get_memes_of_the_day(self):
        subreddits = [
            "meme",
            "memes",
            "dankmemes"
        ]

        result = ""
        for subreddit in subreddits:
            print("loading image from: " + subreddit)
            sub = self.reddit.subreddit(subreddit).top(time_filter='day')
            submission = next(x for x in sub if not x.stickied)
            result += submission.url + '\n'

        result = self._check_answer(result)
        return result

    def _check_max_count(self, count):
        count = int(count)
        if count < 1:
            return 1
        if count > self.max_responses:
            return self.max_responses
        return count

    def _check_answer(self, text):
        if text == "" or text == None:
            self._restart_in_error_case()
            return "Error"
        return text

    def _restart_in_error_case(self):
        self.reddit = asyncpraw.Reddit(
            client_id="KI3xrA2NAM7JmwoSq5pTUg",
            client_secret="mbnSdxDFvmzNmUUZzxflyFgktzkX7Q",
            user_agent="BaumBot",
        )

    def _add_to_porn_subreddits(self, subreddit):
        subreddit = str(subreddit)
        file = open('documents/pornsubreddits.txt', 'r')
        lines = file.readlines()

        for line in lines:
            if line.split('\n')[0] == subreddit:
                return

        file.close()
        file = open('documents/pornsubreddits.txt', 'a')
        file.write(subreddit + '\n')
        file.close()
        print("New: ", subreddit)

    def _get_nsfw_submission(self, subreddit, NSFW):
        if NSFW == "only":
            submission = next(x for x in subreddit if not x.stickied and x.subreddit.over18)
        elif NSFW == "no":
            submission = next(x for x in subreddit if not x.stickied and not x.subreddit.over18)
        else:
            submission = next(x for x in subreddit if not x.stickied)
        return submission
