from tkinter import *
import tkinter.font as font
import os
from gui.resizer import ImageResizer
from algorithm.ai_sailog import Sailog
from dawg_fsm_dictionary.dawg_fsm import DawgFsm
from game_logic.board_rules import BoardRules
from dawg_fsm_dictionary.txt_dictionarys.load_modify_txt import LoadModifyTxt
from game_logic.tile_bag import TileBag
from random import randint


class MainGui(Tk):
    def __init__(self):
        """Main Gui contains all other frames this way going from one frame two another simplified.
        it also contains the main core object of the DAWG dictionary's and the loader module. """

        Tk.__init__(self)
        self.attributes('-fullscreen', True)
        self.title("Scrabble")
        self.width = int(self.winfo_screenwidth())
        self.height = int(self.winfo_screenheight())
        self.main_font = font.Font(family='Verdana', size=12)
        self.frame_holder = Frame(self, bg='#483D8B', borderwidth=5, relief=RIDGE)
        self.frame_holder.pack(fill=BOTH, expand=YES)
        self.frame_holder.grid_rowconfigure(0, weight=1)
        self.frame_holder.grid_columnconfigure(0, weight=1)
        self.frame_dict = {}
        self.resizer = ImageResizer(self.width, self.height)
        self.image_resized_list = self.resizer.get_right_images()
        self.dawg_basis = DawgFsm()
        self.dawg_advanced = DawgFsm()
        self.loader = LoadModifyTxt()
        self.path_basis = "./dawg_fsm_dictionary/txt_dictionarys/basiswoordenlijst_kleuters.txt"
        self.path_advanced = "./dawg_fsm_dictionary/txt_dictionarys/nederlands_dict.txt"

        for frame in (FrameOne, FrameTwo, BoardFrame):
            this_frame = frame(self.frame_holder, self)
            self.frame_dict[frame] = this_frame
            this_frame.grid(row=0, column=0, sticky="nsew")

        self.next_frame(FrameOne)

    def next_frame(self, next_frame):
        frame = self.frame_dict[next_frame]
        frame.lift()

    def quit_program(self):
        self.destroy()

    def reload_dictionary(self):
        """After a new words had been added the fsm must run again.
        Reload the dictionary node from the txt's"""
        self.create_dictionary(self.dawg_basis, self.path_basis)
        self.create_dictionary(self.dawg_advanced, self.path_advanced)

    def create_dictionary(self, dictionary, path):
        """for each word fill the node's """
        dictionary.reset_all()
        file = self.loader.load_txt(path)
        for line in file:
            dictionary.create_words(line.strip('\n'))
        dictionary.clear_redundant()


class FrameOne(Frame):
    def __init__(self, parrent_frame, main_gui):
        """Frame one contains to options for stopping, beginning the game and adding words"""
        Frame.__init__(self, parrent_frame)
        self.config(bg="#483D8B")
        background = Label(self, bg="blue", borderwidth=5, relief=RIDGE, font=main_gui.main_font)
        background.place(relx=0.5, rely=0.5, anchor="center")
        background.config(image=main_gui.image_resized_list[0])

        start_button = Button(self, text="Begin game", command=lambda:  [main_gui.reload_dictionary(), main_gui.next_frame(BoardFrame)],
                                    bg='#0063D3', activebackground='#004BA0', fg='white', font=main_gui.main_font)
        start_button.place(relx=0.5, rely=0.45, anchor="center")

        change_txt_button = Button(self, text="Woorden toevoegen of verwijderen", command=lambda: main_gui.next_frame(FrameTwo),
                              bg='#0063D3', activebackground='#004BA0', fg='white', font=main_gui.main_font)
        change_txt_button.place(relx=0.5, rely=0.55, anchor="center")

        quit_button = Button(self, text="Stoppen", command=lambda: main_gui.quit_program(),
                             bg='#0063D3', activebackground='#004BA0', fg='white', font=main_gui.main_font)
        quit_button.place(relx=0.5, rely=0.65, anchor="center")


