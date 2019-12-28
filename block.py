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
