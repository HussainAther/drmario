import pygame
import random

"""
Create the board. We want to use the blocks to fill up the board
with a starting setup and allow blocks to fall as they do.
"""

width = 10
height = 20
widthpixels = width*drpython.block.width
heightpixels = height*drpython.block.height
spawnpos = Pos(x=3, y=0)

class Board(object):
    """
    Define the class for the boards to include the block functions for
    spawning and falling.
    """
    def __init__(self):
        """
        Initialize the display and board for the game.
        """
        self.display = pygame.Surface((widthpixels, heightpixels))
        self.board = []
        for h in range(0, height):
            self.board.append([])
            for w in range(0, width):
                self.board[h].append(Block(w, h))
        self.brick = None

    def spawnbricks(self):
        """
        Spawn the bricks from the spawn position.
        """
        blocks = (
                self.block(spawnpos.x, spawnpos.y),
                self.block(spawnpos.x + 1, spawnpos.y),
        )