class FrameTwo(Frame):
    def __init__(self, parrent_frame, main_gui):
        """This class  containts the functions/ buttons to add words to the dictionary"""
        Frame.__init__(self, parrent_frame)
        self.config(bg="#99A3A4")
        self.loader = LoadModifyTxt()
        background = Label(self, bg="blue", borderwidth=5, relief=RIDGE, font=main_gui.main_font)
        background.place(relx=0.5, rely=0.5, anchor="center")
        background.config(image=main_gui.image_resized_list[1])

        self.word_entry = Entry(self, font=main_gui.main_font)
        self.word_entry.place(relx=0.5, rely=0.45, anchor="center", relwidth=0.15, relheight=0.05)

        add_button = Button(self, text="Toevoegen", command=lambda: self.add_word(),
                                   bg='#0063D3', activebackground='#004BA0', fg='white', font=main_gui.main_font)
        add_button.place(relx=0.5, rely=0.55, anchor="center")

        remove_button = Button(self, text="Verwijderen", command=lambda: self.remove_word(),
                            bg='#0063D3', activebackground='#004BA0', fg='white', font=main_gui.main_font)
        remove_button.place(relx=0.5, rely=0.60, anchor="center")

        back_button = Button(self, text="Terug", command=lambda: main_gui.next_frame(FrameOne),
                             bg='#0063D3', activebackground='#004BA0', fg='white', font=main_gui.main_font)
        back_button.place(relx=0.5, rely=0.65, anchor="center")

    def add_word(self):
        """Add word to txt with loader script"""
        word = self.word_entry.get()
        if word != "":
            self.loader.add_to_txt("./dawg_fsm_dictionary/txt_dictionarys/basiswoordenlijst_kleuters.txt", word)
        self.word_entry.delete(0, END)

    def remove_word(self):
        """Remove word to txt with loader script"""
        word = self.word_entry.get()
        if word != "":
            self.loader.remove_word_from_txt("./dawg_fsm_dictionary/txt_dictionarys/basiswoordenlijst_kleuters.txt", word)
        self.word_entry.delete(0, END)


