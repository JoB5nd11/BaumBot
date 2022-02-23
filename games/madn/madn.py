import os
import random
import discord

class Madn:
    def __init__(self):
        #Is not None so if returned it shows in chat
        self.status = "<no status>"
        self.gamestate = "<no gamestate>"
        self.gameid = "<no gameid>"
        self.players = {}
        self.turn = "<no game>"

        self.games_folder = os.getcwd() + '\\games\\'
        self.asset_folder = os.getcwd() + '\\games\\madn\\assets\\'

        self.is_register_time = False
        self.colors = ['red', 'blue', 'yellow', 'green']


    def process_command(self, context, debug, loadgame, setup):
        if debug:
            return self._run_debug(debug)
        if loadgame:
            return self._run_loadgame(loadgame)
        if setup:
            #Context to know wich user registered as which player
            return self._run_setup(context, setup)


    def _run_debug(self, debug):
        if debug == 'showblankboard':
            return self._return_blank_board()
        if debug == 'printrules':
            return self._get_rules()
        if debug == 'printgamestate':
            return self.gamestate
        if debug == 'printstatus':
            return self.status
        if debug == 'printgameid':
            return self.gameid
        if debug == 'printplayers':
            return self._print_players()
        if debug == 'printturn':
            return self.turn
        return self.execute_stroke_protocoll()


    def _run_loadgame(self, id):
        #TODO Loadgame
        #TODO return Text with /madn play:showcurrentboard command
        pass


    def _run_setup(self, context, setup):
        if setup == 'newgame':
            return self._create_new_game()
        if 'register' in setup:
            #give user and color to function
            return self._register_player(context.author.name, setup.split('_')[1])
        if setup == 'start':
            return self._start_game()
        return self.execute_stroke_protocoll()


    def _get_rules(self):
        return ('Each play rools the dice up to 3 times. When a 6 is rolled can place his first \n'
                'figure on its starting point. If the player does not roll a 6 he/she can roll \n'
                'roll the dice again three times at the next round. \n'
                '\n'
                'Once a player has a figure on the board the goal is to get the figure around the \n'
                'board into the goal. For that he can roll the dice once and walk a rolled amount on \n'
                'the board. \n'
                '\n'
                'If the players figure land on a tile with another players figure on it, the player can \n'
                'the opponent who has to retread to its home.'
                '\n'
                'If there already is another figure of yours on the desired tile you are have to move \n'
                'another figure. \n'
                '\n'
                'The game is finished if one players has all of his pieces in the goal.\n'
                '\n'
                'EXTRAS: \n'
                '- A player is allowed to move backwards ONLY if he can attack another player with this move. \n'
                '- When moving inside of the goal it is not allowed to skip pieces. Each piece must move \n'
                '  individually. If a high number is rolled a player can decide to move only less \n'
                '  (inside the goal). The remaining moves will be dropped.')


    def _create_new_game(self):
        self.status = 'setup'
        self.is_register_time = True
        self.gameid = self._generate_new_id()
        self.gamestate = self._generate_new_gamestate()

        return (f'Your GameID is **{self.gameid}**\n'
                'Please register for the game now...')


    def _register_player(self, user, color):
        if not self.is_register_time:
            return ('Now is not the time for registration. \n'
                    'Please use `/madn setup:newgame` to start a new game \n'
                    'or `/madn loadgame:<id>` to load into an existing game.')

        if color == 'random':
            free_color_list = []
            for color in self.colors:
                if color not in self.players:
                    free_color_list.append(color)

            color = random.choice(free_color_list)

        self.players[color] = user

        return f'Welcome `{user}`, your are **{color.upper()}**'


    def _start_game(self):
        #TODO No None-Player can start or play
        if not self.is_register_time:
            return ('Now it not the time to start a game. \n'
                    'Please use `/madn setup:newgame` to start a new game \n'
                    'or `/madn loadgame:<id>` to load into an existing game.')

        first_color = random.choice(list(self.players.keys()))
        first_player = self.players[first_color]
        self.turn = first_color

        return ('Let the Game begin! \n'
                f'`{first_player} ({first_color})` begins...')


    def _generate_new_gamestate(self):
        return 'rrrr0000-bbbb0000-yyyy0000-gggg0000-0000000000000000000000000000000000000000'


    def _return_blank_board(self):
        with open(str(os.getcwd()) + self.asset_folder + 'board.png', 'rb') as f:
            file = discord.File(f, filename=str(os.getcwd()) + self.asset_folder + 'board.png')
        return file


    def _generate_new_id(self):
        #TODO CRC32
        return str(hex(random.randint(1_000_000, 9_999_999)).split('x')[1])

    def _print_players(self):
        answer = ""
        if 'red' in self.players:
            answer += (f'**Red**: {self.players["red"]}\n')
        if 'blue' in self.players:
            answer += (f'**Blue**: {self.players["blue"]}\n')
        if 'yellow' in self.players:
            answer += (f'**Yellow**: {self.players["yellow"]}\n')
        if 'green' in self.players:
            answer += (f'**Green**: {self.players["green"]}\n')

        if answer == "":
            return 'No players registered yet, use `/madn setup:register_<color>` to register'
        return answer


    def execute_stroke_protocoll(self):
        #TODO Real Error message?
        return 'I have a stroke :|'


class Figure:
    def __init__(self, number):
        self.number = -1
        self.position = -1
        self.is_in_house = True
        self.is_in_goal = False



if __name__ == '__main__':
    madn = Madn()
    # print(madn._register_player('Xaver115', 'random'))
