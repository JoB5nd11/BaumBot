import praw
import random
import discord
import youtube_dl

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

class MusicClient:
    def __init__(self):
        self.ydl_opts = ydl_opts = {
        	'format': 'bestaudio/best',
        	'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        	'restrictfilenames': True,
        	'noplaylist': True,
        	'nocheckcertificate': True,
        	'ignoreerrors': False,
        	'logtostderr': False,
        	'quiet': True,
        	'no_warnings': True,
        	'default_search': 'auto',
        	'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
        }
        self.youtube = youtube_dl.YoutubeDL(ydl_opts)

    def play(self, voice_channel, url):
        #Differenciate between youtube and spotify
        if voice_channel.is_paused:
            voice_channel.resume()
            voice_channel.stop()
        elif voice_channel.is_playing:
            voice_channel.stop()
            #What about the queue

        with self.youtube as ydl:
            info = ydl.extract_info(url, download=False)
            get_url = info['url']
            voice_channel.play(discord.FFmpegPCMAudio(get_url))

            return info['title']

    def pause(self, voice_channel):
        if voice_channel.is_playing:
            voice_channel.pause() #Check things
        #not pausable mesage?

    def resume(self, voice_channel):
        if voice_channel.is_paused:
            voice_channel.resume()
        #not resumable message

    def stop(self, voice_channel):
        if voice_channel.is_playing:
            voice_channel.stop() #What about the queue
        #not stoppabel

class RandomClient:
    def __init__(self):
        pass

    def get_random_number(self, lower, higher):
        if higher <= lower:
            higher = lower + 1
        answer = "{}".format(random.randint(lower, higher))
        return answer

class PornClient:
    def __init__(self):
        pass

class StockClient:
    def __init__(self):
        pass
