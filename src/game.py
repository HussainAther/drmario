import pygame
import sys

from src.board import Board
from src.exceptions import BottomReached, InvalidOperation, InvalidParameter, OutOfBoard, PositionOccupied
from src.colors import black, blue, darkblue, darkgray, red, white, yellow
from src.utils import Pos

from pygame.constants import *

fps = 60
windowwith = 400
windowheight = 400

boardoffsetx = (windowwidth - drmario.board.widthpixels) / 2
boardoffsety = (windowheight - drmario.board.heightpixels) / 2
boardborder = 1

blockfallinterval = 300
speedfallmultiplier = 100.0

class Game(object):

    def __init__(self):
        self._board = Board()
        pygame.init()

        self._fpsClock = pygame.time.Clock()
        self._display = pygame.display.set_mode((windowwidth, windowheight), 0, 32)
        pygame.display.set_caption("Dr. Mario!")

        self._block_fall_timer = blockfallinterval

        self._speed = False

    def run(self):
        self.board.spawn_brick()

        while True:
            for event in pygame.event.get():
                self.process_event(event)

            self.update(self.fps_clock.get_time())

            self.display.fill(darkgray)

            pygame.draw.rect(self.display, darkblue,
                             (boardoffsetx-boardborder, boardoffsety-boardborder,
                              drmario.board.widthpixels+boardborder*2,
                              drmario.board.heightpixels+boardborder*2))
            board_display = self.board.render()
            self.display.blit(board_display, (boardoffsetx, boardoffsety))

            pygame.display.update()
            self.fps_clock.tick(fps)

    def update(self, delta):

        if self._block_fall_timer <= 0:
            try:
                self.board.move_brick("down")
            except (BottomReached, PositionOccupied):
                self.handle_collision()

            self._block_fall_timer = blockfallinterval
        else:
            if self._speed:
                delta *= speedfallmultiplier

            self._block_fall_timer -= delta

    def handle_collision(self):
        self.board.handle_collision()

    def process_event(self, event):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == K_RIGHT:
                direction = "left" if event.key == K_LEFT else "right"
                self.move_brick(direction)
            elif event.key == K_DOWN:
                self._speed = True
            elif event.key == K_SPACE:
                self.board.rotate_brick()
        elif event.type == KEYUP:
            if event.key == K_DOWN:
                self._speed = False

    def move_brick(self, direction):
        try:
            self.board.move_brick(direction)
        except (OutOfBoard, PositionOccupied):
            # Simply ignore those, the brick will not move at all
            pass

    @property
    def board(self):
        return self._board

    @property
    def display(self):
        return self._display

    @property
    def fps_clock(self):
        return self._fpsClock
