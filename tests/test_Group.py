from src.global_var import WHITE, BLACK, EMPTY
import numpy as np
from src.Board import Board
from src.Group import Group


def test_create_group():
    my_array = np.array([[' ', ' ', ' '],
                        [' ', 'b', ' '],
                        [' ', ' ', ' ']])
    board = Board(1, my_array)
    black_group = Group(board, BLACK)
    black_group.create_group((1, 1))
    assert black_group.groups() == [{(1, 1)}]


def test_add_to_group():
    board = Board(3)
    black_group = Group(board, BLACK)
    board.put_stone((1, 1), BLACK)
    black_group.create_group((1, 1))
    board.put_stone((1, 2), BLACK)
    black_group.add_to_group((1, 2))
    assert black_group.groups() == [{(1, 1), (1, 2)}]
    board.put_stone((1, 2), 'w')
    assert black_group.groups() == [{(1, 1), (1, 2)}]


def test_settle_groups():
    board = Board(3)
    black_group = Group(board, BLACK)
    board.put_stone((1, 1), BLACK)
    black_group.settle_groups((1, 1))
    assert black_group.groups() == [{(1, 1)}]
    board.put_stone((1, 2), BLACK)
    black_group.settle_groups((1, 2))
    assert black_group.groups() == [{(1, 1), (1, 2)}]
    board.put_stone((3, 1), BLACK)
    black_group.settle_groups((3, 1))
    assert black_group.groups() == [{(1, 1), (1, 2)}, {(3, 1)}]
    black_group.settle_groups((2, 1))
    assert black_group.groups() == [{(1, 1), (1, 2), (3, 1), (2, 1)}]


def test_check_and_join_groups_1():
    board = Board(3)
    groups = [{(1, 1), (1, 2), (2, 1)}, {(3, 1), (3, 2), (2, 1)}]
    black_group = Group(board, BLACK, groups)
    coord = (2, 1)
    black_group.check_and_join_groups(coord)
    for group in black_group.groups():
        if coord in group:
            searched_group = group
            break
    assert searched_group == {(1, 1), (1, 2), (2, 1), (3, 1), (3, 2)}
    assert len(black_group.groups()) == 1


def test_check_and_join_groups_2():
    board = Board(3)
    groups = [{(1, 1), (1, 2), (2, 1)}, {(3, 1), (3, 2), (2, 1)}, {(2, 3)}]
    black_group = Group(board, BLACK, groups)
    coord = (2, 1)
    black_group.check_and_join_groups(coord)
    for group in black_group.groups():
        if coord in group:
            searched_group = group
            break
    assert searched_group == {(1, 1), (1, 2), (2, 1), (3, 1), (3, 2)}
    assert len(black_group.groups()) == 2


def test_check_group_rimmed_1():
    board = Board(5)
    w_group = {(2, 2), (2, 3)}
    b_group = {(1, 2), (1, 3), (2, 4), (3, 3), (3, 2), (2, 1)}
    board.put_many_stones(w_group, WHITE)
    board.put_many_stones(b_group, BLACK)
    white_groups = Group(board, WHITE)
    black_groups = Group(board, BLACK)
    assert black_groups.check_group_rimmed(b_group) is False
    assert white_groups.check_group_rimmed(w_group) is True


def test_check_group_rimmed_2():
    board = Board(5)
    w_group = {(2, 2), (2, 3)}
    b_group = {(1, 2), (1, 3), (2, 4), (3, 3), (3, 2)}
    board.put_many_stones(w_group, WHITE)
    board.put_many_stones(b_group, BLACK)
    white_groups = Group(board, WHITE)
    black_groups = Group(board, BLACK)
    assert black_groups.check_group_rimmed(b_group) is False
    assert white_groups.check_group_rimmed(w_group) is False


def test_check_group_rimmed_3():
    board = Board(5)
    w_group = {(2, 2), (2, 3), (3, 3)}
    b_group = {(1, 2), (1, 3), (2, 4), (3, 4), (4, 3), (3, 3), (3, 2), (2, 1)}
    board.put_many_stones(w_group, WHITE)
    board.put_many_stones(b_group, BLACK)
    white_groups = Group(board, WHITE)
    black_groups = Group(board, BLACK)
    assert black_groups.check_group_rimmed(b_group) is False
    assert white_groups.check_group_rimmed(w_group) is True


def test_check_group_rimmed_corner():
    board = Board(5)
    w_group = {(1, 1)}
    b_group = {(1, 2), (2, 1)}
    board.put_many_stones(w_group, WHITE)
    board.put_many_stones(b_group, BLACK)
    white_groups = Group(board, WHITE)
    black_groups = Group(board, BLACK)
    assert black_groups.check_group_rimmed(b_group) is False
    assert white_groups.check_group_rimmed(w_group) is True


def test_check_group_rimmed_wall():
    board = Board(5)
    w_group = {(1, 2), (1, 3)}
    b_group = {(1, 1), (2, 2), (2, 3), (1, 4)}
    board.put_many_stones(w_group, WHITE)
    board.put_many_stones(b_group, BLACK)
    white_groups = Group(board, WHITE)
    black_groups = Group(board, BLACK)
    assert black_groups.check_group_rimmed(b_group) is False
    assert white_groups.check_group_rimmed(w_group) is True


def test_kill_group():
    board = Board(5)
    w_group = {(1, 2), (1, 3)}
    b_group = {(1, 1), (2, 2), (2, 3), (1, 4)}
    board.put_many_stones(w_group, WHITE)
    board.put_many_stones(b_group, BLACK)
    w_groups_list = [{(1, 2), (1, 3)}, {(3, 2)}]
    b_groups_list = [{(1, 1), (2, 2), (2, 3), (1, 4)}]
    white_groups = Group(board, WHITE, w_groups_list)
    black_groups = Group(board, BLACK, b_groups_list)
    if white_groups.check_group_rimmed(w_group) is True:
        white_groups.kill_group(w_group)
    assert len(w_groups_list) == 1
    assert board.board()[1][2] == EMPTY
    black_groups.kill_group(b_group)
    assert len(b_groups_list) == 0
    assert board.board()[1][1] == EMPTY


def test_find_group_of_stone():
    board = Board(5)
    w_groups_list = [{(1, 2), (1, 3)}, {(3, 2)}]
    b_groups_list = [{(1, 1), (2, 2)}, {(2, 3), (1, 4)}, {(5, 5), (4, 5),
                     (3, 5)}]
    white_groups = Group(board, WHITE, w_groups_list)
    black_groups = Group(board, BLACK, b_groups_list)
    assert black_groups.find_group_of_stone((1, 1)) == {(1, 1), (2, 2)}
    assert white_groups.find_group_of_stone((1, 3)) == {(1, 2), (1, 3)}