class BoardFrame(Frame):
    def __init__(self, parrent, main_gui):
        """
        This class contains the buttons and labels to create the board and corresponding buttons. All the functions
        are for the sole purpose of highlighting the right buttons ad the right time. The class only use's the board_logic
        to determine state of the board.
        """
        Frame.__init__(self, parrent)
        self.config(bg="black", width=0.1, height=0.1)
        self.main_gui = main_gui
        background = Label(self, bg="blue", borderwidth=5, relief=RIDGE)
        background.place(relx=0.5, rely=0.5, anchor="center")
        background.config(image=main_gui.image_resized_list[2])

        self.tileframe = Frame(self, width=1, height=1, bg="red")
        self.tileframe.place(relx=0.5, rely=0.525, anchor="c")

        self.rackframe = Frame(self, width=10, height=5, bg="red")
        self.rackframe.place(relx=0.5, rely=0.95, anchor="c")

        self.win_frame = Frame(self, bg="#a8cdf7")

        self.win_label = Label(self.win_frame, text="De winner is:", bg="#c9daf8", compound=CENTER, font=main_gui.main_font)
        self.win_label.place(relx=0.5, rely=0.2, relwidth=0.4, relheight=0.2, anchor='n')

        self.win_point_label = Label(self.win_frame, text=0, bg="#c9daf8", compound=CENTER, font=main_gui.main_font)
        self.win_point_label.place(relx=0.5, rely=0.55, relwidth=0.8, relheight=0.25, anchor='n')

        self.tilelist = [[BoardTile(self, self.tileframe, "", j, i) for i in range(15)] for j in range(15)]
        self.tilerack = [RackTile(self, self.rackframe, "") for i in range(7)]

        for index in range(15):
            for tile_index in range(15):
                self.tilelist[index][tile_index].grid(row=index, column=tile_index)
        for index in range(7):
            self.tilerack[index].grid(row=0, column=index)

        self.turn_without_placement_label = Label(self, text="Overgeslagen beurten: 0", bg="#c9daf8", compound=CENTER, font=main_gui.main_font)
        self.turn_without_placement_label.place(relx=0.8, rely=0.2, relwidth=0.15, relheight=0.05, anchor='n')

        self.point_player_label = Label(self, text= "Speller punten: 0", bg="#c9daf8", compound=CENTER, font=main_gui.main_font)
        self.point_player_label.place(relx=0.8, rely=0.40, relwidth=0.125, relheight=0.05, anchor='n')

        self.point_ai_label = Label(self, text="Computer punten: 0",  bg="#c9daf8", compound=CENTER, font=main_gui.main_font)
        self.point_ai_label.place(relx=0.8, rely=0.55, relwidth=0.125, relheight=0.05, anchor='n')

        back_button = Button(self, text="Back ", command=lambda: [self._reset_game(), main_gui.next_frame(FrameOne)],
                             bg='#0063D3', activebackground='#004BA0', fg='white', font=main_gui.main_font)
        back_button.place(relx=0.075, rely=0.925, relwidth=0.10, relheight=0.05, anchor='n')

        self.reset_button = Button(self, text="Reset ", command=lambda: self._reset_game(),
                                   bg='#0063D3', activebackground='#004BA0', fg='white', font=main_gui.main_font,
                                   state="disabled")
        self.reset_button.place(relx=0.2, rely=0.925, relwidth=0.10, relheight=0.05, anchor='n')

        self.start_button = Button(self, text="Start ", command=lambda: self._start_game(),
                                   bg='#0063D3', activebackground='#004BA0', fg='white', font=main_gui.main_font)
        self.start_button.place(relx=0.325, rely=0.925, relwidth=0.10, relheight=0.05, anchor='n')

        self.check_button = Button(self, text="Check ", command=lambda: self.verify_board(), state="disabled",
                                   bg='#0063D3', activebackground='#004BA0', fg='white', font=main_gui.main_font)
        self.check_button.place(relx=0.675, rely=0.925, relwidth=0.10, relheight=0.05, anchor='n')

        self.skip_button = Button(self, text="Overslaan", command=lambda: self.skip_player_turn(), state="disabled",
                                   bg='#0063D3', activebackground='#004BA0', fg='white', font=main_gui.main_font)
        self.skip_button.place(relx=0.8, rely=0.925, relwidth=0.10, relheight=0.05, anchor='n')

        self.trade_button = Button(self, text="Ruilen", command=lambda: self.start_trade(), state="disabled",
                                  bg='#0063D3', activebackground='#004BA0', fg='white', font=main_gui.main_font)
        self.trade_button.place(relx=0.925, rely=0.85, relwidth=0.10, relheight=0.05, anchor='n')

        self.confirm_trade_button = Button(self, text="Ruil tegels", command=lambda: self.trade_player_tiles(), state="disabled",
                                  bg='#0063D3', activebackground='#004BA0', fg='white', font=main_gui.main_font)
        self.confirm_trade_button.place(relx=0.925, rely=0.925, relwidth=0.10, relheight=0.05, anchor='n')

        self.tile_bag = TileBag()

        self.board_rules = BoardRules()
        self.board_rules.create_board()
        self.board_rules.setup_tile()

        self.trading = False
        self.trading_letters = []
        self.current_holding_letter = ""
        self.current_placed_letters = []
        self.player_points = 0
        self.ai_points = 0
        self.turn_without_placement = 0
        self.ai_speler = Sailog()

    def _set_point_count(self):
        """Set point count"""
        self.point_ai_label.config(text= "Computer punten: "+ str(self.ai_points))
        self.point_player_label.config(text= "Speler punten: " + str(self.player_points) )

    def _set_turn_count(self):
        """Set turn count"""
        self.turn_without_placement_label.config(text="Overgeslagen beurten: " + str(self.turn_without_placement))

    def _reset_game(self):
        """Reset game"""
        self.board_rules.reset_board()
        self.confirm_trade_button.config(state="disabled")
        self.trade_button.config(state="disabled")
        self.start_button.config(state="normal")
        self.check_button.config(state="disabled")
        self.trade_button.config(state="disabled")
        self.skip_button.config(state="disabled")
        self.current_holding_letter = ""
        self.current_placed_letters = []
        self.trading_letters = []
        self.turn_without_placement = 0
        self.player_points = 0
        self.ai_points = 0
        self._set_point_count()
        self.tile_bag.reset_tile_bag()
        self._set_turn_count()

        for row in self.tilelist:
            for tile in row:
                tile.set_state_disable()
                tile.config(text="")
                tile.reset_colour()

        for tile in self.tilerack:
            tile.change_text("")
            tile.set_state_disable()
        self.reset_button.config(state="disabled")

    def verify_end_board(self):
        """Verify if end board"""
        if self.turn_without_placement >= 20:
            if self.ai_points > self.player_points:
                self.win_point_label.config(text="Computer met " + str(self.ai_points) + " punten." + "\nVolgende keer beter")
            else:
                self.win_point_label.config(text="Player met " + str(self.ai_points) + " punten.")
            self.win_frame.place(relx=0.5, rely=0.525, anchor="c", relwidth=0.2, relheight=0.2,)
            self._reset_game()
        elif self.tile_bag.get_tiles_left() == 0 and self.turn_without_placement >= 10:
            return -1

    def verify_board(self):
        """Verify new board with board_logic"""
        self.skip_button.config(state="normal")
        self.check_button.config(state="disabled")
        self.trade_button.config(state="normal")
        gui_board = self._get_board_tiles()
        self.board_rules.set_validate_letters(gui_board)
        if self.board_rules.validate_board(self.main_gui.dawg_basis) or self.board_rules.validate_board(self.main_gui.dawg_advanced):
            self.player_points += self.board_rules.calculate_points(gui_board)
            self.board_rules.set_board_letters(gui_board) # Board is True
            self._set_board_tiles(self.board_rules.get_board_letters())
            self._reduce_gui_tiles()
            self._set_rack_tiles(self.tile_bag.get_amount_of_letters(self._count_tiles()))
            self._reset_state_rack_tiles()
            self._verify_state_board()
            self._set_point_count()
            self.turn_without_placement = 0
            self.ai_turn(self.board_rules.get_board_letters())
        else:
            self._set_board_tiles(self.board_rules.get_board_letters())
            self._verify_state_board()
            self._reset_state_rack_tiles()
        self.verify_end_board()

    def _reduce_gui_tiles(self):
        """remove placed letters from tile rack"""
        for placed_letter in self.current_placed_letters:
            for tile in self.tilerack:
                if tile.get_text() == placed_letter:
                    tile.change_text("")
                    break

    def skip_player_turn(self):
        """Skip turn"""
        self.turn_without_placement += 1
        self._set_turn_count()
        self.ai_turn(self.board_rules.get_board_letters())

    def _count_tiles(self):
        """count_rack_tiles """
        count = 0
        for tile in self.tilerack:
            if tile.get_text() == "":
                count += 1
        return count

    def _start_game(self):
        """Start game"""
        self.skip_button.config(state="normal")
        self.trade_button.config(state="normal")
        self.reset_button.config(state="normal")
        self.start_button.config(state="disabled")
        self.win_frame.place_forget()
        self._set_rack_tiles(self.tile_bag.get_amount_of_letters(7))
        for row in self.tilelist:
            for tile in row:
                tile.set_state_normal()
        decision = randint(0, 1)
        if decision == 1:
            self.ai_turn(self.board_rules.get_board_letters())

    def _set_board_tiles(self, matrix):
        """set all board tiles"""
        for row in range(len(matrix)):
            for column in range(len(matrix[row])):
                self.tilelist[row][column].change_text(matrix[row][column])
                self.tilelist[row][column].reset_colour()

    def _set_rack_tiles(self, letters):
        """set all rack tiles"""
        for row in range(len(self.tilerack)):
            for letter in letters:
                if self.tilerack[row].get_text() == "":
                    self.tilerack[row].config(state="normal")
                    self.tilerack[row].change_text(letter)
                    letters.remove(letter)
                    break

    def _get_board_tiles(self):
        """get all board tiles"""
        matrix = []
        for row in self.tilelist:
            row_list = []
            for tile in row:
                row_list.append(tile.get_text())
            matrix.append(row_list)
        return matrix

    def _reset_state_rack_tiles(self):
        """Reset rack tiles"""
        for tile in self.tilerack:
            if tile.get_text() != "":
                tile.set_state_normal()

    def _verify_state_board(self):
        """Decide if button must me highlighted or not"""
        for row in self.tilelist:
            for tile in row:
                if tile.get_text() != "":
                    tile.config(bg='#f5c346')
                    tile.config(state="disabled")
                else:
                    tile.config(state="normal")

    def set_current_holding_letter(self, object):
        """set current holding butten letter"""
        self.skip_button.config(state="disabled")
        if self.trading == False:
            self.trade_button.config(state="disabled")
            if self.current_holding_letter == "":
                self.current_holding_letter = object.get_text()
                object.config(state="disabled")
        else:
            self.trading_letters.append(object.get_text())
            object.config(state="disabled")

    def place_holding_letter(self, object):
        """place current holding butten letter on button"""
        if self.current_holding_letter != "":
            self.check_button.config(state="normal")
            object.config(text=self.current_holding_letter)
            object.config(bg='#f5c346')
            self.current_placed_letters.append(self.current_holding_letter)
            self.current_holding_letter = ""
            self._verify_state_board()

    def start_trade(self):
        """Start tade button"""
        self.skip_button.config(state="disabled")
        self.trade_button.config(state="disabled")
        self.confirm_trade_button.config(state="normal")
        self.trading = True
        self.trade_enable_disable_board()

    def trade_enable_disable_board(self):
        """disable board during trade"""
        for row in self.tilelist:
            for tile in row:
                if self.trading == True:
                    tile.config(state="disabled")
                else:
                    tile.config(state="normal")

    def trade_player_tiles(self):
        """Confirm trading of tiles button"""
        self.trading = False
        if len(self.trading_letters) != 0:
            new_letters = []
            for letter in self.trading_letters:
                new_letter = self.tile_bag.trade_leter(letter)
                if new_letter != False:
                    new_letters.append(new_letter)
                else:
                    new_letters.append(letter)

            for index in range(len(self.trading_letters)):
                for row in range(len(self.tilerack)):
                    if self.tilerack[row].get_text() == self.trading_letters[index]:
                        self.tilerack[row].change_text(new_letters[index])
                        break
            self.trading_letters = []
        self.trade_enable_disable_board()
        self._reset_state_rack_tiles()
        self.confirm_trade_button.config(state="disabled")
        self.trade_button.config(state="normal")
        self.skip_button.config(state="normal")
        self.ai_turn(self.board_rules.get_board_letters())
        self._set_turn_count()

    def ai_turn(self, matrix):
        """Ai Turn Uses sailog logic to determine word/response"""
        new_matrix, current_tiles = self.ai_speler.determine_next_move(self.main_gui.dawg_basis, matrix, self.tile_bag)
        if len(current_tiles) != 7:
            self.ai_points += self.board_rules.calculate_points(new_matrix)
            self._set_board_tiles(new_matrix)
            self.board_rules.set_board_letters(new_matrix)
            self._verify_state_board()
            self._set_point_count()
            self.turn_without_placement = 0
        else:
            self.turn_without_placement += 1
        self._set_turn_count()
        self._verify_state_board()
        self.verify_end_board()


