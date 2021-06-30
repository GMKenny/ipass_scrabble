from dawg_fsm_dictionary.dawg_fsm import DawgFsm
from algorithm.move_generation import MoveGeneration
from game_logic.board_rules import BoardRules
import unittest


class TestDawgFsm(unittest.TestCase):

    def test_move_generation(self):
        """Verify if a move can be made based on the matrix input"""
        dawg_test = DawgFsm()
        dawg_test.create_words("kat")
        dawg_test.create_words("klap")
        dawg_test.create_words("knaap")
        dawg_test.clear_redundant()

        matrix = [["" for i in range(15)] for j in range(15)]

        move_gen_test = MoveGeneration()
        move_gen_test.set_current_board_tiles_words(matrix, ["k","a","t","a","b","c","d"], ["kat"])
        matrix, left_over_tiles = move_gen_test.get_next_move(dawg_test)

        self.assertEqual(matrix[7], ['', '', '', '', '', '', '', 'k', 'a', 't', '', '', '', '', ''])
        self.assertEqual(left_over_tiles, ['a', 'b', 'c', 'd'])



