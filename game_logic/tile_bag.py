import random


class TileBag:
    def __init__(self):
        """
        This class is for the tile bag, it contains a list of letters. it had different functions to serve the
        purpose of a tile bag: creating tiles, trading tiles, resetting the tile bag,
        """
        self.tilebag = []
        self.create_letters()

    def create_letters(self):
        """
        Create the right amount of tiles for each letter per the scrabble rulles.
        for in range of .. extend a tuple of items into the tilebag list.
        """
        self.tilebag.extend(("q", "x", "y"))
        for index in range(2):
            self.tilebag.extend(("b", "c", "f", "h", "p", "v", "w", "z"))
        for index in range(3):
            self.tilebag.extend(("k", "l", "g", "m", "u", "j"))
        for index in range(5):
            self.tilebag.extend(("d", "t", "s", "r"))
        for index in range(6):
            self.tilebag.extend(("a", "o", "i",))
        for index in range(10):
            self.tilebag.extend(("n"))
        for index in range(18):
            self.tilebag.extend(("e"))

    def get_tiles_left(self):
        """
        :return: Return the amount of tiles left in the bag.
        """
        return len(self.tilebag)

    def reset_tile_bag(self):
        """
        Reset the bag of tiles to begin position
        """
        self.tilebag = []
        self.create_letters()

    def get_amount_of_letters(self, amount):
        """
        For each time amount is get a letter and append to list
        :param amount: int value
        :return: letter list
        """
        letter_list = []
        for times in range(amount):
            letter = self._get_letter()
            if letter != -1:
                letter_list.append(letter)
        return letter_list

    def trade_leter(self, letter):
        """
        Trade letter for another letter if the tile bag is not empty. extend the letter and return another letter
        else return False
        :param letter: string letter
        :return: False or string letter
        """
        if len(self.tilebag) != 0:
            self.tilebag.extend(letter)
            return self._get_letter()
        return False

    def _get_letter(self):
        """
        Get one letter from tile bag if tile bag is not empty
        :return: -1 or string letter
        """
        if len(self.tilebag) != 0:
            return self.tilebag.pop(random.randint(0, len(self.tilebag)-1))
        return -1




