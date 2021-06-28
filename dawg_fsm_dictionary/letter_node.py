
class LetterNode:
    def __init__(self, letter):
        """This class is for the different nodes for the DAWG suffix tree.
        It has 5 variables: one for the letter, one for the connection boolean, one for the is word boolean.
        and there are 2 dictionary for storing the connection between the nodes. one for the valid connection and
        one for the backtracking step of minimizing the nodes."""
        self.letter = letter
        self.connection_dict = {}
        self.reversed_dict = {}
        self.connection = False
        self.is_word = False

    def get_letter_node(self):
        """Set letter"""
        return self.letter

    def set_has_connection(self):
        """Set connection true"""
        self.connection = True

    def get_has_connection(self):
        """Get current state of connections"""
        return self.connection

    def create_connection(self, letter, node_connection):
        """
        Create a Connection between this node and the next node by a given letter and node.
        :param letter: string letter
        :param node_connection: Node
        """
        self.set_has_connection()
        self.connection_dict[letter] = node_connection

    def get_next_node(self, letter):
        """
        if letter in dictionary get the next node with the letter as key.
        :param letter: string Letter
        """
        if letter in self.connection_dict:
            return self.connection_dict[letter]

    def create_reversed_connection(self, letter, reversed_connection):
        """
        Creates a connection in de dictionary with the letter as key and node as Value
        :param letter: string Letter
        :param reversed_connection: Node
        """
        self.reversed_dict[letter] = reversed_connection

    def get_reversed_next_node(self, letter):
        """
        if letter in dictionary get the next reversed node with the letter as key.
        :param letter: Letter
        :return:
        """
        if letter in self.reversed_dict:
            return self.reversed_dict[letter]
        return None

    def set_is_word(self):
        """Set word true"""
        self.is_word = True

    def get_is_word(self):
        """Get boolean word"""
        return self.is_word

    def clear_redundant_reversed_dict(self):
        """Clear the redundant dictionary (after minimizing the nodes)"""
        self.reversed_dict.clear()



