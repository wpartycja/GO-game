from src.Board import Board
from src.global_var import WHITE, BLACK, EMPTY
import numpy as np


def test_make_board():
    board = Board(1)
    assert board.board().tolist() == [[' ', ' ', ' '],
                                      [' ', '*', ' '],
                                      [' ', ' ', ' ']]
    assert board.dim() == 1


def test_surroundings_and_dict():
    my_array = np.array([[' ', ' ', ' ', ' ', ' '],
                        [' ', '*', 'b', '*', ' '],
                        [' ', 'w', '*', 'w', ' '],
                        [' ', '*', 'w', '*', ' '],
                        [' ', ' ', ' ', ' ', ' ']])
    board = Board(3, my_array)
    coord = (2, 2)
    assert board.surroundings(coord) == ('b', 'w', 'w', 'w')
    assert board.surroundings_dict(coord) == {
        (1, 2): 'b',
        (3, 2): 'w',
        (2, 3): 'w',
        (2, 1): 'w'}


def test_find_enemy():
    board = Board(3)
    color = WHITE
    assert board.find_enemy(color) == BLACK


def test_check_free_space_true():
    board = Board(3)
    coord = (3, 1)
    assert board.check_free_space(coord) is True


def test_check_free_space_false():
    my_array = np.array([[' ', ' ', ' ', ' ', ' '],
                        [' ', '*', 'b', '*', ' '],
                        [' ', 'w', '*', 'w', ' '],
                        [' ', '*', 'w', '*', ' '],
                        [' ', ' ', ' ', ' ', ' ']])
    board = Board(3, my_array)
    coord = (1, 2)
    assert board.check_free_space(coord) is False


def test_check_move_if_suicide_false():
    my_array = np.array([[' ', ' ', ' ', ' ', ' '],
                        [' ', '*', 'w', '*', ' '],
                        [' ', 'w', '*', 'w', ' '],
                        [' ', '*', 'w', '*', ' '],
                        [' ', ' ', ' ', ' ', ' ']])
    board = Board(3, my_array)
    assert board.check_move_if_suicide((2, 2), BLACK) is False


def test_check_move_if_suicide_false_corner():
    my_array = np.array([[' ', ' ', ' ', ' ', ' '],
                        [' ', '*', 'w', '*', ' '],
                        [' ', 'w', '*', 'w', ' '],
                        [' ', '*', 'w', '*', ' '],
                        [' ', ' ', ' ', ' ', ' ']])
    board = Board(3, my_array)
    assert board.check_move_if_suicide((1, 3), BLACK) is False


def test_check_move_if_suicide_false_wall():
    my_array = np.array([[' ', ' ', ' ', ' ', ' '],
                        [' ', 'w', '*', 'w', ' '],
                        [' ', 'w', 'w', 'w', ' '],
                        [' ', '*', 'w', '*', ' '],
                        [' ', ' ', ' ', ' ', ' ']])
    board = Board(3, my_array)
    assert board.check_move_if_suicide((1, 2), BLACK) is False


def test_check_move_if_suicide_true_1():
    my_array = np.array([[' ', ' ', ' ', ' ', ' '],
                        [' ', '*', 'b', '*', ' '],
                        [' ', 'w', '*', 'w', ' '],
                        [' ', '*', 'w', '*', ' '],
                        [' ', ' ', ' ', ' ', ' ']])
    board = Board(3, my_array)
    assert board.check_move_if_suicide((2, 2), BLACK) is True


def test_check_move_if_suicide_true_2():
    my_array = np.array([[' ', ' ', ' ', ' ', ' '],
                        [' ', '*', 'w', '*', ' '],
                        [' ', 'w', '*', 'w', ' '],
                        [' ', '*', '*', '*', ' '],
                        [' ', ' ', ' ', ' ', ' ']])
    board = Board(3, my_array)
    assert board.check_move_if_suicide((2, 2), BLACK) is True


