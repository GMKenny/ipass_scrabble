

class VowelConsonant:
    def __init__(self):
        """Heuristic strategy: place words that are have either more vowels of consonants based on the letters
        remaining in the rack_tiles"""
        # Row below not needed but given for refrence of constants
        # constants ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"]
        self.vowel = ["a", "o", "i", "u", "e"]

    def determine_vowel_consonant_move(self, rack_tiles, all_words):
        """
        for every letter in rack_tiles determine the amount of vowels and consonants.
        for every word in all_words determine the amount of vowels and consonants.
        sort the lists with vowels and consonants on highest value.

        if there are more more vowels in the count of rack_tiles return a list with the vowel words first.
        else return a list with the consonants words first.

        :param rack_tiles: List of letters.
        :param all_words: List of possible words.
        :return: a list with words orders by consonants and vowel amount.
        """
        current_vowel_count, current_consonant_count = self._vowel_consonant_count(rack_tiles)
        vowels, consonanten = self._get_count_dict_vowel_consonant(all_words)

        vowel_word_list = list(sorted(vowels, key=vowels.get, reverse=True))
        consonant_word_list = list(sorted(consonanten, key=consonanten.get, reverse=True))

        if current_vowel_count + 1 > current_consonant_count:
            return vowel_word_list + consonant_word_list
        else:
            return consonant_word_list + vowel_word_list

    def _get_count_dict_vowel_consonant(self, possible_word_list):
        """
        for every word in possible_word_list determine the amount of vowels and consonants.

        :param possible_word_list: list of possible words.
        :return: two dictionary's with the count of the vowels and consonant.
        """
        best_vowel_word = {}
        best_consonant_word = {}
        for word in possible_word_list:
            best_vowel_word[word], best_consonant_word[word] = self._vowel_consonant_count([char for char in word])
        return best_vowel_word, best_consonant_word

    def _vowel_consonant_count(self, letter_list):
        """
        for every letter in letter_list determine the amount of vowels and consonants.
        if current letter is a vowel add 1 to vowel count else letter must be a consonants add 1 to consonants count

        :param letter_list: List of letters.
        :return: two int the count of vowels and consonants
        """

        vowel_count = 0
        consonants_count = 0
        for letter in letter_list:
            if letter in self.vowel:
                vowel_count += 1
            else:
                consonants_count += 1
        return vowel_count, consonants_count

