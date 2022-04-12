from src.Board import Board
from src.Player import Player
from src.Game import Game
from src.global_var import BLACK, WHITE
import numpy as np


def test_opponent():
    board = Board(3)
    player1 = Player('Patrycja', BLACK)
    player2 = Player('Hubert', WHITE)
    players = (player1, player2)
    game = Game(board, players)
    assert game.opponent(player1) == player2


def test_winner():
    board = Board(3)
    player1 = Player('Patrycja', BLACK, None, 0, None, 90)
    player2 = Player('Hubert', WHITE, None, 0, None, 89)
    players = (player1, player2)
    game = Game(board, players)
    assert game.winner() == 'Patrycja'
    player2 = Player('Hubert', WHITE, None, 0, None, 90)
    players = (player1, player2)
    game = Game(board, players)
    assert game.winner() is None


def test_winner_info():
    board = Board(3)
    player1 = Player('Patrycja', BLACK, None, 0, None, 90)
    player2 = Player('Hubert', WHITE, None, 0, None, 91)
    players = (player1, player2)
    game = Game(board, players)
    assert game.winner_info() == 'The winner is Hubert! Congratulations!'


def test_set_territories():
    my_array = np.array([[' ', ' ', ' ', ' ', ' '],
                        [' ', '*', 'b', 'w', ' '],
                        [' ', 'b', 'w', '*', ' '],
                        [' ', 'w', 'w', '*', ' '],
                        [' ', ' ', ' ', ' ', ' ']])
    board = Board(3, my_array)
    player1 = Player('Patrycja', BLACK)
    player2 = Player('Hubert', WHITE)
    players = (player1, player2)
    game = Game(board, players)
    game.set_territories()
    assert player1.territories[0] == {(1, 1)}
    assert player2.territories[0] == {(2, 3), (3, 3)}


def test_set_territories_1():
    my_array = np.array([[' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', '*', 'w', 'b', 'b', '*', ' '],
                        [' ', 'w', '*', 'w', '*', '*', ' '],
                        [' ', '*', 'w', '*', '*', '*', ' '],
                        [' ', 'w', '*', '*', '*', '*', ' '],
                        [' ', '*', '*', '*', '*', '*', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ']])
    board = Board(5, my_array)
    player1 = Player('Patrycja', BLACK)
    player2 = Player('Hubert', WHITE)
    players = (player1, player2)
    game = Game(board, players)
    game.set_territories()
    assert player2.territories[0] == {(1, 1)}


def test_set_teritories_2():
    my_array = np.array([[' ', ' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', '*', 'w', 'b', 'b', '*', ' '],
                        [' ', 'w', '*', 'w', '*', '*', ' '],
                        [' ', 'w', '*', 'w', '*', '*', ' '],
                        [' ', 'w', '*', '*', 'w', '*', ' '],
                        [' ', 'w', '*', '*', '*', 'w', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ', ' ']])
    board = Board(5, my_array)
    player1 = Player('Patrycja', BLACK)
    player2 = Player('Hubert', WHITE)
    players = (player1, player2)
    game = Game(board, players)
    game.set_territories()
    assert player2.territories[1] == {(2, 2), (3, 2), (4, 2), (4, 3), (5, 2),
                                      (5, 3), (5, 4)}
