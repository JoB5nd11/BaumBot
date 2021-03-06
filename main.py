import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

import utils
import games
import clients

class BaumBot:
    def __init__(self, token=None):
        self.token = token

        intents = discord.Intents.all()

        self.client = commands.Bot(command_prefix=".")
        self.slash = SlashCommand(self.client, sync_commands=True)
        self.voice_channel = None

        self.init_clients()
        self.init_games()
        self.init_events()
        self.init_commands()

    def run(self):
        self.client.run(self.token)

    def init_clients(self):
        self.book_client = clients.BookClient()
        self.music_client = clients.MusicClient()
        self.porn_client = clients.PornClient()
        self.random_client = clients.RandomClient()
        self.reddit_client = clients.RedditClient()
        self.response_client = clients.ResponseClient()
        self.rule34_client = clients.Rule34Client()
        self.stock_client = clients.StockClient()

    def init_games(self):
        self.ttt_game = games.TicTacToe()
        self.madn_game = games.Madn()
        self.sticky_diamond_slot = games.StickyDiamonds() #TODO

    def init_events(self):
        @self.client.event
        async def on_ready(): #Show registration data on load-up e.g. 'BaumBot#4721' in console
            print('We have logged in as {0.user}'.format(self.client))

        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return
            response = self.response_client.responde(message.content)
            if response:
                await message.channel.send(response)

    def init_commands(self):
        #DEBUG commands
        @self.slash.slash(name="test", description="A simple test function")
        async def test(context: SlashContext):
            await context.defer()
            await context.send('callback from client')

        @self.slash.slash(name="lines", description="LOC of BaumBot")
        async def lines(context: SlashContext):
            # await context.defer()
            await context.send(utils.calc_loc())

        @self.slash.slash(name="ping", description="Speed Test for the BaumBot")
        async def ping(context: SlashContext):
            await context.send('BaumBot Speed: {}ms'.format(round(self.client.latency * 1000), 0))

        @self.slash.slash(name="shutdown", description="Shuts down the BaumBot. Cannot be undone!")
        async def shutdown(context: SlashContext):
            await context.send('Goodbye ????')
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


        #Response Client Calls
        @self.slash.slash(name="printresponses", description="Prints a list of all responses")
        async def printresponses(context: SlashContext):
            await context.send(self.response_client.print_responses())

        @self.slash.slash(name="addresponse", description="Add a new Response to BaumBot's response list",
                          options=[create_option(name="trigger", description="Text that triggers BaumBot's answer", option_type=3, required=True),
                                   create_option(name="answer", description="Text that BaumBot should return", option_type=3, required=True)])
        async def addresponse(context: SlashContext, trigger, answer):
            self.response_client.add_response(trigger, answer)
            await context.send(f'Added Response: `{trigger} -> {answer}`')

        @self.slash.slash(name="deleteallresponses", description="Deletes All Answers from a specific Trigger",
                          options=[create_option(name="trigger", description="Text that triggers BaumBot's answer", option_type=3, required=True)])
        async def deleteallresponses(context: SlashContext, trigger):
            await context.send(self.response_client.delete_all_reponses(trigger))

        @self.slash.slash(name="deleteresponse", description="Deletes a specific Answer from a specific Trigger",
                          options=[create_option(name="trigger", description="Text that triggers BaumBot's answer", option_type=3, required=True),
                                   create_option(name="answer", description="Text that BaumBot should return", option_type=3, required=True)])
        async def deleteresponse(context: SlashContext, trigger, answer):
            await context.send(self.response_client.delete_response(trigger, answer))


        #Book Client Calls
        @self.slash.slash(name="getbooklist", description="Prints the Book-Database",
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


        #Music Client Calls
        @self.slash.slash(name="play", description="Plays music from given link",
                          options=[create_option(name="url", description="The Url of the music website", option_type=3, required=True)])
        async def play(context: SlashContext, url: str):
            self.voice_channel = await utils.check_and_join(self.voice_channel, context)
            await context.defer()
            title = self.music_client.play(self.voice_channel, url)
            await context.send(title)

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

        @self.slash.slash(name="currentsong", description="Show the currently playing song")
        async def currentsong(context: SlashContext):
            await context.defer()
            await context.send(self.music_client.current_song)

        @self.slash.slash(name="printqueue", description="Show all the song that are in queue")
        async def printqueue(context: SlashContext):
            await context.defer()
            await context.send(self.music_client.print_queue())

        @self.slash.slash(name="clearqueue", description="Clears the current queue")
        async def clearqueue(context: SlashContext):
            await context.defer()
            await context.send(self.music_client.clear_queue())

        @self.slash.slash(name="nextsong", description="Stops the current song and plays the next in the queue")
        async def nextsong(context: SlashContext):
            await context.defer()
            await context.send(self.music_client.next_song(self.voice_channel))

        @self.slash.slash(name="repeatcurrentsong", description="Repeats the current song a given number of times",
                          options=[create_option(name="count", description="numbers of times the song should be repeated", option_type=4, required=True)])
        async def repeatcurrentsong(context: SlashContext, count: int =0):
            await context.defer()
            await context.send(self.music_client.repeat_current_song(count))

        #TODO Spotify Ingetration
        #TODO radio <genre>
        #TODO add sfx


        #Porn Client Calls
        #TODO Random porn video
        #TODO Random porn image gallery
        #TODO Random category <media: video/image> <get links: yes/no>
        #TODO Random porn star <media: video/image> <get links: yes/no>
        #TODO Random porn page
        #TODO Random From Fav List <media: video/image>
        #TODO Get From Category <site> <media: video/image>
        #TODO Get From Star <site> <media: video/image>


        #Random Client Calls
        @self.slash.slash(name="randomnumber", description="Returns a random number", options=[
                          create_option(name="min", description="lowest possible number", option_type=4, required=False),
                          create_option(name="max", description="highest possible number", option_type=4, required=False)])
        async def randomnumber(context: SlashContext, min: int = 0, max: int = 1):
            await context.send(self.random_client.get_random_number(min, max))

        @self.slash.slash(name="russianroulette", description="Shoot already")
        async def russianroulette(context: SlashContext):
            if self.random_client.get_random_number(1, 6) == '6':
                message = "You died!"
                #TODO Timeout for today
            else:
                message = "You live (for now)"
            await context.send(message)


        #Reddit Client Calls
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


        #Rule 34 Client Calls
        @self.slash.slash(name="randomr34", description="Gives back random r34 post",
        options=[create_option(name="search", description="Keyword for the search", option_type=3, required=False),
                 create_option(name="gay", description="Can search be gay", option_type=5, required=False),
                 create_option(name="hentai", description="Can search be Hentai", option_type=5, required=False),
                 create_option(name="animated", description="Can search be animated", option_type=5, required=False),
                 create_option(name="drawing", description="Can search be drawn", option_type=5, required=False),
                 create_option(name="comic", description="Can search be a Comic", option_type=5, required=False)])
        async def randomr34(context: SlashContext, search:str="levi", gay:bool= None, hentai:bool= None, animated:bool= None, drawing:bool= None, comic:bool= None):
            await context.defer()
            await context.send(self.rule34_client.getr34img(search, gay, hentai, animated, drawing, comic))

        #Conversion Client Calls
        #kg to lb and stuff

        #Timer Client Calls

        #Math Client Calls
        #calc
        #calc4x
        #calccomplexconv
        #mathplot2d
        #mathplot3d
        #mathderivative
        #mathintegral
        #makechart

        #Science Client Calls
        #Draw molecule

        #Stock Client Calls
        #TODO get stock value <stock name> <date>
        #TODO get stock graph <stock name> <time [today, week, month, year, 5year, all]>
        #TODO get crypto value <crypto name> <date>
        #TODO get crypto graph <crypto name> <time [today, week, month, year, 5year, all]>
        #TODO get top flop of the day
        #TODO cash converter
        #Finance system? <- pls no, im a virign


        #Discord Bot Games calls?
        #TODO multiple simultanious games (ID system)
        #TODO AI OPs

        #TicTacToe
        @self.slash.slash(name="ttt", description="TicTacToe Game Commands", options=[
                          create_option(name="getboard", description="gets the current board", option_type=5, required=False),
                          create_option(name="makeboard", description="creates a board from given string", option_type=3, required=False),
                          create_option(name="clearboard", description="clears the current board image", option_type=5, required=False),
                          create_option(name="draw", description="draws the next character on given space", option_type=3, required=False)])
        async def ttt(context: SlashContext, getboard: bool =False, makeboard: str ='', clearboard: bool =False, draw: str ='x0'):
            if clearboard:
                await context.send(file=self.ttt_game.clear_board())
            elif getboard:
                await context.send(file=self.ttt_game.get_board())
            elif makeboard:
                await context.send(file=self.ttt_game.get_board(makeboard))
            elif draw != 0:
                await context.send(file=self.ttt_game.move(draw))
            else:
                await context.send("I have a stroke :|")

        #Mensch aegere dich nicht
        @self.slash.slash(name="madn", description="MADN Game Commands", options=[
                          create_option(name="debug", description="commands for debug purposes", option_type=3, required=False, choices=[
                                        create_choice(name="showblankboard", value="showblankboard"),
                                        create_choice(name="printrules", value="printrules"),
                                        create_choice(name="printgamestate", value="printgamestate"),
                                        create_choice(name="printstatus", value="printstatus"),
                                        create_choice(name="printgameid", value="printgameid"),
                                        create_choice(name="printplayers", value="printplayers"),
                                        create_choice(name="printturn", value="printturn"),
                                        create_choice(name="roll6", value="roll6")]),
                          create_option(name="loadgame", description="loads a game from a given ID", option_type=3, required=False),
                          create_option(name="setup", description="commands for setting up the game", option_type=3, required=False, choices=[
                                        create_choice(name="newgame", value="newgame"),
                                        create_choice(name="register_red", value="register_red"),
                                        create_choice(name="register_blue", value="register_blue"),
                                        create_choice(name="register_yellow", value="register_yellow"),
                                        create_choice(name="register_green", value="register_green"),
                                        create_choice(name="register_random", value="register_random"),
                                        create_choice(name="start", value="start")]),
                          create_option(name="play", description="commands for playing the game", option_type=3, required=False, choices=[
                                        create_choice(name="roll", value="roll"),
                                        create_choice(name="move1", value="move1"),
                                        create_choice(name="move2", value="move2"),
                                        create_choice(name="move3", value="move3"),
                                        create_choice(name="move4", value="move4")]),
                          create_option(name="extra", description="extra optionen for moves and the game", option_type=3, required=False, choices=[
                                        create_choice(name="moveback", value="moveback")])])
        async def madn(context: SlashContext, debug: str = None, loadgame: str = None, setup: str = None, play: str = None, extra: str = None):
            res = self.madn_game.process_command(context, debug, loadgame, setup, play, extra)
            if isinstance(res, str):
                await context.send(res)
            elif res:
                await context.send(file=res)
                await context.send(self.madn_game.next_step())
            else:
                await context.send(self.madn_game.execute_stroke_protocoll())



        #TODO 4 gewinnt
        #TODO Chess
        #TODO Risiko
        #TODO Poker
        #TODO UNO
        #TODO Dame
        #TODO Backgamnom
        #TODO Monopoly
        #TODO Snakes and Ladders
        #TODO Slot Machine (Multiple?)
        #TODO Minesweeper
        #TODO Solitaire
        #TODO Battleship
        #TODO City Buidler

        #Casino Client Calls (also Game Client, but with Money)
        @self.slash.slash(name="casino", description="Get Casino Commands", options=[
                          create_option(name="getbalance", description="see the money amount you have", option_type=5, required=False),
                          create_option(name="getbankbalance", description="see the money of the bank", option_type=5, required=False),
                          create_option(name="getgames", description="prints out all the casino games", option_type=5, required=False)])
        async def casino(context: SlashContext, getbalance: bool = False, getbankbalance: bool = False, getgames: bool = False):
            pass

        @self.slash.slash(name="blackjack", description="Blackjack Game Commands", options=[
                          create_option(name="join", description="join a game of blackjack", option_type=5, required=False),
                          create_option(name="hit", description="set a amount of coins on your current hand", option_type=4, required=False),
                          create_option(name="stand", description="wait for the end of the round", option_type=5, required=False),
                          create_option(name="double", description="double you current bet (only on first move)", option_type=5, required=False),
                          create_option(name="split", description="split you current hand (only if double on hand)", option_type=5, required=False),
                          create_option(name="surrender", description="drop your current hand and lose your bet", option_type=5, required=False),
                          create_option(name="printrules", description="prints the blackjack's rules", option_type=5, required=False)])
        async def blackjack(context: SlashContext, join: bool = False, hit: int = None, stand: bool = False, double: bool = False,
                                                   split: bool = False, surrender: bool = False, printrules: bool = False):
            pass
        #Blackjack
            # registration
            #/blackjack join
            # hit, stand, double, split, surrender
            #/blackjack hit:<value>
            #/blackjack stand
            #/blackjack double
            #/blackjack split
            #/blackjack surrender

            # both blackjack 3:2 -> 30$ out for 20$ in

        #Insults #TODO

        #Other
        #Team Generator
        @self.slash.slash(name="generateteams", description="Splits all attendees in 'General' into teams", options=[
                          create_option(name="teams", description="number of teams to create", option_type=4, required=False),
                          create_option(name="fair", description="Wether teams split should be even", option_type=5, required=False)])
        async def generateteams(context: SlashContext, teams: int = 2, fair: bool = True):
            member_list = [member.name for member in self.client.get_channel(849279926700212298).members if member != self.client.user]
            await context.send(utils.generate_teams(member_list, teams, fair))


        #Testing
        @self.slash.slash(name="testgif", description="Testing function for gifs")
        async def testgif(context: SlashContext):
            from PIL import Image
            import glob
            file_names = ['./games/madn/assets/blue1.png',
                          './games/madn/assets/green1.png',
                          './games/madn/assets/red1.png',
                          './games/madn/assets/yellow1.png']
            frames = [Image.open(image) for image in file_names]
            frame_one = frames[0]
            frame_one.save("my_awesome.gif", format="GIF", append_images=frames, save_all=True, duration=400, loop=0)
            with open('./my_awesome.gif', 'rb') as f:
                await context.send(file=discord.File(f, filename='my_awesome.gif'))

        @self.slash.slash(name="testslotroll", description="Test rolling a slot")
        async def testslotroll(context: SlashContext):
            slot = self.sticky_diamond_slot
            await context.send(slot.test_roll())


if __name__ == '__main__':
    with open('./safe/token.txt', 'r') as file:
        token = file.readline().strip()
    baumBot = BaumBot(token)
    baumBot.run()
