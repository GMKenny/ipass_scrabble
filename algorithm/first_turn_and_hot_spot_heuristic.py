
class FirstTurnOpenAndHotSpotBlock:
    def __init__(self):
        """Heuristic strategy First Turn Open: play the most smallest possible words with the given words,
        to prevent bonusus and easy wordson the next turn"""
        self.start_position = [7, 7]

    def get_startposition(self):
        """
        Return the start position for first turn open.
        :return: start position.
        """
        return self.start_position

    def get_smaller_words_size_six(self, all_words):
        """
        For each word in all_words if word the length of the words is in between 8 en 2 letter append to list.
        :param all_words: List of all possible words.
        :return all_words_copy: List of words smaller than 8 and bigger than 1.
        """
        all_words_copy = []
        for word in all_words:
            if 7 >= len(word) > 1:
                all_words_copy.append(word)
        return all_words_copy


    def get_order_by_smallest(self, all_words):
        """
        For every word in all_words sort the list by smallest word size fist
        :param all_words : all possible words.
        :return: sorted list of smallest items.
        """
        return sorted(all_words, key=len)

