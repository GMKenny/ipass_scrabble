from dawg_fsm_dictionary.letter_node import LetterNode


class DawgFsm:
    def __init__(self):
        """This Class holds the Directed acyclic word graph finite state machine.
        it holds 4 variables the start node, the last word, a list of all nodes and a list of last position nodes.

        It creates a suffix tree out of the given word with each node representing a letter.
        Example: Kat and Kats contain: Start, K, A, T, S nodes, 5 in total.
        minimizing: after each word that's added to the tree similar end nodes get merged into one by backtrack the already made tree
        Example: Sometime and Time contain: Start, T, I, M, E S, O, M, E nodes, 9 in total

        after all the words are loaded a function can be run to clean the redundant connections."""
        self.startnode = LetterNode("StartNode")
        self.lastword = ""
        self.all_nodes = []
        self.last_position_nodes = []

    def create_words(self, word):
        """
        Create nodes for the given word.
        verify if there was a last word before this word that contains the same letters.
        if there are letter in common current node is the node of the last letter in common, else start node in the current node.
        for every letter from the common letter create a new node and give it the current letter as varible.
            append the node to with all nodes. create a connection between the current node and the new node and from
            the new node to the current node. append the node to a list only word nodes. variable current node is the next node.
        set the Last current node as word. append to list the last node and corresponding letter.
        variable last word is equal to the current word.
        if there are letters in common and the length of word nodes is not equal to zero.
            start minimizing nodes
        :param word: string of word
        """
        commen_letters = self._commen_letters(word)
        word_nodes = []

        if commen_letters > 0:
            current_node = self._get_commen_node(word[:commen_letters])
        else:
            current_node = self.startnode

        for letter in word[commen_letters:]:
            next_node = LetterNode(letter)
            self.all_nodes.append(next_node)

            current_node.create_connection(letter, next_node)
            next_node.create_reversed_connection(letter, current_node)

            word_nodes.append((current_node, letter, next_node))
            current_node = next_node

        current_node.set_is_word()
        self.last_position_nodes.append((current_node.get_letter_node(), current_node))
        self.lastword = word

        if commen_letters != 0 and len(word_nodes) != 0:
            self._minimize_nodes(word_nodes)

    def _minimize_nodes(self, word_nodes):
        """
        Create to variable for holding the node object (last node).
        for item in all last position nodes, if the letter of the current node and last node are the same variable last node is node.
        if the last node variable is none do noting, else: remove the last last node from all node list.
        create connection between the last word node and the last node variable.

        create new variable node to verify by backtracking the node of the last variable object.
        if node to verify is empty break, if the nodes are not either both none words or both words break.
        create a connection between the current node and the second to last node of the node to verify.
        :param word_nodes: current word (word_nodes)
        """
        last_node = None
        for index in range(len(self.last_position_nodes)):
            if self.last_position_nodes[index][0] == word_nodes[-1][1]:
                if self.last_position_nodes[index][1].get_has_connection() == False:
                    last_node = self.last_position_nodes[index][1]
                    break

        if last_node is not None:
            self.last_position_nodes.pop(-1)
            word_nodes[-1][0].create_connection(word_nodes[-1][1], last_node)
            node_verify = last_node.get_reversed_next_node(word_nodes[-1][1])

            for index in range(len(word_nodes) - 2, -1, -1):
                first_node = node_verify
                node_verify = node_verify.get_reversed_next_node(word_nodes[index][1])

                if node_verify is None:
                    break
                if node_verify.get_is_word() != word_nodes[index][2].get_is_word():
                    break
                word_nodes[index][0].create_connection(word_nodes[index][1], first_node)

    def _commen_letters(self, word):
        """
        Create one variable count_similar to hold the count of similar letters.
        for letter in word if the letter is the same as the last word index. add 1 to count else return the current count.
        return count.
        :param word: string of word.
        :return: similar word count.
        """
        count_similar = 0
        for index in range(min(len(word), len(self.lastword))):
            if word[index] == self.lastword[index]:
                count_similar += 1
            else:
                return count_similar
        return count_similar

    def _get_commen_node(self, word):
        """
        for each letter in the word. get the current letter node and return the last node.
        :param word:
        :return:
        """
        commen_node = self.startnode
        for letter in word:
            commen_node = commen_node.get_next_node(letter)
        return commen_node

    def is_word(self, word):
        """
        for each letter in word, try to get the next letter node if letter node exist return if the node is a letter.
        :param word:
        :return:
        """
        similar_node = self.startnode
        try:
            for letter in word:
                similar_node = similar_node.get_next_node(letter)
            return similar_node.get_is_word()
        except AttributeError:
            return False

    def clear_redundant(self):
        """
        (After minimizing nodes clean the list and every object)
        clear the 2 varbiles list in the class
        for node in all nodes clear the reverse back tracking dict.
        """
        self.last_position_nodes.clear()
        for node in self.all_nodes:
            node.clear_redundant_reversed_dict()
        self.all_nodes.clear()

    def reset_all(self):
        """ Clear all nodes and create a new start Node"""
        self.startnode = LetterNode("StartNode")
        self.lastword = ""
        self.all_nodes.clear()
        self.last_position_nodes.clear()



