

class LoadModifyTxt:
    def __init__(self):
        """Class for editing and sorting the txt during load or txt adjustments"""
        self.word_list = []

    def load_txt(self, location):
        """
        Load every word from the file and add them to a list.
        return a sorted list.
        :param location: location of file
        :return: sorted list
        """
        self.word_list = []
        file = open(location, "r")
        for line in file:
            self.word_list.append(line.strip('\n'))
        return sorted(self.word_list)

    def add_to_txt(self, location, word):
        """
        adding word to txt file
        :param location: location of file
        :param word: string
        """
        with open(location, "a") as file:
            file.write(word)

    def remove_word_from_txt(self, location, word):
        """
        Removes a given word from the txt file
        :param location: location of file
        :param word: word to remove
        """
        file = open(location, "r")
        for line in file:
            txt_word = line.strip('\n')
            if txt_word == word:
                continue
            self.word_list.append(txt_word)
        self._write_file(location, self.word_list)

    def _write_file(self, location, word_list):
        """
        rewrite the txt
        :param location: location of file
        :param word_list: list of words
        """
        with open(location, "w") as file:
            file.writelines(word_list)

