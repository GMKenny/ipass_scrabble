from game_logic.board_rules import BoardRules
from dawg_fsm_dictionary.dawg_fsm import DawgFsm
import unittest


class TestBoardRules(unittest.TestCase):

    def test_set_board(self):
        """Verifying if set and get board letters are working after setup"""
        board_rule_test = BoardRules()
        board_rule_test.create_board()
        board_rule_test.setup_tile()
        new_input = board_rule_test.get_board_letters()
        new_input[7][7] = "k"
        board_rule_test.set_board_letters(new_input)
        output = board_rule_test.get_board_letters()
        self.assertEqual(output[7][7], "k")

    def test_validate_board(self):
        """Validate the board see if words are correctly validated"""
        dawg_test = DawgFsm()
        dawg_test.create_words("kat")
        dawg_test.create_words("klap")
        dawg_test.clear_redundant()

        board_rule_test = BoardRules()
        board_rule_test.create_board()
        board_rule_test.setup_tile()
        new_input = board_rule_test.get_board_letters()

        new_input[7][7] = "k"
        new_input[7][8] = "l"
        new_input[7][9] = "a"
        new_input[7][10] = "p"
        new_input[8][7] = "a"
        new_input[9][7] = "t"

        board_rule_test.set_validate_letters(new_input)
        self.assertEqual(board_rule_test.validate_board(dawg_test), True)

    def test_calculate_points(self):
        """Verify if board point are calculated correctly"""
        dawg_test = DawgFsm()
        dawg_test.create_words("kat")
        dawg_test.create_words("klap")
        dawg_test.clear_redundant()


        board_rule_test = BoardRules()
        board_rule_test.create_board()
        board_rule_test.setup_tile()
        new_input = board_rule_test.get_board_letters()

        new_input[7][7] = "k"
        new_input[7][8] = "l"
        new_input[7][9] = "a"
        new_input[7][10] = "p"
        board_rule_test.set_board_letters(new_input)
        new_input[8][7] = "a"
        new_input[9][7] = "t"

        board_rule_test.set_validate_letters(new_input)
        board_rule_test.validate_board(dawg_test)
        self.assertEqual(board_rule_test.calculate_points(new_input), 6)






