#Discord imports
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
#Other imports
import time
#Own imports
import utils
import responses
import clients
import r34

class BaumBot:
    def __init__(self, token=None):
        self.token = token

        self.client = commands.Bot(command_prefix=".")
        self.slash = SlashCommand(self.client, sync_commands=True)
        self.guild_ids = [849279926700212294]
        self.voice_channel = None

        self.init_clients()
        self.init_events()
        self.init_commands()

    def run(self):
        self.client.run(self.token)

    def init_clients(self):
        self.responses = responses.Response()
        self.reddit_client = clients.RedditClient()
        self.random_client = clients.RandomClient()
        self.porn_client = clients.PornClient()
        self.music_client = clients.MusicClient()
        self.stock_client = clients.StockClient()
        self.ttt_client = clients.TicTacToeClient()
        self.book_client = clients.BookClient()

    def init_events(self):
        @self.client.event
        async def on_ready(): #Show registration data on load-up e.g. 'BaumBot#4721' in console
        	print('We have logged in as {0.user}'.format(self.client))

        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
            	return
            await message.channel.send(self.responses.responde(message.content))

    def init_commands(self):
        #DEBUG commands
        @self.slash.slash(name="test", description="A simple test function", guild_ids=self.guild_ids)
        async def test(context: SlashContext):
            await context.defer()
            await context.send('callback from client')

        @self.slash.slash(name="ping", description="Speed Test for the BaumBot", guild_ids=self.guild_ids)
        async def ping(context: SlashContext):
            await context.send('BaumBot Speed: {}ms'.format(round(self.client.latency * 1000), 0))

        @self.slash.slash(name="shutdown", description="Shuts down the BaumBot. Cannot be undone!", guild_ids=self.guild_ids)
        async def shutdown(context: SlashContext):
            await context.send('Goodbye 👋')
            quit()

        @self.slash.slash(name="clear", description="Clears the current screen", guild_ids=self.guild_ids)
        async def shutdown(context: SlashContext):
            answer = "."
            for _ in range(100):
                answer += '\n'
            answer += "."
            await context.send(answer)


        #Channel commands
        @self.slash.slash(name="join", description="BaumBot joins the channel of the command author", guild_ids=self.guild_ids)
        async def join(context: SlashContext):
            self.voice_channel = await utils.check_and_join(self.voice_channel, context, on_join=True)

        @self.slash.slash(name="leave", description="BaumBot leaves its current voice channel", guild_ids=self.guild_ids)
        async def leave(context: SlashContext):
            await utils.check_and_leave(self.voice_channel)
            await context.send('I am leaving: "{}"'.format(context.author.voice.channel.name))
            self.voice_channel = None


        #Reddit client calls
        @self.slash.slash(name="randomsubreddit", description="Gives back a random subreddit link", guild_ids=self.guild_ids,
                          options=[create_option(name="nsfw", description="Include, Exclude or Exclusive NSFW", option_type=3, required=False, choices=[
                                                 create_choice(name="Yes", value="yes"),
                                                 create_choice(name="No", value="no"),
                                                 create_choice(name="Only", value="only")]),
                                   create_option(name="count", description="Number of returned subreddit link", option_type=4, required=False),
                                   create_option(name="sort", description="Returned link sort by (e.g. new, hot, top)", option_type=3, required=False, choices=[
                                                 create_choice(name="New", value="/new"),
                                                 create_choice(name="Hot", value="/"),
                                                 create_choice(name="TopHour", value="/top/?t=hour"),
                                                 create_choice(name="TopDay", value="/top/?t=day"),
                                                 create_choice(name="TopMonth", value="/top/?t=month"),
                                                 create_choice(name="TopYear", value="top_year': '/top/?t=year"),
                                                 create_choice(name="TopAll", value="/top/?t=all")])])
        async def randomsubreddit(context: SlashContext, nsfw: str ="yes", count: int =1, sort: str ="/top/?t=all"):
            await context.defer()
            await context.send(self.reddit_client.get_random_subreddit(NSFW=nsfw, count=count, sort=sort))

        @self.slash.slash(name="randomredditpost", description="Gives back a random reddit post", guild_ids=self.guild_ids,
                          options=[create_option(name="nsfw", description="Include, Exclude or Exclusive NSFW", option_type=3, required=False, choices=[
                                                create_choice(name="Yes", value="yes"),
                                                create_choice(name="No", value="no"),
                                                create_choice(name="Only", value="only")]),
                                   create_option(name="count", description="Number of returned posts", option_type=4, required=False),
                                   create_option(name="images", description="Include, Exclude or Exclusive image content", option_type=3, required=False, choices=[
                                                 create_choice(name="Yes", value="yes"),
                                                 create_choice(name="No", value="no"),
                                                 create_choice(name="Only", value="only")]),
                                   create_option(name="spoilers", description="Wether to hide spoilers", option_type=3, required=False, choices=[
                                                 create_choice(name="Yes", value="yes"),
                                                 create_choice(name="No", value="no")])])
        async def randomredditpost(context: SlashContext, nsfw: str ="yes", count: int=1, images: str ="only", spoilers: str ="no"):
            await context.defer()
            await context.send(self.reddit_client.get_random_post(NSFW=nsfw, count=count, images=images))

        @self.slash.slash(name="memesoftheday", description="Gives the 5 best memes of the day", guild_ids=self.guild_ids)
        async def memesoftheday(context: SlashContext):
            await context.defer()
            await context.send(self.reddit_client.get_memes_of_the_day())

        #Music client calls
        @self.slash.slash(name="play", description="Plays music from given link", guild_ids=self.guild_ids,
                          options=[create_option(name="url", description="The Url of the music website", option_type=3, required=True)])
        async def play(context: SlashContext, url: str):
            self.voice_channel = await utils.check_and_join(self.voice_channel, context)
            await context.defer()
            title = self.music_client.play(self.voice_channel, url)
            await context.send(title)

        @self.slash.slash(name="pause", description="Stops the current playing song", guild_ids=self.guild_ids)
        async def pause(context: SlashContext):
            await context.defer()
            self.music_client.pause(self.voice_channel)
            await context.send("Now Paused!")

        @self.slash.slash(name="resume", description="Stops the current playing song", guild_ids=self.guild_ids)
        async def resume(context: SlashContext):
            await context.defer()
            self.music_client.resume(self.voice_channel)
            await context.send("Resumed...")

        @self.slash.slash(name="stop", description="Stops the current playing song", guild_ids=self.guild_ids)
        async def stop(context: SlashContext):
            await context.defer()
            self.music_client.stop(self.voice_channel)
            await context.send("(jazz music stops)")

        @self.slash.slash(name="currentsong", description="Show the currently playing song", guild_ids=self.guild_ids)
        async def currentsong(context: SlashContext):
            await context.defer()
            await context.send(self.music_client.current_song)

        @self.slash.slash(name="printqueue", description="Show all the song that are in queue", guild_ids=self.guild_ids)
        async def printqueue(context: SlashContext):
            await context.defer()
            await context.send(self.music_client.print_queue())

        @self.slash.slash(name="clearqueue", description="Clears the current queue", guild_ids=self.guild_ids)
        async def clearqueue(context: SlashContext):
            await context.defer()
            await context.send(self.music_client.clear_queue())

        @self.slash.slash(name="nextsong", description="Stops the current song and plays the next in the queue", guild_ids=self.guild_ids)
        async def nextsong(context: SlashContext):
            await context.defer()
            await context.send(self.music_client.next_song(self.voice_channel))

        @self.slash.slash(name="repeatcurrentsong", description="Repeats the current song a given number of times", guild_ids=self.guild_ids,
                          options=[create_option(name="count", description="numbers of times the song should be repeated", option_type=4, required=True)])
        async def repeatcurrentsong(context: SlashContext, count: int =0):
            await context.defer()
            await context.send(self.music_client.repeat_current_song(count))

        #TODO add full playlists
        #TODO get current playing
        @self.slash.slash(name="randomr34", description="Gives back random r34 post", guild_ids=self.guild_ids)
        async def randomr34(context: SlashContext):
            await context.defer()
            await context.send(r34.getr34img())

        #TODO push to queue -> simply /play if playing
        #TODO show queue
        #TODO next
        #TODO Repeat: count
        #TODO clearqueue

        #TODO Spotify Ingetration
        #TODO radio <genre>
        #TODO add sfx
        #TODO add r34 bot ;)

        #Book client calls
        @self.slash.slash(name="getbooklist", description="Prints the Book-Database", guild_ids=self.guild_ids,
                          options=[create_option(name="head", description="Number of Books from start", option_type=4, required=False),
                                   create_option(name="tail", description="Number of Books from end", option_type=4, required=False),
                                   create_option(name="unread", description="Include, Exclude or Exclusive read book", option_type=3, required=False, choices=[
                                                 create_choice(name="Yes", value="yes"),
                                                 create_choice(name="No", value="no"),
                                                 create_choice(name="Only", value="only")]),
                                    create_option(name="sort", description="Sort the returned book by", option_type=3, required=False, choices=[
                                                 create_choice(name="ID", value="id"),
                                                 create_choice(name="Title", value="title"),
                                                 create_choice(name="Author", value="author"),
                                                 create_choice(name="Published", value="published"),
                                                 create_choice(name="Genre", value="Genre"),
                                                 create_choice(name="Pages", value="pages")])])
        async def getbooklist(context: SlashContext, head: int =-1, tail: int =-1, unread: str ="yes", sort: str ="id"):
            await context.defer()
            await context.send(self.book_client.get_book_list(head, tail, unread, sort))

        # @self.slash.slash(name="getcitelist", description="Prints the Cite-Database", options=[])
        # async def getcitelist(context: SlashContext):
        #     pass

        # @self.slash.slash(name="addbook", description="Add a book to the BaumBot Book-Database", guild_ids=self.guild_ids,
        #                   options=[create_option(name="title", description="Title of the book", option_type=3, required=True),
        #                            create_option(name="author", description="Author of the book", option_type=3, required=False),
        #                            create_option(name="published", description="Year of publishing of the book", option_type=4, required=False),
        #                            create_option(name="genre", description="Genre of the book (if genre not present do 'owngenre')", option_type=4, required=False, choices=[
        #                                          create_choice(name="Fantasy", value="Fantasy"),
        #                                          create_choice(name="SciFi", value="SciFi"),
        #                                          create_choice(name="Dystopian", value="Dystopian"),
        #                                          create_choice(name="Action & Adventure", value="Action & Adventure"),
        #                                          create_choice(name="Horror", value="Horror"),
        #                                          create_choice(name="Thriller & Suspense", value="Thriller & Suspense"),
        #                                          create_choice(name="Romance", value="Romance")#TODO
        #                            ]),
        #                            create_option(name="owngenre", description="An own genre because it was not in the genre list", option_type=3, required=False),
        #                            create_option(name="pages", description="Number of pages of the book", option_type=4, required=False),
        #                            create_option(name="comment", description="Your comment to the book", option_type=4, required=False)])
        # async def addbook(context: SlashContext):
        #     #ID, TITLE, AUTHOR, PUBLISHED, GENRE, PAGES, COMMENT
        #     pass

        # @self.slash.slash(name="addcite", description="Add a cite to the BaumBot Cite-Database", options=[])
        # async def addcite(context: SlashContext):
        #     pass

        @self.slash.slash(name="removebook", description="Removes a book at a given index", guild_ids=self.guild_ids, options=[])
        async def removebook(context: SlashContext):
            pass

        # @self.slash.slash(name="removecite", description="Removes a cite at a given index", options=[])
        # async def removecite(context: SlashContext):
        #     pass

        @self.slash.slash(name="markread", description="Mark a book at given index as read", guild_ids=self.guild_ids)
        async def markread(context: SlashContext):
            pass
            #If already read mark as unread


        #Random client calls
        @self.slash.slash(name="randomnumber", description="Returns a random number", guild_ids=self.guild_ids, options=[
                          create_option(name="min", description="lowest possible number", option_type=4, required=False),
                          create_option(name="max", description="highest possible number", option_type=4, required=False)])
        async def randomnumber(context: SlashContext, min: int =0, max: int = 1):
            await context.send(self.random_client.get_random_number(min, max))

        #Porn client calls
        #TODO Random porn <website>
        #TODO Random category <get links: yes/no>
        #TODO Random porn star <get links: yes/no>
        #TODO Random porn page

        #Stock client calls?
        #TODO get stock value <stock name> <date>
        #TODO get stock graph <stock name> <time [today, week, month, year, 5year, all]>
        #TODO get crypto value <crypto name> <date>
        #TODO get crypto graph <crypto name> <time [today, week, month, year, 5year, all]>
        #TODO get top flop of the day
        #TODO cash converter
        #Finance system? <- pls no, im a virign

        #Discord Bot Games (TicTacToe, Chess, etc) calls?
        #TODO TicTacToe
        @self.slash.slash(name="ttt", description="Return a image", guild_ids=self.guild_ids, options=[
                          create_option(name="getboard", description="gets the current board", option_type=5, required=False),
                          create_option(name="makeboard", description="creates a board from given string", option_type=3, required=False),
                          create_option(name="clearboard", description="clears the current board image", option_type=5, required=False),
                          create_option(name="draw", description="draws the next character on given space", option_type=3, required=False)])
        async def ttt(context: SlashContext, getboard: bool =False, makeboard: str ='', clearboard: bool =False, draw: str ='x0'):
            if clearboard:
                await context.send(file=self.ttt_client.clear_board())
            elif getboard:
                await context.send(file=self.ttt_client.get_board())
            elif makeboard:
                await context.send(file=self.ttt_client.get_board(makeboard))
            elif draw != 0:
                await context.send(file=self.ttt_client.move(draw))
            else:
                await context.send("I have a stroke :|")

        #TODO 4 gewinnt
        #Insults


if __name__ == '__main__':
    token_file = open('safe/token.txt', 'r')
    Lines = token_file.readlines()
    for line in Lines:
        token = line.split('\n')[0]
    baumBot = BaumBot(token)
    baumBot.run()
