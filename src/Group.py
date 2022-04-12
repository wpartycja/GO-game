from src.global_var import EMPTY


class Group:
    """
    Class Group. Contains attributes:
    :param board: board
    :type board: Board

    :param color: color of a stones in this group
    :type color: str

    :param groups: all groups of stones that belongs to color
    :type groups: list of sets of tuples
    """
    def __init__(self, board, color, groups=None):
        self._board = board
        self._color = color
        self._groups = [] if groups is None else groups

    def board(self):
        return self._board

    def color(self):
        return self._color

    def groups(self):
        return self._groups

    def set_groups(self, new_groups):
        self._groups = new_groups

    def create_group(self, coord):
        """
        creates new group of one stone
        and adds it to list of all groups
        """
        new_group = set()
        new_group.add(coord)
        self.groups().append(new_group)

    def add_to_group(self, coord):
        """
        adds one stone to its group
        """
        color = self.color()
        surroundings_dict = self.board().surroundings_dict(coord)
        for loc, value in surroundings_dict.items():
            if value == color:
                for group in self.groups():
                    if loc in group:
                        group.add(coord)

    def check_and_join_groups(self, coord):
        """
        if after given move two groups have joined
        this function does it
        """
        n = 0
        joined_group = set()
        all_groups = []
        for group in self.groups():
            if coord in group:
                n += 1
                if n == 1:
                    joined_group = group
                if n > 1:
                    joined_group = joined_group.union(group)
            else:
                all_groups.append(group)
        all_groups.append(joined_group)
        self.set_groups(all_groups)

    def settle_groups(self, coord):
        """
        makes needed groups changes after one move
        """
        color = self.color()
        surroundings = self.board().surroundings(coord)
        if color not in surroundings:
            self.create_group(coord)
        else:
            self.add_to_group(coord)
            self.check_and_join_groups(coord)

    def check_group_rimmed(self, group):
        """
        checks if given group is surrouded
        (don't have any empty space around)
        """
        for stone in group:
            surroundings = self.board().surroundings(stone)
            if EMPTY in surroundings:
                return False
        return True

    def kill_group(self, group):
        """
        removes whole group from the board
        """
        for stone in group:
            self.board().kill_stone(stone)
        self.groups().remove(group)

    def find_group_of_stone(self, coord):
        """
        find to which group belongs given stone
        (if it exist)
        """
        for group in self.groups():
            if coord in group:
                return group
        return None

    def delete_group(self, group):
        """
        deletes given group from list of all groups
        """
        for element in self.groups():
            if element == group:
                self.groups().remove(element)