class BoardTile(Button):
    """Class board tiles is a TK button and takes care of the colours and letters."""
    def __init__(self, master, parrent, current, row, column):
        Button.__init__(self, parrent, command=lambda: master.place_holding_letter(self),
                        bg="#e9e9e9", activebackground='#e9e9e9', text=current, height=2, width=4, state="disabled")
        self.current_object = self
        self.row = row
        self.column = column
        self.dark_red = "#cc080a"
        self.dark_blue = "#1f5dc4"
        self.light_blue = "#a8cdf7"
        self.roze = "#fdc7d0"
        self.colours = {"00": self.dark_red, "07": self.dark_red, "014": self.dark_red, "70": self.dark_red, "714": self.dark_red,
                        "140": self.dark_red, "147": self.dark_red, "1414": self.dark_red, "15": self.dark_blue, "19": self.dark_blue,
                        "51": self.dark_blue,  "55": self.dark_blue, "59": self.dark_blue, "513": self.dark_blue, "91": self.dark_blue,
                        "95": self.dark_blue, "99": self.dark_blue, "913": self.dark_blue, "135": self.dark_blue, "139": self.dark_blue,
                        "03": self.light_blue, "011": self.light_blue, "26": self.light_blue, "28": self.light_blue, "37": self.light_blue,
                        "314": self.light_blue, "30": self.light_blue, "62": self.light_blue, "66": self.light_blue, "68": self.light_blue,
                        "612": self.light_blue, "73": self.light_blue, "711": self.light_blue, "82": self.light_blue, "86": self.light_blue,
                        "88": self.light_blue, "812": self.light_blue, "117": self.light_blue, "1114": self.light_blue,
                        "126": self.light_blue, "128": self.light_blue, "143": self.light_blue, "1411": self.light_blue, "11": self.roze,
                        "22": self.roze, "113": self.roze, "212": self.roze, "311": self.roze, "33": self.roze, "44": self.roze, "410": self.roze,
                        "77": self.roze, "104": self.roze, "1010": self.roze, "1111": self.roze, "122": self.roze, "1212": self.roze,
                        "131": self.roze, "1313": self.roze}
        self.set_colour(row, column)

    def set_colour(self, row, column):
        """Set button colour"""
        string = str(row) + str(column)
        if string in self.colours:
            self.current_object.config(bg=self.colours[string])

    def reset_colour(self):
        """Reset button colour"""
        string = str(self.row) + str(self.column)
        if string in self.colours and self.get_text() == "":
            self.current_object.config(bg=self.colours[string])
        elif self.row == 11 and self.column == 0 and self.get_text() == "":
            self.current_object.config(bg="#a8cdf7")
        else:
            self.current_object.config(bg="#e9e9e9")

    def get_text(self):  # , char
        """Get button text"""
        return self.current_object['text']

    def change_text(self, char):
        """Change button text"""
        self.config(text=char)

    def set_state_normal(self):
        """Set state normal"""
        self.config(state="normal")

    def set_state_disable(self):
        """Set state disable"""
        self.config(state="disabled")


class RackTile(Button):
    """ This Class contains the rack tile buttons and functions to change the button and text"""
    def __init__(self, master, parrent, current):
        Button.__init__(self, parrent, command=lambda: master.set_current_holding_letter(self), text=current, bg='#f5c346', activebackground='#f5c346', height=2, width=4, state="disabled")
        self.current_object = self

    def get_text(self):
        """Get button text"""
        return self.current_object['text']

    def change_text(self, char):
        """Change button text"""
        self.config(text=char)

    def set_state_normal(self):
        """Set state normal"""
        self.config(state="normal")

    def set_state_disable(self):
        """Set state disable"""
        self.config(state="disabled")




