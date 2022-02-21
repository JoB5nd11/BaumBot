import os
import discord
from PIL import Image, ImageDraw, ImageFilter

class TicTacToe:
    def __init__(self):
        self.clear_board()
        self.coordinates = [[0, 0], [100, 0], [200, 0], [0, 100], [100, 100], [200, 100], [0, 200], [100, 200], [200, 200]]
        self.current_pos_string = '---------'
        self.board_image = Image.open(str(os.getcwd()) + '\\games\\tictactoe\\assets\\board.png')
        self.current_board_image = Image.open(str(os.getcwd()) + '\\games\\tictactoe\\gamefiles\\currentboard.png')
        self.x_image = Image.open(str(os.getcwd()) + '\\games\\tictactoe\\assets\\cross.png')
        self.o_image = Image.open(str(os.getcwd()) + '\\games\\tictactoe\\assets\\circle.png')
        self.t_image = Image.open(str(os.getcwd()) + '\\games\\tictactoe\\assets\\tri.png')
        self.s_image = Image.open(str(os.getcwd()) + '\\games\\tictactoe\\assets\\square.png')

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
        elif position[0] == 's':
            self._put_symbol_in_current_pos_string('s', field_nr)
        elif position[0] == 't':
            self._put_symbol_in_current_pos_string('t', field_nr)
        else:
            print("TTT symbol was not in the game set")
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
                elif pos == 's':
                    self.current_board_image.paste(self.s_image, (self.coordinates[i][0], self.coordinates[i][1]), self.s_image)
                    self.current_board_image.save(str(os.getcwd()) + '\\games\\tictactoe\\gamefiles\\currentboard.png')
                elif pos == 't':
                    self.current_board_image.paste(self.t_image, (self.coordinates[i][0], self.coordinates[i][1]), self.t_image)
                    self.current_board_image.save(str(os.getcwd()) + '\\games\\tictactoe\\gamefiles\\currentboard.png')

    def _put_symbol_in_current_pos_string(self, symbol, position):
        list1 = list(self.current_pos_string)
        list1[position] = symbol
        self.current_pos_string = ''.join(list1)
