import pygame
import sys

from src.board import Board
from src.exceptions import BottomReached, InvalidOperation, InvalidParameter, OutOfBoard, PositionOccupied
from src.colors import black, blue, darkblue, darkgray, red, white, yellow
from src.utils import Pos

from pygame.constants import *

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
        self.board = Board()
        pygame.init()

        self.fpsClock = pygame.time.Clock()
        self.display = pygame.display.setmode((windowwidth, windowheight), 0, 32)
        pygame.display.setcaption("Dr. Mario!")

        self.blockfalltimer = blockfallinterval

        self.speed = False

    def run(self):
        self.board.spawnbrick()

        while True:
            for event in pygame.event.get():
                self.processevent(event)

            self.update(self.fpsclock.gettime())

            self.display.fill(darkgray)

            pygame.draw.rect(self.display, darkblue,
                             (boardoffsetx-boardborder, boardoffsety-boardborder,
                              140+boardborder*2,
                              400+boardborder*2))
            boarddisplay = self.board.render()
            self.display.blit(boarddisplay, (boardoffsetx, boardoffsety))

            pygame.display.update()
            self.fpsclock.tick(fps)

    def update(self, delta):

        if self.blockfalltimer <= 0:
            try:
                self.board.movebrick("down")
            except (BottomReached, PositionOccupied):
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
            if event.key == KLEFT or event.key == KRIGHT:
                direction = "left" if event.key == KLEFT else "right"
                self.movebrick(direction)
            elif event.key == KDOWN:
                self.speed = True
            elif event.key == KSPACE:
                self.board.rotatebrick()
        elif event.type == KEYUP:
            if event.key == KDOWN:
                self.speed = False

    def movebrick(self, direction):
        try:
            self.board.movebrick(direction)
        except (OutOfBoard, PositionOccupied):
            # Simply ignore those, the brick will not move at all
            pass

    @property
    def board(self):
        return self.board

    @property
    def display(self):
        return self.display

    @property
    def fpsclock(self):
        return self.fpsClock
