import os
import random
import discord
from PIL import Image
#TODO
# - Cannot register if full message
# - Show color of who's turn it is

class Madn:
    def __init__(self):
        #Is not None so if returned it shows in chat
        self.status = "<no status>"
        self.gamestate = "<no gamestate>"
        self.gameid = "<no gameid>"
        self.players = {
            'red': None,
            'blue': None,
            'yellow': None,
            'green': None,
        }
        self.current_player = "<no game>"

        self.games_folder = os.getcwd() + '\\games\\'
        self.asset_folder = os.getcwd() + '\\games\\madn\\assets\\'

        self.colors = ['red', 'blue', 'yellow', 'green']
        self.next_step = ''

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

    def next_step(self):
        return self.next_step

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
            return self.current_player
        if debug == 'roll6':
            if self.current_player.username == 'Xaver115':
                return self._roll_dice(self.current_player, dice=6)
            return 'You have no permission to use this command!'
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
        if not 'play' in self.status:
            return ('You have not started a game. \n'
                    'Please use `/madn setup:newgame` to start a new game \n'
                    'or `/madn loadgame:<id>` to load into an existing game.')

        player = None
        for p in self.players.values():
            if p.username == context.author.name:
                player = p
                break

        #If the context author is not in self.players
        if player == None:
            return ('Excuse me, but you do not participate in this game. \n'
                    'Wait for the next game to join...')

        if play == 'roll':
            if not 'roll' in self.status:
                return ('You cannot roll the dice now. \n'
                        'You have to move one of the following figures: \n'
                        f'{self.current_player.get_moveable_figures_as_string()}')
            return self._roll_dice(player)

        if 'move' in play:
            if not 'move' in self.status:
                return ('You cannot move now. \n'
                        'You have to move roll the dice first with: `/madn play:roll`')
            #give figure number to player.move(),
            #Format: move1, move2, move3 or move4
            player.move(play.split('move')[1])
            return self._generate_current_board_image()

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
        self.players = {
            'red': None,
            'blue': None,
            'yellow': None,
            'green': None,
        }
        self.current_player = "<no game>"

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
                if self.players[color] == None:
                    free_color_list.append(color)

            color = random.choice(free_color_list)

        if self.players[color] != None:
            return 'This color is already occupied, please choose another'

        self.players[color] = Player(user, color, self)
        return f'Welcome `{user}`, your are **{color.upper()}**'


    def _start_game(self):
        if self.status != 'setup':
            return ('Now it not the time to start a game. \n'
                    'Please use `/madn setup:newgame` to start a new game \n'
                    'or `/madn loadgame:<id>` to load into an existing game.')

        for key, value in self.players.items():
            if value != None:
                break
        #Runs only if the loop isn't fully run (if a value was found)
        else:
            return ('You cannot start the game without any registered players... \n'
                    'Please use `/madn setup:register_<color>` to register')

        #Remove all empty keys in Player dict
        to_delete_keys = []
        for key, value in self.players.items():
            if value == None:
                to_delete_keys.append(key)

        for key in to_delete_keys:
            del self.players[key]

        first_color = random.choice(list(self.players.keys()))
        first_player = self.players[first_color] #Returns a player object
        self.current_player = first_player
        self.status = f'play roll {self.current_player}'

        return ('Let the Game begin! \n'
                f'{first_player} begins...')


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

        for key in self.players.keys():
            if self.players[key] != None:
                answer += str(self.players[key]) + '\n'

        if answer == "":
            return 'No players registered yet, use `/madn setup:register_<color>` to register'
        return answer


    def _roll_dice(self, player, dice=None):
        if not 'play' in self.status:
            return ('You have not started a game. \n'
                    'Please use `/madn setup:newgame` to start a new game \n'
                    'or `/madn loadgame:<id>` to load into an existing game.')

        if not self._is_players_turn(player):
            return ('Sorry it is not you turn right now. \n'
                    f'Currently it is {self.current_player}\'s turn')

        if not dice:
            dice = random.randint(1, 6)
        answer = f'You rolled a `{dice}`\n'

        if player.are_all_figures_home() and dice != 6:
            if player.contiguous_turns < 2:
                answer += 'Please roll again'
            else:
                self.current_player.contiguous_turns = 0
                self.current_player = self._get_next_turn_player()

                answer += 'Sorry :/\n'
                answer += f'Next player: {self.current_player}'
                self.status = f'play roll {self.current_player}'
            player.contiguous_turns += 1
            return answer

        #all pieces are at home
        if player.are_all_figures_home() and dice == 6:
            answer += 'You can choose any of your figures to set it on the board...'
            self.status = f'play move out any {self.current_player}'
            return answer

        #at least one piece is at home
        if player.is_one_figure_home() and dice == 6:
            pass

        #all pieces are on the board
        if not player.is_one_figure_home() and dice == 6:
            pass

        #TODO move regularly

        return self.execute_stroke_protocoll()


    def _is_players_turn(self, player):
        for key, value in self.players.items():
            if key == self.current_player.color and value == player:
                return True
        return False


    def _get_next_turn_player(self):
        found = False
        for key, value in self.players.items():
            if found:
                return value

            if key == self.current_player.color:
                found = True

        #If last ones turn, first player in dict is returned
        if found:
            return list(self.players.values())[0]
        else:
            return self.execute_stroke_protocoll()

    #TODO
    def _check_for_capture(self):
        pass

    #TODO
    def _capture(self):
        pass

    def _generate_current_board_image(self):
        board_img = Image.open(self.asset_folder + 'board.png')
        grid_size = 48

        for p in self.players.values():
            for fig in p.figures.values():
                fig_img = Image.open(fig.asset)
                coords = (grid_size * map[fig.position][0] + 10, grid_size * map[fig.position][1]+ 10)
                board_img.paste(fig_img, coords, fig_img)

        board_img.save(self.asset_folder + 'tmp_board.png')
        with open(self.asset_folder + 'tmp_board.png', 'rb') as f:
            return discord.File(f, filename=self.asset_folder + 'tmp_board.png')

    def execute_stroke_protocoll(self):
        #TODO Real Error message?
        return 'I have a stroke :|'


