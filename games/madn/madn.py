import os
import random
import discord

#TODO
# - Cannot register if full message
# - Show color of who's turn it is

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

        self.colors = ['red', 'blue', 'yellow', 'green']


    def process_command(self, context, debug, loadgame, setup, play, extra):
        if debug:
            return self._run_debug(debug)
        if loadgame:
            return self._run_loadgame(loadgame)
        if setup:
            #Context to know wich user registered as which player
            return self._run_setup(context, setup)
        if play:
            #Context to know which user wants to move
            return self._run_play(context, play)
        if extra:
            return self._run_extra(extra)
        return self.execute_stroke_protocoll()


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


    def _run_play(self, context, play):
        if self.status != 'play':
            return ('You have not started a game. \n'
                    'Please use `/madn setup:newgame` to start a new game \n'
                    'or `/madn loadgame:<id>` to load into an existing game.')

        player = context.author.name

        if play == 'roll':
            return self._roll_dice(player)
        if play == 'move1':
            pass
        if play == 'move2':
            pass
        if play == 'move3':
            pass
        if play == 'move4':
            pass
        return self.execute_stroke_protocoll()


    def _run_extra(self, extra):
        if extra == 'moveback':
            pass
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
        self.gameid = self._generate_new_id()
        self.gamestate = self._generate_new_gamestate()
        self.players = {}
        self.turn = "<no game>"

        return (f'Your GameID is **{self.gameid}**\n'
                'Please register for the game now...')


    def _register_player(self, user, color):
        if self.status != 'setup':
            return ('Now is not the time for registration. \n'
                    'Please use `/madn setup:newgame` to start a new game \n'
                    'or `/madn loadgame:<id>` to load into an existing game.')

        if color == 'random':
            free_color_list = []
            for color in self.colors:
                if color not in self.players:
                    free_color_list.append(color)

            color = random.choice(free_color_list)

        if color in self.players:
            return 'This color is already occupied, please choose another'

        self.players[color] = user

        return f'Welcome `{user}`, your are **{color.upper()}**'


    def _start_game(self):
        if self.status != 'setup':
            return ('Now it not the time to start a game. \n'
                    'Please use `/madn setup:newgame` to start a new game \n'
                    'or `/madn loadgame:<id>` to load into an existing game.')

        if len(list(self.players.keys())) == 0:
            return ('You cannot start the game without any registered players... \n'
                    'Please use `/madn setup:register_<color>` to register')

        first_color = random.choice(list(self.players.keys()))
        first_player = self.players[first_color]
        self.turn = first_color
        self.status = 'play'

        return ('Let the Game begin! \n'
                f'`{first_player} ({self.turn})` begins...')


    def _generate_new_gamestate(self):
        #TODO
        return 'rrrr0000-bbbb0000-yyyy0000-gggg0000-0000000000000000000000000000000000000000'


    def _return_blank_board(self):
        with open(self.asset_folder + 'board.png', 'rb') as f:
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


    def _roll_dice(self, player):
        if self.status != 'play':
            return ('You have not started a game. \n'
                    'Please use `/madn setup:newgame` to start a new game \n'
                    'or `/madn loadgame:<id>` to load into an existing game.')

        if not self._is_players_turn(player):
            return ('Sorry it is not you turn right now. \n'
                    f'Currently it is {self.players[self.turn]}s turn')

        dice = random.randint(1, 6)
        return f'You rolled a {dice}!'


    def _is_players_turn(self, player):
        for key, value in self.players.items():
            if key == self.turn and value == player:
                return True
        return False


    def execute_stroke_protocoll(self):
        #TODO Real Error message?
        return 'I have a stroke :|'


class Figure:
    def __init__(self, number, color):
        self.number = -1
        self.color = None
        self.position = -1
        self.is_in_house = True
        self.is_in_goal = False

        self.GOAL = [-1, -1, -1, -1]

        self.setup()

    def setup(self):
        """
        The Goal position are specific for each color. For the values check the `board_numbers.png`
        in the assets folder.
        The start position is determined by adding the figure number to a board tile. E.g:
        The start positions for the red pieces are: 40, 41, 42, 43
        The first figure should stand on 40, the second on 41, the third on 42 and the fourth on 43.
        There adding the figure number to 39 the start position is determined.
        Likewise for all other colors.
        """
        if self.color == 'red':
            self.GOAL = [44, 45, 46, 47]
            self.position = 39 + self.number

        elif self.color == 'blue':
            self.GOAL = [52, 53, 54, 55]
            self.position = 47 + self.number

        elif self.color == 'yellow':
            self.GOAL = [60, 61, 62, 63]
            self.position = 55 + self.number

        elif self.color == 'green':
            self.GOAL = [68, 69, 70, 71]
            self.position = 63 + self.number

        else:
            raise ValueError(f"The color of this figure ({self.color}) is either not "
                              "red, blue, yellow or green, "
                              "or it is not set yet")

    def move(self, n):
        self.position += n

    def reset(self):
        #TODO
        pass

    def is_in_house(self):
        #TODO
        pass

    def is_in_goal(self):
        #TODO
        pass



if __name__ == '__main__':
    madn = Madn()
    # print(madn._register_player('Xaver115', 'random'))
