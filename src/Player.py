class Player:
    def __init__(self, name, color, groups=None, slaves=0, territories=None,
                 points=0):
        """
        Class Player. Contains attributes:
        :param name: players name
        :type name: str

        :param color: color
        :type color:str

        :param groups: all its groups of stones
        :type groups: Group

        :param slaves: number of players' slaves
        "type slaves: int

        :param territories: all its territories
        "type territories: list

        :param points: points
        :type ponts: float
        """
        self._name = name
        self._color = color
        self._groups = groups
        self.slaves = 0 if slaves is None else slaves
        self.territories = [] if territories is None else territories
        self.points = points

    def name(self):
        return self._name

    def groups(self):
        return self._groups

    def color(self):
        return self._color

    def add_slaves(self, group):
        """
        adds number of slaves
        """
        self.slaves += len(group)

    def add_territory(self, space):
        self.territories += space

    def points_for_territories(self):
        """
        counts points for all territories
        """
        points = 0
        for group in self.territories:
            points += len(group)
        return points

    def count_points(self):
        """
        counts points in total
        """
        self.points += self.points_for_territories() + self.slaves

    def komi_points(self):
        """
        adds komi points
        """
        self.points = 7.5