class Player:
    def __init__(self, username, color, game):
        self.username = username
        self.color = color
        self.game = game

        self.figures = {
            '1': Figure(1, self.color, self.game),
            '2': Figure(2, self.color, self.game),
            '3': Figure(3, self.color, self.game),
            '4': Figure(4, self.color, self.game),
        }

        self.start_position = self._get_start_position()
        self.current_roll = -1
        self.in_goal = [None, None, None, None]
        self.contiguous_turns = 0

    def __str__(self):
        return f"`{self.username}` *({self.color})*"

    def move(self, number):
        if self.figures[number].is_in_house:
            return self._move_out(number)

        #TODO regular
        pass

    def _move_out(self, number):
        self.figures[number].move_to(self.start_position)
        self.game.next_step = 'Please roll again'
        return 1 #success

    def are_all_figures_home(self):
        for figure in self.figures.values():
            if not figure.is_in_house:
                return False
        return True

    def is_one_figure_home(self):
        for figure in self.figures.values():
            if figure.is_in_house:
                return True
        return False

    def get_moveable_figures_as_string(self):
        pass

    def _get_start_position(self):
        if self.color == 'red':
            return 0
        if self.color == 'blue':
            return 10
        if self.color == 'green':
            return 20
        if self.color == 'yellow':
            return 30


class Figure:
    def __init__(self, number, color, game):
        self.number = number
        self.color = color
        self.game = game
        self.position = -1
        self.is_in_house = True
        self.is_in_goal = False

        self.asset = os.getcwd() + '\\games\\madn\\assets\\' + f'{self.color}{self.number}.png'
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
            self.position = 39 + self.number
        elif self.color == 'blue':
            self.position = 47 + self.number
        elif self.color == 'yellow':
            self.position = 55 + self.number
        elif self.color == 'green':
            self.position = 63 + self.number
        else:
            raise ValueError(f"The color of this figure ({self.color}) is either not "
                              "red, blue, yellow or green, "
                              "or it is not set yet")

    def move(self, n):
        self.position += n

    def move_to(self, n):
        self.position = n
        return 1 #success

    def reset(self):
        self.setup()

map = {
    0: [11, 7],
    1: [10, 7],
    2: [9, 7],
    3: [8, 7],
    4: [7, 7],
    5: [7, 8],
    6: [7, 9],
    7: [7, 10],
    8: [7, 11],
    9: [6, 11],
    10: [5, 11],
    11: [5, 10],
    12: [5, 9],
    13: [5, 8],
    14: [5, 7],
    15: [4, 7],
    16: [3, 7],
    17: [2, 7],
    18: [1, 7],
    19: [1, 6],
    20: [1, 5],
    21: [2, 5],
    22: [3, 5],
    23: [4, 5],
    24: [5, 5],
    25: [5, 4],
    26: [5, 3],
    27: [5, 2],
    28: [5, 1],
    29: [6, 1],
    30: [7, 1],
    31: [7, 2],
    32: [7, 3],
    33: [7, 4],
    34: [7, 5],
    35: [8, 5],
    36: [9, 5],
    37: [10, 5],
    38: [11, 5],
    39: [11, 6],
    40: [10, 10],
    41: [11, 10],
    42: [10, 11],
    43: [11, 11],
    44: [10, 6],
    45: [9, 6],
    46: [8, 6],
    47: [7, 6],
    48: [1, 10],
    49: [2, 10],
    50: [1, 11],
    51: [2, 11],
    52: [6, 10],
    53: [6, 9],
    54: [6, 8],
    55: [6, 7],
    56: [1, 1],
    57: [2, 1],
    58: [1, 2],
    59: [2, 2],
    60: [2, 6],
    61: [3, 6],
    62: [4, 6],
    63: [5, 6],
    64: [10, 1],
    65: [11, 1],
    66: [10, 2],
    67: [11, 2],
    68: [6, 2],
    69: [6, 3],
    70: [6, 4],
    71: [6, 5],
}


if __name__ == '__main__':
    madn = Madn()
    print(madn._create_new_game(), "\n")
    print(madn._register_player('Test1', 'random'), "\n")
    print(madn._register_player('Test2', 'random'), "\n")
    print(madn._start_game(), "\n")
    print(madn._generate_current_board_image())
