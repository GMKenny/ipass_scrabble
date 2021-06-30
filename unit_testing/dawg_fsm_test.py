from dawg_fsm_dictionary.dawg_fsm import DawgFsm
import unittest


class TestDawgFsm(unittest.TestCase):

    def test_dawg_fsm(self):
        """Simple node verification no minimization has taking place."""
        dawg_test = DawgFsm()
        dawg_test.create_words("kat")
        dawg_test.create_words("klap")
        dawg_test.create_words("knaap")
        dawg_test.clear_redundant()

        self.assertEqual(dawg_test.is_word("klap"), True)
        self.assertEqual(dawg_test.is_word("katten"), False)
        self.assertEqual(dawg_test.is_word("klap"), True)
        self.assertEqual(dawg_test.is_word("katt"), False)
        self.assertEqual(dawg_test.is_word("ka"), False)

    def test_dawg_fsm_two(self):
        """Multiple end node point are merged"""
        dawg_test = DawgFsm()
        dawg_test.create_words("blaf")
        dawg_test.create_words("blafen")
        dawg_test.create_words("kalf")
        dawg_test.create_words("kat")
        dawg_test.create_words("katten")
        dawg_test.clear_redundant()

        self.assertEqual(dawg_test.is_word("blaf"), True)
        self.assertEqual(dawg_test.is_word("blafen"), True)
        self.assertEqual(dawg_test.is_word("kat"), True)
        self.assertEqual(dawg_test.is_word("katten"), True)
        self.assertEqual(dawg_test.is_word("katt"), False)
        self.assertEqual(dawg_test.is_word("blafe"), False)
        self.assertEqual(dawg_test.is_word("kalf"), True)

