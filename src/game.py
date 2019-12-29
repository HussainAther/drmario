import pygame
import sys

from pygame.constants import *
from src.board import Board
from src.exceptions import BottomReached, InvalidOperation, InvalidParameter, OutOfBoard, PositionOccupied
from src.colors import black, blue, darkblue, darkgray, red, white, yellow
from src.utils import Pos


fps = 60
windowwidth = 400
windowheight = 400

boardoffsetx = (windowwidth - 140) / 2
boardoffsety = (windowheight - 400) / 2
boardborder = 1

blockfallinterval = 300
speedfallmultiplier = 100.0

class Game(object):

    def __init__(self):
        self._board = Board()
        pygame.init()

        self.fpsClock = pygame.time.Clock()
        self._display = pygame.display.set_mode((windowwidth, windowheight), 0, 32)
        pygame.display.set_caption("Dr. Mario!")

        self.blockfalltimer = blockfallinterval

        self.speed = False

    def run(self):
        self._board.spawndublock()

        while True:
            for event in pygame.event.get():
                self.processevent(event)

            self.update(self.fpsclock.get_time())

            self._display.fill(darkgray)

            pygame.draw.rect(self._display, darkblue,
                             (boardoffsetx-boardborder, boardoffsety-boardborder,
                              140+boardborder*2,
                              400+boardborder*2))
            boarddisplay = self._board.render()
            self._display.blit(boarddisplay, (boardoffsetx, boardoffsety))

            pygame.display.update()
            self.fpsclock.tick(fps)

    def update(self, delta):

        if self.blockfalltimer <= 0:
            try:
                self._board.movedublock("down")
            except (BottomReached, PositionOccupied):
                self.handlecollision()

            self.blockfalltimer = blockfallinterval
        else:
            if self.speed:
                delta *= speedfallmultiplier

            self.blockfalltimer -= delta

    def handlecollision(self):
        self._board.handlecollision()

    def processevent(self, event):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == KLEFT or event.key == KRIGHT:
                direction = "left" if event.key == KLEFT else "right"
                self.movedublock(direction)
            elif event.key == KDOWN:
                self.speed = True
            elif event.key == KSPACE:
                self._board.rotatebrick()
        elif event.type == KEYUP:
            if event.key == KDOWN:
                self.speed = False

    def movedublock(self, direction):
        try:
            self._board.movedublock(direction)
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
    def fpsclock(self):
        return self.fpsClock
