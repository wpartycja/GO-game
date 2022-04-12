from src.global_var import PASS


class Game:
    def __init__(self, board, players):
        """
        Class Game. Contains attributes:
        :param board: game board
        "type board: Board

        :param players: two player that take part in game
        :type players: list
        """
        self._board = board
        self._players = players
        self.turn = players[0]

    def board(self):
        return self._board

    def players(self):
        return self._players

    def opponent(self, player):
        """
        returns the opponent of given player
        """
        for person in self.players():
            if player.color() == person.color():
                return self.players()[1]
            else:
                return self.players()[0]

    def count_points(self):
        """
        counts points for both players
        """
        for player in self.players():
            player.count_points()

    def move_possibility(self, player, coord):
        """
        returns True is move to given place is possible
        in other case returns False
        """
        color = player.color()
        if coord == PASS:
            return True
        if (not self.board().check_coord_existance(coord)
                or not self.board().check_free_space(coord)
                or not self.board().check_move_if_suicide(coord, color)):
            return False
        else:
            return True

    def one_player_move(self, player, coord):
        """
        makes full one player move and controls changes
        in both players, both groups and on the board
        """
        self.board().put_stone(coord, player.color())
        player.groups().settle_groups(coord)
        enemy = self.board().find_enemy(player.color())
        surroundings_dict = self.board().surroundings_dict(coord)
        opponent = self.opponent(player)
        for loc, value in surroundings_dict.items():
            if value == enemy:
                checked_group = opponent.groups().find_group_of_stone(loc)
                if opponent.groups().check_group_rimmed(checked_group) is True:
                    opponent.groups().kill_group(checked_group)
                    player.add_slaves(checked_group)
                    opponent.groups().delete_group(checked_group)

    def winner(self):
        """
        return the winner
        """
        if self.players()[0].points > self.players()[1].points:
            return self.players()[0].name()
        elif self.players()[0].points < self.players()[1].points:
            return self.players()[1].name()
        else:
            None

    def winner_info(self):
        """
        returns string information about the game results
        """
        if self.winner():
            winner = self.winner()
            results = f'The winner is {winner}! Congratulations!'
        else:
            results = 'The game ended with a draw'
        return results

    def end_of_game_info(self):
        """
        counts everything at the end of game and return
        string information about results
        """
        self.set_territories()
        self.count_points()
        results = self.winner_info()
        return results

    def set_territories(self):
        """
        counts all territories and sets it to proper player
        """
        player = self.players()[0]
        opponent = self.opponent(player)
        all_territories = self.board().all_territories()
        for territory in all_territories:
            for field in territory:
                surroundings = self.board().surroundings(field)
                if player.color() in surroundings:
                    player.territories.append(territory)
                    break
                if opponent.color() in surroundings:
                    opponent.territories.append(territory)
                    break

    def change_turn(self):
        """
        changes turn
        """
        if self.turn == self.players()[0]:
            self.turn = self.players()[1]
        else:
            self.turn = self.players()[0]
        return self.turn
