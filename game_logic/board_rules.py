from game_logic.tile_object import TileObject


class BoardRules:
    def __init__(self):
        """This Class contains the rules of scrabble: Creating the board/matrix objects, How the points are calculated,
        Verifying player placement,Validating the board. it also contains 3 variables: board for containing the matrix,
        point list to determine each letter and its corresponding value and a bonus list to determine wat tiles are bonuses.

        Each object of the matrix is connected to there neighbor tiles
        this is used to determine if the placement always connects to the starting point this is done by a recursive
        search method"""
        self.board = []
        self.point_list = {"a": 1, "b": 3, "c": 5, "d": 2, "e": 1, "f": 4, "g": 3, "h": 4, "i": 2, "j": 7, "k": 3,
                           "l": 3, "m": 3, "n": 1, "o": 1, "p": 3, "q": 10, "r": 2, "s": 2, "t": 2, "u": 4, "v": 4,
                           "w": 5, "x": 8, "y": 8, "z": 4}
        self.bonus_list = {"00": "TWS", "03": "DLS", "07": "TWS", "011": "DLS", "014": "TWS",
                           "11": "DWS", "15": "TLS", "19": "TLS", "113": "DWS",
                           "22": "DWS", "26": "DLS", "28": "DLS", "212": "DWS",
                           "30": "DLS", "33": "DWS", "37": "DLS", "311": "DWS", "314": "DLS",
                           "44": "DWS", "410": "DWS",
                           "51": "TLS", "55": "TLS", "59": "TLS", "513": "TLS",
                           "62": "DLS", "66": "DLS", "68": "DLS", "612": "DLS",
                           "70": "TLS", "73": "DLS", "711": "DLS", "714": "TLS",
                           "82": "DLS", "86": "DLS", "88": "DLS", "812": "DLS",
                           "91": "TLS", "95": "TLS", "99": "TLS", "913": "TLS",
                           "104": "DWS", "1010": "DWS",
                           "110": "DLS", "117": "DLS", "1111": "DWS", "1114": "DLS",
                           "122": "DWS", "126": "DLS", "128": "DLS", "1212": "DWS",
                           "131": "DWS", "135": "TLS", "139": "TLS", "1313": "DWS",
                           "140": "TWS", "143": "DLS", "147": "TWS", "1411": "DLS", "1414": "TWS"}

    def create_board(self):
        """
        Creates a new board/matrix with tile objects.
        """
        self.board = [[TileObject(j, i) for i in range(15)] for j in range(15)]

    def setup_tile(self):
        """
        Setup each object of the matrix to know what its neighbor objects are
        """
        self.board[7][7].set_start_point()
        for row in range(15):
            for column in range(15):
                neighbor_tiles = self._get_neighbor_or_none(row, column)
                self.board[row][column].set_neighbor_connections(neighbor_tiles)
                self._set_bonus_tiles(self.board, row, column)

    def _get_neighbor_or_none(self, row, column):
        """
        Every position has 4 possible neighbors objects.
        Create 2 variables dicts to determine the location of up, down, left, right
        Determine for the current row and column what the neighbors objects are.
        :param row: Current row position
        :param column: Current column position
        """
        neighbor_tiles = [None, None, None, None]  # B O L R
        row_positions = {0: row-1, 1: row+1, 2: row, 3: row}
        column_positions = {0: column, 1: column, 2: column-1, 3: column+1}
        for i in range(4):
            try:
                neighbor_tiles[i] = self.board[row_positions[i]][column_positions[i]]
            except IndexError:
                continue
        return neighbor_tiles

    def _set_bonus_tiles(self, board, row, column):
        """
        Determine for each object if it is a bonus tile or not with the self.bonus_tile list.
        :param board: Tile board objects
        :param row: Current row position
        :param column: Current row position
        """
        if str(row) + str(column) in self.bonus_list:
            board[row][column].set_bonus(self.bonus_list[str(row) + str(column)])

    def get_board_letters(self):
        """Get current board letters"""
        board_letters = [[self.board[row][column].get_letter() for column in range(15)] for row in range(15)]
        return board_letters

    def set_validate_letters(self, new_letters):
        """
        To determine if a board is valid every object has a place holder for the board to verify.
        for each item in the matrix set the new letter of the board/matrix to be validated.
        :param new_letters: matrix of new letters.
        """
        for row in range(15):
            for column in range(15):
                self.board[row][column].set_validate_letter(new_letters[row][column])

    def validate_board(self, dawg_dict):
        """
        if not all letters placed correctly on the board return False else, get all board words.
        for each board word determine if the word is a real word, if not return False.
        when all words are verified return True
        :param dawg_dict: dictonary
        """
        verify_placement = self._verify_placement_correct(self.board)
        if not verify_placement:
            return False

        all_words = self._get_validate_placed_words(self.board)

        for word in all_words:
            if not dawg_dict.is_word(word):
                return False
        return True

    def _verify_placement_correct(self, board):
        """
        For the given matrix, loop though it and verify if the current letter is not equal to empty.
            if the position is the start point continue with next position.
            else get current board object neighbors and determine
                if neighbors is the the start point, continue with next position.
                else: return false
        if all position start point are found return True
        :param board: board / Matrix
        :return: boolean True or False
        """
        for row in range(15):
            for column in range(15):
                if board[row][column].get_validate_letter() != "":
                    if board[row][column].get_start_point():
                        continue
                    else:
                        neighbors = board[row][column].get_neighbor_connections()
                        if self._recursive_search_start_point(board[row][column], neighbors):
                            continue
                        else:
                            return False
        return True

    def _recursive_search_start_point(self, main_object, neighbors):
        """
        For each neighbor object if the object is not none.
            if the neighbor letter is not equal to empty.
                if neighbor is start point return True.
                else current neighbors is the neighbors list minus the main object
                    recursive search the current neighbors if true return True
        if for loop finds no start point return False
        :param main_object: Current object.
        :param neighbors: Neighbor objects
        :return: boolean True or False
        """
        for neighbor in neighbors:
            if neighbor is not None:
                if neighbor.get_validate_letter() != "":
                    if neighbor.get_start_point():
                        return True
                    else:
                        next_neighbors = list(set(neighbor.get_neighbor_connections()) - {main_object})
                        if self._recursive_search_start_point(neighbor, next_neighbors):
                            return True
        return False

    def _get_validate_placed_words(self, board):
        """
        Create a variable current_board that is the board
        For times in range of 2 (Transposed board).
            for every item in the matrix. if the current letter is not empty append the letter to the word else: at Space.
            current_board is a transposed board of the current board.
        Split every word in word list and remove spaces.
        for every word in word list if the word is smaller than 1 remove from list.
        return word list.
        :param board: Current Board/Matrix
        """
        words = ""
        current_board = board
        for times in range(2):
            for row in range(15):
                for column in range(15):
                    letter = current_board[row][column].get_validate_letter()
                    if letter != "":
                        words += letter
                    else:
                        words += " "
            current_board = list(zip(*current_board))
        all_letters_and_words = list(filter(lambda i: i != "", words.split(" ")))
        word_list = [x for x in all_letters_and_words if len(x) > 1]
        return word_list

    def set_board_letters(self, new_board):
        """
        Set permanant correct board letters.
        :param new_board: current board / matrix
        """
        for row in range(15):
            for column in range(15):
                self.board[row][column].set_letter(new_board[row][column])

    def calculate_points(self, new_board):
        """
        To determine if words are placed before or after the turn to matrices are compared with each other. beyond that
        new letters have a different point calculation than already exiting ones including the bonus positions.

        Create variable point is equal to zero. find all new letters added to the matrix and there position.
        if the amount of letters is more than 50 increase points with 50. if no letters where added return 0.
        compare the new board words with the old board if and get all changed words.
        from all the letters of changed words subtract the original letters.

        calculate values of letters changed words and original letters with the corresponding bonuses separately.
        return (the changed word points with the orginal letters point) times the word bonus
        :param new_board: board / matrix
        """
        points = 0
        new_letter_positions = self._get_new_letters_positions(new_board)
        if len(new_letter_positions) > 7:
            points += 50
        if len(new_letter_positions) == 0:
            return 0

        current_board = self.get_board_letters()

        self.set_validate_letters(current_board)
        current_board_words = self._get_validate_placed_words(self.board)

        self.set_validate_letters(new_board)
        new_board_words = self._get_validate_placed_words(self.board)

        all_changed_words = self._get_all_changed_words(current_board_words, new_board_words)
        tiles_on_board = self._retrieve_none_placed_tiles(new_letter_positions, all_changed_words)

        tiles_on_board_points = self._determine_none_bonus_points(tiles_on_board)
        word_bonus, main_word_points = self._determine_bonus_points(new_letter_positions)
        points += ((tiles_on_board_points + main_word_points) * word_bonus)

        return points

    def _get_all_changed_words(self, current_board_word, new_board_word):
        """
        Create Varible copy of new_board_word
        for each word in the old word list, if word if in the new board remove word from the copy
        return all changed words.
        :param current_board_word: list of words
        :param new_board_word: list of words
        """
        all_changed_words = new_board_word.copy()
        for item in current_board_word:
            if item in all_changed_words:
                all_changed_words.remove(item)
        return all_changed_words

    def _retrieve_none_placed_tiles(self, new_letter_positions, all_changed_words):
        """
        Create a variable list_letters that contains all the individual lettes of every word in all changed words.
        for letter in new layed down words, if the letter in list_letters remove letter from list.
        :param new_letter_positions: list of letters
        :param all_changed_words: list of words
        :return: list of letters
        """
        list_letters = [letter for row in all_changed_words for letter in row]

        for letter in new_letter_positions:
            if letter[0] in list_letters:
                list_letters.remove(letter[0])
        return list_letters


    def _get_new_letters_positions(self, matrix):
        """
        get the new letters added to the board/matrix by comparing the old and the new matrix.
        for each item in the old matrix if the item is not equal to new matrix add to list.
        return new letter list.
        :param matrix: matrix / board
        :return: list of new letters
        """
        new_letters = []
        current_board = self.get_board_letters()
        for row in range(len(matrix)):
            for column in range(len(matrix[row])):
                if current_board[row][column] != matrix[row][column]:
                    new_letters.append([matrix[row][column], row, column])
        return new_letters

    def _determine_none_bonus_points(self, letter_list):
        """
        Determine for each letter what point are give to it and add it to variable.
        :param letter_list:
        :return: points
        """
        points = 0
        for letter in letter_list:
            points += self.point_list[letter]
        return points

    def _determine_bonus_points(self, main_word_positions):
        """
        determine for each letter what points are given and what bonus is applied to it and if a word bonus wil be given.
        for letter determine if the board position has a bonus.
            add the corresponding bonus point to bonus points and word bonus to word bonus variables.
        :param main_word_positions:
        :return: word bonus, points
        """
        word_bonus = 0
        points = 0
        for letter_position in main_word_positions:
            bonus = self.board[letter_position[1]][letter_position[2]].get_bonus()
            if bonus == "DLS":
                points += self.point_list[letter_position[0]] * 2
            if bonus == "TLS":
                points += self.point_list[letter_position[0]] * 3
            if bonus == "DWS":
                word_bonus += 2
            if bonus == "TWS":
                word_bonus += 3
            if bonus is None:
                points += self.point_list[letter_position[0]]
        if word_bonus == 0:
            word_bonus = 1
        return word_bonus, points