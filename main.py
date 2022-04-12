import pygame
from src.global_var import WHITE, BLACK, DIM
from src.Board import Board
from src.Player import Player
from src.Game import Game
from src.Group import Group
from src.BoardDisplay import BoardDisplay
import argparse


def create_parser():
    """
    creates parser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("black_player",
                        help='name of the player who plays with black stones')
    parser.add_argument("white_player",
                        help='name of the player who plays with white stones')
    parser.add_argument("-komi", action='store_true',
                        help='Sets 7.5 komi points for white player')
    return parser


def main():
    # data intitialization
    parser = create_parser()
    args = parser.parse_args()

    board = Board(DIM)
    b_groups = Group(board, BLACK)
    w_groups = Group(board, WHITE)
    player_1 = Player(args.black_player, BLACK, b_groups)
    player_2 = Player(args.white_player, WHITE, w_groups)
    players = (player_1, player_2)
    game = Game(board, players)
    display = BoardDisplay(board, game)

    # adds komi points to white player if user wants
    if args.komi:
        player_2.komi_points()

    # displaying empty game board
    display.board_base()

    # all gameplay
    display.gameplay()

    # counting points and displaying them on screen
    game.end_of_game_info()
    display.display_score()

    # closing the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()


main()
