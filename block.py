class Color(object):
    """
    Give the object a color depending on how it spawns
    and how it touches another block.
    """
    clear = 0
    blue = 1
    red = 2
    yellow = 3

class Block(object):
    """
    Give properties to the block itself. It needs to fall
    at a certain speed and keep track of its color.
    """
    def __init__(self, x, y, color=None):
        """
        Initialize a cleared empty block.
        """
        self.x = x
        self.y = y
        self.color = Color.CLEAR
        self.falling = False
        if color:
            self.setcolor(color)

    def setcolor(self, color):
        """
        Set the color of the block from clear to
        another color.
        """
        if self.color != Color.clear:
            raise InvalidOperation("Trying to set color on a colored block.")
        if color != Color.blue and color != color.red and color != color.yellow:
            raise InvalidParameter("Invalid color value: {}".format(color))

    def clear(self):
        """
        Clear the color.
        """
        self.color = Color.clear

    def setfalling(self, falling):
        """
        Set a piece as falling.
        """
        self.falling = falling

    def __repr__(self):
        """
        Get the information about a block.
        """
        return "Block ({}, {}) color: {} falling: {}".format(self.x, self.y, self.color, self.falling)
