import ex
import os
import pygame
import utils

"""
Coding the blocks is straightforward with a position and color
as well as status for cleared and falling for each one. Here we define
properties of the blocks themselves that can be used later for creating
vitamins.
"""

width = 20
height = 14

class Color(object):
    """
    Give the object a color depending on how it spawns
    and how it touches another block.
    """
    clear = 0
    blue = 1
    red = 2
    yellow = 3

class block(object):
    """
    Give properties to the block itself. It needs to fall
    at a certain speed and keep track of its color.
    """
    def __init__(self, x, y, color=None):
        """
        Initialize a cleared empty block.
        """
        self._x = x
        self._y = y
        self._color = Color.clear
        self._falling = False
        if color:
            self.setcolor(color)
    
   def loadimage(self, name):
        """
        Load the sprite from the img folder.
        """
        fullname = os.path.join("img", "megavitamin", name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error as message:
            print("Cannot load image:", name)
            raise SystemExit(message)
        image = image.convert()
        return image

    def setcolor(self, color):
        """
        Set the color of the block to another color.
        """
        if self._color != Color.clear:
            raise ex.InvalidOperation("Trying to set color on a colored block.")
        if color != Color.blue and color != Color.red and color != Color.yellow:
            raise ex.InvalidParameter("Invalid color value: {}".format(color))
        self._color = color

    def setimage(self, color, orient):
        """
        For a color and orientation, set and load the image.
        """
        return loadimage(str(orient) + str(color) + str.bmp))

    def clear(self):
        """
        Clear the color.
        """
        self._color = Color.clear

    def setfalling(self, falling):
        """
        Set a piece as falling.
        """
        self._falling = falling

    def __repr__(self):
        """
        Get the information about a block.
        """
        return "Block ({}, {}) color: {} falling: {}".format(self.x, self.y, self.color, self._falling)

    def isclear(self):
        """
        Is the block clear?
        """
        return self.color == Color.clear
 
    def isfalling(self):
        """
        Is the block falling?
        """
        return self._falling

    @property
    def x(self):
        """
        Return x-coordinate of the block.
        """
        return self._x

    @property
    def y(self):
        """
        Return y-coordinate of the block.
        """
        return self._y

    @property
    def xpixels(self):
        """
        Get the number of pixels on the screen in the
        x-direction.
        """
        return self.x*width
 
    @property
    def ypixels(self):
        """
        In the y-direction 
        """
        return self.y*height

    @property
    def pos(self):
        """
        Get the current block position.
        """
        return utils.Pos(self.x, self.y) 

    @property
    def color(self):
        """
        Get the block color.
        """
        return self._color
