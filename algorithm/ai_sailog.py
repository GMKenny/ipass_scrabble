from itertools import combinations as iter_comb
from algorithm.vowel_consonant_heuristic import VowelConsonant
from algorithm.first_turn_and_hot_spot_heuristic import FirstTurnOpenAndHotSpotBlock
from algorithm.u_with_q_unseen_heuristic import UWithQUnseen
from algorithm.move_generation import MoveGeneration


class Sailog:
    def __init__(self):
        """
        Sailog = Scrabble Artificial Intelligence Logopedische Game
        This class create the reaction of the ai speller during the session.
        it uses the different heuristic strategy's, move generation and tile bag to determine the best valid move to place.
        """
        self.current_tiles = []
        self.turn_passed_without_placement = 0
        self.current_board_tiles = []
        self.vc_heuristic = VowelConsonant()
        self.fto_hsb_heuristic = FirstTurnOpenAndHotSpotBlock()
        self.uwq_unseen = UWithQUnseen()
        self.move_generation = MoveGeneration()

    def set_current_tiles(self, current_tiles):
        """
        :param current_tiles: list of letters
        :set: current_tiles
        """
        self.current_tiles = current_tiles

    def determine_next_move(self, dawg_dict, board_matrix, tile_bag):
        """
        if there are 2 turns in where no changes where made trade tiles
        Get new tiles based upon the current length of the tiles minus seven.
        Get all possible word combination the current board en letters can make.
        Verify all the possible words with the dictionary for valid words.
        Sort the list of all possible words based upon the different heuristics and count of tiles left.
        Set the current matrix/board, rack tiles/list of letters and list of possible words.
        Get next matrix and racktiles based upon the set data.
        if the current tiles remains the same no changes where made increase turns with out placement.

        :param dawg_dict: Dictionary
        :param board_matrix: matrix
        :param tile_bag: tile bag
        :return: matrix/board and rack tiles/list of letters
        """
        if self.turn_passed_without_placement == 2:
            self._replace_tiles(tile_bag)

        self.current_tiles.extend(tile_bag.get_amount_of_letters(7 - len(self.current_tiles)))
        al_board_lettes = self._get_all_board_letters_words(board_matrix)
        possible_words = self._get_all_word_combination_tiles(al_board_lettes, self.current_tiles)

        valid_rack_words = self._get_valid_words(possible_words, dawg_dict)

        tile_bag_count = tile_bag.get_tiles_left()
        words_to_check = self._get_heuristic_words(tile_bag_count, valid_rack_words)

        self.move_generation.set_current_board_tiles_words(board_matrix, self.current_tiles, words_to_check)
        new_board, self.current_tiles = self.move_generation.get_next_move(dawg_dict)

        if len(self.current_tiles) == 7:
            self.turn_passed_without_placement += 1
        if len(self.current_tiles) < 7:
            self.turn_passed_without_placement = 0

        return new_board, self.current_tiles

    def _get_heuristic_words(self, tile_bag_count, valid_rack_words):
        """
        Determine by the count of tile left in the tile bag what heuristic to use for sorting the word list.
        For the first turn when there are 89 tiles still in the bag use First turn and hot spot heuristic.
        until there are 20 left in the tile hot spot heuristic.
        when there are less than 20 tiles in the bag check use vowel consonant heuristic.
        :param tile_bag_count: count of tiles left
        :param valid_rack_words: all valid rack words.
        :return: sorted list based of the heuristic.
        """
        if tile_bag_count == 89:
            double_check = self.fto_hsb_heuristic.get_order_by_smallest(valid_rack_words)
            words_to_check = self.fto_hsb_heuristic.get_smaller_words_size_six(double_check)
        elif tile_bag_count > 20:
            words_to_check = self.fto_hsb_heuristic.get_order_by_smallest(valid_rack_words)
            words_to_check = self.uwq_unseen.filter_u_with_q_words(words_to_check)
        else:
            words_to_check = self.vc_heuristic.determine_vowel_consonant_move(self.current_tiles, valid_rack_words)
        return words_to_check

    def _get_all_board_letters_words(self, matrix):
        """
        Get all possible words and letters from the board/matrix
        for each item in the matrix add the letter the list if not empty and not already in list.
        :param matrix: list matrix
        :return: list of all board letters and words
        """
        word_list = ["",]
        current_matrix = matrix
        for i in range(2):
            for row in range(len(current_matrix)):
                word = ""
                for column in range(len(current_matrix[row])):
                    if current_matrix[row][column] != "":
                        word += current_matrix[row][column]
                    elif word != "":
                        if word not in word_list:
                            word_list.append(word)
            current_matrix = list(zip(*current_matrix))
        return word_list


    def _get_all_word_combination_tiles(self, word_list, racktiles):
        """Create a list of all possible words made width the board/matrix words and racktiles
        for each letter and word in the list create all possible combinations made with the rack tiles.
        return list of words.
         """
        all_combonations = []
        for word in word_list:
            repeat_list = racktiles + [word]
            for lenght in range(0, len(repeat_list) + 1):
                for sub in iter_comb(repeat_list, lenght):
                    if sub not in all_combonations:
                        all_combonations.append(sub)
        return all_combonations


    def _get_valid_words(self, possible_words, dawg_dict):
        """

        :param possible_words:
        :param dawg_dict:
        :return:
        """
        valid_words = []
        for word in possible_words:
            current_word = "".join(word)
            if dawg_dict.is_word(current_word):
                if current_word not in valid_words:
                    valid_words.append(current_word)
        return valid_words

    def _replace_tiles(self, tile_bag):
        """
        for the length of the current tiles owned divided by 2.
        if there are letters from the tile bag add them to the list and remove the letter given
        :param tile_bag: tile_bag
        :set turn passed and current tiles
        """
        for i in range(len(self.current_tiles) // 2):
            tiles = tile_bag.trade_leter(self.current_tiles[i])
            if tiles:
                self.current_tiles.remove(self.current_tiles[i])
                self.current_tiles.extend(tiles)
        self.turn_passed_without_placement = 0









