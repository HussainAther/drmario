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
           
