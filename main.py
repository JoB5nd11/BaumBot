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

class BaumBot:
    def __init__(self, token=None):
        self.token = token

        self.client = commands.Bot(command_prefix=".")
        self.slash = SlashCommand(self.client, sync_commands=True)
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
        @self.slash.slash(name="test", description="A simple test function")
        async def test(context: SlashContext):
            await context.send('callback from client')

        @self.slash.slash(name="ping", description="Speed Test for the BaumBot")
        async def ping(context: SlashContext):
            await context.send('BaumBot Speed: {}ms'.format(round(self.client.latency * 1000), 0))

        @self.slash.slash(name="shutdown", description="Shuts down the BaumBot. Cannot be undone!")
        async def shutdown(context: SlashContext):
            await context.send('Goodbye 👋')
            quit()

        @self.slash.slash(name="clear", description="Clears the current screen")
        async def shutdown(context: SlashContext):
            answer = "."
            for _ in range(100):
                answer += '\n'
            answer += "."
            await context.send(answer)

        #Channel commands
        @self.slash.slash(name="join", description="BaumBot joins the channel of the command author")
        async def join(context: SlashContext):
            self.voice_channel = await utils.check_and_join(self.voice_channel, context, on_join=True)

        @self.slash.slash(name="leave", description="BaumBot leaves its current voice channel")
        async def leave(context: SlashContext):
            await utils.check_and_leave(self.voice_channel)
            await context.send('I am leaving: "{}"'.format(context.author.voice.channel.name))
            self.voice_channel = None

        #Reddit client calls
        @self.slash.slash(name="randomsubreddit", description="Gives back a random subreddit link",
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

        @self.slash.slash(name="randomredditpost", description="Gives back a random reddit post",
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

        @self.slash.slash(name="memesoftheday", description="Gives the 5 best memes of the day")
        async def memesoftheday(context: SlashContext):
            await context.defer()
            await context.send(self.reddit_client.get_memes_of_the_day())

        #Music client calls
        @self.slash.slash(name="play", description="Plays music from given link",
                          options=[create_option(name="url", description="The Url of the music website", option_type=3, required=True)])
        async def play(context: SlashContext, url: str):
            self.voice_channel = await utils.check_and_join(self.voice_channel, context)
            await context.defer()
            title = self.music_client.play(self.voice_channel, url)
            await context.send("Now playing: " + title)

        @self.slash.slash(name="pause", description="Stops the current playing song")
        async def pause(context: SlashContext):
            await context.defer()
            self.music_client.pause(self.voice_channel)
            await context.send("Now Paused!")

        @self.slash.slash(name="resume", description="Stops the current playing song")
        async def resume(context: SlashContext):
            await context.defer()
            self.music_client.resume(self.voice_channel)
            await context.send("Resumed...")

        @self.slash.slash(name="stop", description="Stops the current playing song")
        async def stop(context: SlashContext):
            await context.defer()
            self.music_client.stop(self.voice_channel)
            await context.send("(jazz music stops)")

        #TODO Queue -> push -> yeet -> delete
        #TODO Spotify Ingetration
        #TODO Repeat
        #TODO radio <genre>
        #TODO play soundfile

        #Random client calls
        @self.slash.slash(name="randomnumber", description="Returns a random number", options=[
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
        #Finance system? <- pls no im a virign

        #Discord Bot Games (TicTacToe, Chess, etc) calls?
        #TODO TicTacToe
        @self.slash.slash(name="ttt", description="Return a image", options=[
                          create_option(name="getboard", description="gets the current board", option_type=5, required=False),
                          create_option(name="makeboard", description="creates a board from given string", option_type=3, required=False),
                          create_option(name="clearboard", description="clears the current board image", option_type=5, required=False),
                          create_option(name="draw", description="draws the next character on given space", option_type=3, required=False)
        ])
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
