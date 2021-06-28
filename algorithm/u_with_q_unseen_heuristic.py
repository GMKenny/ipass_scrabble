
class UWithQUnseen:
    def __init__(self):
        """Heuristic strategy: play words with the letter q and u as soon as possible since they are hard to
        play after the game progresses"""
        self.q_and_u = ["q", "u"]

    def filter_u_with_q_words(self, all_words):
        """
        For every word in all_words determine if te current letter of the word is equal to a Q or U.
            if letter is equal to q or q append the word to new list and remove word form original list
        return the new list with the the original list on the back.

        :param all_words: list of all possible words
        :return: sorted list with the u with q words up front
        """
        none_q_u_words = all_words.copy()
        q_u_words = []
        for word in range(len(all_words)):
            for letter in range(len(all_words[word])):
                if all_words[word][letter] in self.q_and_u:
                    q_u_words.append(all_words[word][letter])
                    break
        none_q_u_words = list(set(none_q_u_words) - set(q_u_words))
        return q_u_words + none_q_u_words

