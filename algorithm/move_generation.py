import copy


class MoveGeneration:
    def __init__(self):
        """Class MoveGeneration returns a matrix with a new word based upon a list of words, list of letters tiles and
            board/matrix. it wil loop through the different words and and determine if the there is a position that
            allows for a connection with another letter but while still being validly word and placed.
             (instead of multiple functions transpose the board and run the same loop)"""

        self.board = []
        self.rack_tiles = []
        self.word_list = []

    def set_current_board_tiles_words(self, board, rack_tiles, word_list):
        """
        :param board: Matrix with letters
        :param rack_tiles: list of letters
        :param word_list: possible words made with the letters and board
        """
        self.board = board
        self.rack_tiles = rack_tiles
        self.word_list = word_list

    def get_next_move(self, dawg_dict):
        """
        create a new list wit the original matrix/board and a matrix of the original matrix transposed.
        for each position on the matrix/board verify if there is any word that fids in the matrix that is a valid word
        and valid position. if the length of the rack tiles is not 7, a valid position was found and return the matrix/board
        and rack tiles.

        :param dawg_dict: Dictionary to check valid words
        :return: return new/old matrix and rack tiles/list of letters
        """
        current_boards = [self.board] + [self._get_transposed_matrix(self.board)]
        # for each position
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                # Generate a word based on the given word_list, current_board, row, column and dawg_dict
                matrix, rack = self._move_generation(self.word_list, current_boards, row, column, dawg_dict)

                if len(rack) != 7:
                    return matrix, rack
        return self.board, self.rack_tiles

    def _move_generation(self, all_words, current_boards, row, column, dawg_dict):
        """
        For every word in the all_words list, for every matrix/board verify:
        if not at least one connection_point in the row or column continue with next matrix.
        if the letter before the first letter and and the letter after the last letter are not empty continue with next matrix.

        copy the variable of list of rack tiles/letters and the current matrix
        if the word placed on the matrix/board has no anchor point or the letters are either not in the rack or board continue with next matrix.
        for all words placed on the board verify if all of the placed words are valid words if not continue with next matrix.

        if the matrix is 1 (transposed) transpose the board again en return the board/matrix and rack tiles/list of letter
        :param all_words: list of all possible words.
        :param current_boards: current board/matrix.
        :param row: current row.
        :param column: current column.
        :param dawg_dict: Dictionary.
        :return:
        """
        for word in all_words:
            for matrix in range(len(current_boards)):  # vertical en horizontal
                if not self._find_one_connections(current_boards[matrix], row, column):
                    continue

                front_tile_empty = self._empty_neighbor_letter(current_boards[matrix], row, column, 0, -1)
                back_tile_empty = self._empty_neighbor_letter(current_boards[matrix], row, column, 0, len(word))

                if not front_tile_empty or not back_tile_empty:
                    continue

                rack_tiles = self.rack_tiles[:]
                eddited_board = copy.deepcopy(current_boards[matrix])  # 3 dagen van me leven.

                if not self._verify_anchor_point(word, row, column, eddited_board, rack_tiles):
                    continue

                word_list = self._collected_matrix_words(eddited_board)

                in_dict = True
                for side_words in word_list:
                    if not dawg_dict.is_word(side_words):
                        in_dict = False
                if not in_dict:
                    continue

                if matrix == 1:
                    new_board = self._get_transposed_matrix(eddited_board)
                else:
                    new_board = eddited_board

                return new_board, rack_tiles
        return self.board, self.rack_tiles

    def _get_transposed_matrix(self, board):
        """
        get a matrix and return a transposed matrix
        :param board: matrix
        :return: transposed_matrix
        """
        transposed_matrix = [list(a) for a in zip(*board)]
        return transposed_matrix

    def _collected_matrix_words(self, current_board):
        """
        for each side of the board return all words that are longer than 1 item.

        for each matrix, for each row in the matrix, for each letter in the row if the current letter is equal to
        nothing append a space else at the letter.
        for each item in word_list filter the spaces or less than 1 letter and remove them from the list.
        return a list of words.
        :param current_board: current matrix.board
        :return: list of all possible words of the matrix
        """
        word_list = ""
        current_board = current_board[:]
        for index in range(2): # verticaal en horizontaal
            for row in current_board:
                for letter in row:
                    if letter == '':
                        word_list += " "
                    else:
                        word_list += letter
            current_board = self._get_transposed_matrix(current_board)
        word_list = [x for x in list(filter(lambda item: item != "", "".join(word_list).split(" "))) if len(x) > 1]
        return word_list

    def _empty_neighbor_letter(self, board, row, column, placement_row, placement_column):
        """
        Try to get the neighbor letter of the matrix/board if not exist or empty return true else false
        :param board: matrix/board
        :param row: current row
        :param column: current column
        :param placement_row: int to increase
        :param placement_column: int to increase
        :return: boolean True or False
        """
        try:
            if board[row+placement_row][column+placement_column] == "":
                return True
        except IndexError:
            return True
        return False

    def _verify_anchor_point(self, word, row, column, eddited_board, rack_tiles):
        """
        For each letter in word verify that there either in the rack tiles or in the board.

        create 2 variables boolean letters_found, anchor_point_tile set to False.
        for letter in the range of the word try to get te current item board item, if not break.
        if the current letter is on the board set anchor_point_tile and letters_found True, elif the current letter
        is empty but is in the rack tiles remove letter from rack tiles and set letters_found True, else break.

        if the row and column are the middle of the board 7,7 set anchor_point_tile True.
        if either anchor_point_tile, letters_found or the len of the rack tiles is 7 return False else return True

        :param word: string: word
        :param row: current row
        :param column: current column
        :param eddited_board: matrix/board
        :param rack_tiles: current list of letters
        :return: boolean True or False
        """
        letters_found = False
        anchor_point_tile = False

        for letter_index in range(len(word)):
            letters_found = False

            try:
                current_board_letter = eddited_board[row][column + letter_index]
            except IndexError:
                break

            if current_board_letter == word[letter_index]:
                anchor_point_tile = True
                letters_found = True
            elif current_board_letter == "" and word[letter_index] in rack_tiles:
                eddited_board[row][column + letter_index] = word[letter_index]
                rack_tiles.remove(word[letter_index])
                letters_found = True
            else:
                break

        if row == 7 and column == 7:
            anchor_point_tile = True
        if not letters_found or not anchor_point_tile or len(rack_tiles) == 7:
            return False
        return True

    def _find_one_connections(self, board, row, column):
        """
        reduce the list of possible searches by verifying if there are even any anchor point to connect to.

        if row and column are equal to 8 return True,
        for row in the board if there is one position filled return True.
        for column in the board if there is one position filled return True.
        else return False.
        :param board: matrix/board
        :param row: current row
        :param column: current column
        :return: boolean True or False
        """
        if row == 7 and column == 7:
            return True
        for index in range(column, 15):
            if board[row][index] != "":
                return True
        for index in range(row, 15):
            if board[index][column] != "":
                return True
        return False



