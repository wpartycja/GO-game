import pygame
from src.global_var import WHITE, BLACK, DIM, PASS
import math


class BoardDisplay:
    def __init__(self, board, game):
        """
        Class BoardDisplay. Contains attributes:
        :param board: game board
        :type board: Board

        :param game: game object
        :type game: Game
        """
        self._board = board
        self._white = (255, 255, 255)
        self._black = (0, 0, 0)
        self._size = 593
        self._game = game
        self._img = pygame.image.load('images/goban-19x19.png')
        self._surface = self.set_surface()

    def game(self):
        return self._game

    def board(self):
        return self._board

    def surface(self):
        return self._surface

    def white(self):
        return self._white

    def black(self):
        return self._black

    def size(self):
        return self._size

    def img(self):
        return self._img

    def set_surface(self):
        surface = pygame.display.set_mode((self.size(), self.size()))
        return surface

    def board_base(self):
        """
        displayes the base of a board
        """
        pygame.init()
        pygame.display.set_caption('GO')
        self.surface().fill(self.white())
        self.surface().blit(self.img(), (0, 0))
        pygame.display.update()

    def update_board(self):
        """
        updates the situation that is on a board
        """
        self.board_base()
        size = self.size()
        for x in range(1, DIM+1):
            for y in range(1, DIM+1):
                if self.board().board()[x][y] == BLACK:
                    pygame.draw.circle(self.surface(), self.black(),
                                       ((y-0.5)*(size/DIM),
                                       (x-0.5)*(size/DIM)),
                                       (math.floor(size/DIM/2)))
                    pygame.display.update()
                elif self.board().board()[x][y] == WHITE:
                    pygame.draw.circle(self.surface(), self.white(),
                                       ((y-0.5)*(size/DIM),
                                       (x-0.5)*(size/DIM)),
                                       (math.floor(size/DIM/2)))
                    pygame.display.update()

    def make_move(self, player):
        """
        takes cooordinates of the place where user clicked
        and returns it
        """
        size = self.size()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return PASS
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x = int(math.ceil(((event.pos[1]) / (size/DIM))))
                        y = int(math.ceil(((event.pos[0]) / (size/DIM))))
                        coord = (x, y)
                        return coord

    def display_score(self):
        """
        displays game results
        """
        text_color = (104, 12, 33)
        font = pygame.font.Font('freesansbold.ttf', 26)
        result = self.game().end_of_game_info()
        text = font.render(result, True, text_color)
        textRect = text.get_rect()
        textRect.center = (self.size()/2, self.size()/2-15)
        self.surface().blit(text, textRect)

    def gameplay(self):
        """
        holds whole gameplay, reads players moves,
        until both players won't pass
        """
        prev_move = None
        while True:
            coord = (0, 0)
            while not self.game().move_possibility(self.game().turn, coord):
                coord = self.make_move(self.game().turn)
            if coord == PASS:
                if prev_move == PASS:
                    while True:
                        self.display_score()
                        pygame.display.update()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                quit()
                prev_move = PASS
                self.game().change_turn()
                continue
            prev_move = coord
            self.game().one_player_move(self.game().turn, coord)
            self.update_board()
            pygame.display.update()
            self.game().change_turn()
