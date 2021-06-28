

class TileObject:
    def __init__(self, row, column):
        """
        Class Tile objects are there to hold the letters of the matrix, hold the start positions, one letter value,
        and one validate letter value. the Validate letter is used to determine is a board thats going to be placed
        is vallid following the rules.  it holds 6 varibles two string for letters, one for bonus, one for start point,
        and one for the neighbor Tile objects Up, Down, Left, Right.
        :param row: current row
        :param column: current column
        """
        self.neighbors = None  # [None, None, None, None] Boven, Onder, Links, Rechts.
        self.position = [row, column]
        self.bonus = None
        self.letter = ""
        self.validate_letter = ""
        self.start_point = False

    def set_start_point(self):
        """
        Set Start point True
        """
        self.start_point = True

    def get_start_point(self):
        """
        Get Start point
        :return: start point
        """
        return self.start_point

    def set_neighbor_connections(self, list):
        """
        Set neighbor list
        :param list: list of tile objects
        """
        self.neighbors = list

    def get_neighbor_connections(self):
        """
        Get neighbor list
        :return: neighbor list
        """
        return self.neighbors

    def set_bonus(self, bonus):
        """
        Set Bonus
        :param bonus: bonus
        """
        self.bonus = bonus

    def get_bonus(self):
        """
        Get Bonus
        :return: bonus
        """
        return self.bonus

    def get_position(self):
        """
        Get Position
        :return: Position
        """
        return self.position

    def set_letter(self, letter):
        """
        Set_letter, if letter is not none set start point True
        :param letter: letter
        """
        if letter != "":
            self.set_start_point()
        self.letter = letter

    def get_letter(self):
        """
        Get Letter
        :return: Letter
        """
        return self.letter

    def set_validate_letter(self, validate_letter):
        """
        Set validate letter
        :param validate_letter: string letter
        """
        self.validate_letter = validate_letter

    def get_validate_letter(self):
        """
        Get validate letter
        :return: validate letter
        """
        return self.validate_letter