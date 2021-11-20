import os
import praw
import random
import discord
import sqlite3
import youtube_dl
import pandas as pd
from PIL import Image, ImageDraw, ImageFilter

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

    #TODO wrong link -> Marek!
    #TODO adult warning! -> nice cock!

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
        #not stoppable

class RandomClient:
    def __init__(self):
        pass

    def get_random_number(self, lower, higher):
        higher = int(higher)
        lower = int(lower)
        if higher <= lower:
            higher = lower + 1
        return str(random.randint(int(lower), int(higher)))



class TicTacToeClient:
    def __init__(self):
        self.clear_board()
        self.coordinates = [[0, 0], [100, 0], [200, 0], [0, 100], [100, 100], [200, 100], [0, 200], [100, 200], [200, 200]]
        self.current_pos_string = '---------'
        self.board_image = Image.open(str(os.getcwd()) + '\\games\\tictactoe\\assets\\board.png')
        self.current_board_image = Image.open(str(os.getcwd()) + '\\games\\tictactoe\\gamefiles\\currentboard.png')
        self.x_image = Image.open(str(os.getcwd()) + '\\games\\tictactoe\\assets\\cross.png')
        self.o_image = Image.open(str(os.getcwd()) + '\\games\\tictactoe\\assets\\circle.png')

    def get_board(self, pos_string='', error=False, occupied=False): #TODO dont redraw
        if len(pos_string) > 9 or error:
            with open(str(os.getcwd()) + '\\games\\tictactoe\\assets\\error.png', "rb") as f:
                file = discord.File(f, filename=str(os.getcwd()) + '\\games\\tictactoe\\assets\\error.png')
            return file
        elif occupied:
            with open(str(os.getcwd()) + '\\games\\tictactoe\\assets\\occupied.png', "rb") as f:
                file = discord.File(f, filename=str(os.getcwd()) + '\\games\\tictactoe\\assets\\occupied.png')
            return file

        self._make_board(pos_string)

        file_name = str(os.getcwd()) + '\\games\\tictactoe\\gamefiles\\currentboard.png'
        with open(file_name, "rb") as f:
            file = discord.File(f, filename=file_name)
        return file

    def clear_board(self):
        self.current_board_image = Image.open(str(os.getcwd()) + '\\games\\tictactoe\\assets\\board.png')
        self.current_board_image.save(str(os.getcwd()) + '\\games\\tictactoe\\gamefiles\\currentboard.png')
        self.current_pos_string = '---------'
        return self.get_board()

    def move(self, position):
        position = [char for char in position]
        if len(position) > 2:
            print("TTT Move has more than 2 characters")
            return self.get_board(error=True)

        try:
            field_nr = int(position[1]) - 1
            if field_nr < 0 or field_nr > 8:
                print("TTT field_nr is smaller than 0 or bigger than 8")
                return self.get_board(error=True)
        except:
            print("TTT could not determine field_nr")
            return self.get_board(error=True)

        if self.current_pos_string[field_nr] != '-':
            return self.get_board(occupied=True)

        if position[0] == 'x':
            self._put_symbol_in_current_pos_string('x', field_nr)
        elif position[0] == 'o':
            self._put_symbol_in_current_pos_string('o', field_nr)
        else:
            print("TTT symbol was neither x nor o")
            return self.get_board(error=True)

        return self.get_board(self.current_pos_string)

    def game_over(self):
        pass #TODO

    def _make_board(self, pos_string):
        if(len(pos_string) == 9):
            self.current_board_image = Image.open(str(os.getcwd()) + '\\games\\tictactoe\\assets\\board.png')
            self.current_board_image.save(str(os.getcwd()) + '\\games\\tictactoe\\gamefiles\\currentboard.png')
            for i, pos in enumerate(pos_string):
                if pos == 'x':
                    self.current_board_image.paste(self.x_image, (self.coordinates[i][0], self.coordinates[i][1]), self.x_image)
                    self.current_board_image.save(str(os.getcwd()) + '\\games\\tictactoe\\gamefiles\\currentboard.png')
                elif pos == 'o':
                    self.current_board_image.paste(self.o_image, (self.coordinates[i][0], self.coordinates[i][1]), self.o_image)
                    self.current_board_image.save(str(os.getcwd()) + '\\games\\tictactoe\\gamefiles\\currentboard.png')

    def _put_symbol_in_current_pos_string(self, symbol, position):
        list1 = list(self.current_pos_string)
        list1[position] = symbol
        self.current_pos_string = ''.join(list1)

class BookClient:
    def __init__(self):
        self.book_db = sqlite3.connect('databases/books.db')

    def get_book_list(self, head=-1, tail=-1, unread="yes", sort="id"):
        result = "```ID | Title                        | Author                        | Published | Genre                        | Pages | Comment\n"
        cursor = self.book_db.execute("SELECT ID, TITLE, AUTHOR, PUBLISHED, GENRE, PAGES, COMMENT FROM BOOK")
        distances = [3, 29, 30, 10, 29, 6, 20]

        for row in cursor:
            for i, cell in enumerate(row):
                if row:
                    result += str(cell) + (" " * (distances[i] - len(str(cell)))) + "| "
                else:
                    result += "-" + (" " * (distances[i] - len("-"))) + "| "
            result += "\n"

        result += "```"
        return result

    def get_cite_list(self, tail=-1):
        pass

    def add_book_to_db(self, title, author=None, link=None, year=None):
        pass

    def add_cite_to_db(self, cite, book_title=None):
        pass

    def remove_book_from_db(self, index):
        pass

    def remove_cite_from_db(self, index):
        pass

    #Net so wichtig!
    def get_unread_books(self, username):
        pass

    def mark_as_read(self, username, book):
        pass


class PornClient:
    def __init__(self):
        pass

class StockClient:
    def __init__(self):
        pass
