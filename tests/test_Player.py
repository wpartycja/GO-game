from src.global_var import WHITE, BLACK
from src.Player import Player


def test_add_slaves():
    player = Player('Hubi', WHITE)
    group = {(1, 1), (4, 2), (1, 2), (2, 2), (3, 2)}
    player.add_slaves(group)
    assert player.slaves == 5


def test_points_for_territories():
    territories = [{(1, 1), (1, 2), (2, 2)}, {(4, 4), (4, 5), (5, 5)}, {(3, 3),
                   (3, 4)}]
    player = Player('Hubi', WHITE, None, 0, territories, 0)
    assert player.points_for_territories() == 8


def test_count_points():
    group = {(1, 1), (4, 2), (1, 2), (2, 2), (3, 2)}
    teritories = [{(1, 1), (1, 2), (2, 2)}, {(4, 4), (4, 5), (5, 5)}, {(3, 3),
                  (3, 4)}]
    player = Player('Roch', BLACK, group, 9, teritories)
    player.count_points()
    assert player.points == 17


def test_komi_points():
    player = Player('Hubi', WHITE)
    player.komi_points()
    assert player.points == 7.5
