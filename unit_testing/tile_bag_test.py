from game_logic.tile_bag import *
import unittest


class TestTileBag(unittest.TestCase):

    def test_get_tiles_left(self):
        """verify if amount of tiles are removed from tile bag"""
        tile_test = TileBag()
        tile_test.get_amount_of_letters(3)

        self.assertEqual(tile_test.get_tiles_left(), 100)

    def test_reset_tile_bag(self):
        """verify if tile bag reset Reset tile bag"""
        tile_test = TileBag()
        tile_test.get_amount_of_letters(5)
        tile_test.reset_tile_bag()

        self.assertEqual(tile_test.get_tiles_left(), 103)