def test_put_stone():
    my_array = np.array([[' ', ' ', ' ', ' ', ' '],
                        [' ', '*', 'w', '*', ' '],
                        [' ', 'w', '*', 'w', ' '],
                        [' ', '*', 'w', '*', ' '],
                        [' ', ' ', ' ', ' ', ' ']])
    board = Board(3, my_array)
    coord = (1, 1)
    x, y = coord
    board.put_stone(coord, WHITE)
    assert board.board()[x][y] == WHITE


def test_put_many_stones():
    board = Board(5)
    coord_to_put = {(1, 1), (1, 2), (1, 3), (4, 5)}
    board.put_many_stones(coord_to_put, WHITE)
    assert board.board()[1][1] == WHITE
    assert board.board()[4][5] == WHITE
    assert board.board()[2][3] == EMPTY


def test_check_coord_existance_true():
    board = Board(3)
    coord = (2, 3)
    assert board.check_coord_existance(coord) is True


def test_check_coord_existance_false():
    board = Board(3)
    coord = (1, 4)
    assert board.check_coord_existance(coord) is False


def test_kill_stone():
    board = Board(4)
    board.put_stone((2, 4), WHITE)
    assert board.board()[2][4] == WHITE
    board.kill_stone((2, 4))
    assert board.board()[2][4] == EMPTY


def test_make_group_regard_one_field():
    my_array = np.array([[' ', ' ', ' ', ' ', ' '],
                        [' ', 'w', '*', '*', ' '],
                        [' ', 'w', 'w', '*', ' '],
                        [' ', 'w', 'w', '*', ' '],
                        [' ', ' ', ' ', ' ', ' ']])
    board = Board(3, my_array)
    assert board.make_group_regard_one_field((1, 3)) == {(1, 2),
                                                         (1, 3), (2, 3)}
    assert board.make_group_regard_one_field((3, 3)) == {(3, 3), (2, 3)}


def test_group_empty_spaces():
    my_array = np.array([[' ', ' ', ' ', ' ', ' '],
                        [' ', 'w', '*', '*', ' '],
                        [' ', 'w', 'w', '*', ' '],
                        [' ', 'w', 'w', '*', ' '],
                        [' ', ' ', ' ', ' ', ' ']])
    board = Board(3, my_array)
    assert board.all_territories()[0] == {(1, 2), (1, 3), (2, 3), (3, 3)}


def test_check_if_territory():
    my_array = np.array([[' ', ' ', ' ', ' ', ' '],
                        [' ', 'w', '*', '*', ' '],
                        [' ', 'w', 'w', '*', ' '],
                        [' ', '*', 'b', '*', ' '],
                        [' ', ' ', ' ', ' ', ' ']])
    board = Board(3, my_array)
    assert len(board.all_territories()) == 0


def test_check_if_territory_1():
    my_array = np.array([[' ', ' ', ' ', ' ', ' '],
                        [' ', 'w', '*', '*', ' '],
                        [' ', '*', '*', '*', ' '],
                        [' ', '*', 'b', '*', ' '],
                        [' ', ' ', ' ', ' ', ' ']])
    board = Board(3, my_array)
    group = {(1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 3)}
    assert board.check_if_territory(group) is False


def test_check_if_territory_2():
    my_array = np.array([[' ', ' ', ' ', ' ', ' ', ' '],
                        [' ', 'w', '*', '*', '*', ' '],
                        [' ', '*', '*', '*', 'b', ' '],
                        [' ', '*', 'b', '*', '*', ' '],
                        [' ', 'b', '*', 'b', '*', ' '],
                        [' ', ' ', ' ', ' ', ' ', ' ']])
    board = Board(3, my_array)
    group_n = {(1, 2), (1, 3), (1, 4), (2, 1), (2, 2), (2, 3), (3, 1), (3, 3),
               (3, 4), (4, 4)}
    assert board.check_if_territory(group_n) is False
    group_y = {(4, 2)}
    assert board.check_if_territory(group_y) is True
