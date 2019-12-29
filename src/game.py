import board
import ex
import pygame
import sys

from board import Board
from pygame.constants import KEYUP, KEYDOWN, K_DOWN, K_LEFT, K_RIGHT, K_SPACE, K_UP, QUIT 
from colors import black, blue, darkblue, darkgray, red, white, yellow
from utils import Pos

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
        self.board.spawndublock()

        while True:
            for event in pygame.event.get():
                self.processevent(event)

            self.update(self.fpsclock.get_time())

            self._display.fill(darkgray)

            pygame.draw.rect(self._display, darkblue,
                             (boardoffsetx-boardborder, boardoffsety-boardborder,
                              140+boardborder*2,
                              400+boardborder*2))
            boarddisplay = self.board.render()
            self._display.blit(boarddisplay, (boardoffsetx, boardoffsety))

            pygame.display.update()
            self.fpsclock.tick(fps)

    def update(self, delta):

        if self.blockfalltimer <= 0:
            try:
                self.board.movedublock("down")
            except (ex.BottomReached, ex.PositionOccupied):
                self.handlecollision()

            self.blockfalltimer = blockfallinterval
        else:
            if self.speed:
                delta *= speedfallmultiplier

            self.blockfalltimer -= delta

    def handlecollision(self):
        self.board.handlecollision()

    def processevent(self, event):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == K_RIGHT:
                direction = "left" if event.key == K_LEFT else "right"
                self.movedublock(direction)
            elif event.key == K_DOWN:
                self.speed = True
            elif event.key == K_SPACE:
                self.board.rotatedublock()
        elif event.type == KEYUP:
            if event.key == K_DOWN:
                self.speed = False

    def movedublock(self, direction):
        try:
            self.board.movedublock(direction)
        except (ex.OutOfBoard, ex.PositionOccupied):
            # Simply ignore those, the dublock will not move at all.
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
