import numpy as np
from src.global_var import WALL, EMPTY, BLACK, WHITE


class Board:
    """
    Class Board. Contains attributes:
    :param dim: board dimension
    :type dim: int

    :param array: setted board
    :type array: 2-dimensional array
    """
    def __init__(self, dim, array=None):
        self._dim = dim
        if array is None:
            self._board = self.make_board(dim)
        else:
            self._board = array

    def dim(self):
        return self._dim

    def board(self):
        return self._board

    # general Board methods, used in gameplay to modify the board with stones

    def make_board(self, dim):
        """
        Creates starting game board (so it is empty)
        with frame around it to help in work with surroundings
        """
        board = np.full((dim+2, dim+2), EMPTY, dtype='U')
        board[:, [0, dim+1]] = WALL
        board[[0, dim+1], :] = WALL
        return board

    def surroundings(self, coord):
        """
        return values which surround given path
        """
        x, y = coord
        upper = self.board()[x-1][y]
        lower = self.board()[x+1][y]
        right = self.board()[x][y+1]
        left = self.board()[x][y-1]
        return (upper, lower, right, left)

    def surroundings_dict(self, coord):
        """
        returns dict {coordinates : value} of place
        which surrounds given path
        """
        x, y = coord
        upper, lower, right, left = self.surroundings(coord)
        surroundings_dict = {
            (x-1, y): upper,
            (x+1, y): lower,
            (x, y+1): right,
            (x, y-1): left
        }
        return surroundings_dict

    def find_enemy(self, color):
        """
        finds enemy of given color
        """
        enemy = WHITE if color == BLACK else BLACK
        return enemy

    def check_coord_existance(self, coord):
        """
        checks if given coordinates exist
        """
        x, y = coord
        if x in range(1, self.dim()+1) and y in range(1, self.dim()+1):
            return True
        else:
            return False

    def check_free_space(self, coord):
        """
        checks if given place isn't occupied
        """
        x, y = coord
        if self.board()[x][y] != EMPTY:
            return False
        else:
            return True

    def check_move_if_suicide(self, coord, color):
        """
        check if this move won't imply sucide
        """
        surroudings = self.surroundings(coord)
        enemy = self.find_enemy(color)
        borders = (enemy, WALL)
        if set(surroudings).issubset(borders):
            return False
        else:
            return True

    def put_stone(self, coord, color):
        """
        puts stone on a board
        """
        x, y = coord
        self.board()[x][y] = color

    def put_many_stones(self, list_of_coord, color):
        """
        puts many stones on a board
        this function is used in unit tests
        """
        for x, y in list_of_coord:
            self.board()[x][y] = color

    def kill_stone(self, coord):
        """
        removes stone from a board
        """
        x, y = coord
        self.board()[x][y] = EMPTY

    # methods needed to count territories
    # it's needed at the end of a game to count points

    def all_groups_with_repet(self):
        """
        find's generally all groups of empty paths,
        but here one path can be in two groups
        - next function fixes is
        """
        groups = []
        for x in range(1, self.dim()+1):
            for y in range(1, self.dim()+1):
                field = self.board()[x][y]
                if field == EMPTY:
                    field_coord = (x, y)
                    minor = self.make_group_regard_one_field(field_coord)
                    if len(groups) != 0:
                        for i in range(len(groups)):
                            if field_coord in groups[i]:
                                groups[i] = groups[i].union(minor)
                                minor = None
                                break
                    if minor:
                        groups.append(minor)
        return groups

    def make_group_regard_one_field(self, coord):
        """
        takes one path and creates a group
        with all empty paths around it
        """
        territory = set()
        territory.add(coord)
        surroundings_dict = self.surroundings_dict(coord)
        for loc, value in surroundings_dict.items():
            if value == EMPTY:
                territory.add(loc)
        return territory

    def check_if_territory(self, group):
        """
        checks if given group is a territory,
        if it has both colors in its surroundings - it isn't
        """
        both_colors = {WHITE, BLACK}
        group_surroundings = set()
        for field in group:
            surroundings = self.surroundings(field)
            group_surroundings = group_surroundings.union(set(surroundings))
        if both_colors.issubset(group_surroundings):
            return False
        else:
            return True

    def all_territories(self):
        """
        function creates a list of all groups, join them
        if one path is in two groups, and returns groups,
        which are real territories
        """
        groups = self.all_groups_with_repet()
        new_groups = []
        for i in range(len(groups)):
            new_set = groups[i]
            for j in range(len(groups)):
                if len(groups[i].intersection(groups[j])) != 0:
                    new_set = groups[j].union(new_set)
            new_groups.append(new_set)
        territories = []
        for group in new_groups:
            if self.check_if_territory(group):
                territories.append(group)
        return territories
