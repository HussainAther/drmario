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
        self.block = None

    def spawnblocks(self):
        """
        Spawn the blocks from the spawn position.
        """
        blocks = (
                self.block(spawnpos.x, spawnpos.y),
                self.block(spawnpos.x + 1, spawnpos.y),
        )

        for block in blocks:
            if not block.isclear(): # Block must be clear when they spawn.
                                    # If not, then you lose the game because you've
                                    # reached the top. 
                raise PositionOccupied("Block is not clear at spawn point.")
        colors = (random.randint(1, 3), # Choose the block colors.
                  random.randint(1, 3))
        for i in (0, 1): # Set the block colors.
            blocks[i].setcolor(colors[i])
 
    def moveblock(self, direction):
        """
        Move the block in a direction.
        """
        a, b = self.block.blocks
        directdict = {"down" : (0, 1),
                      "left" : (-1, 0),
                      "right" : (1, 0),
                      "up" : (0, -1)}
        (x, y) = directdict[direction]
        try: # Check if we've reached the bottom of the board.
            newa = self.block(a.x+x, a.y+y)
            newb = self.block(b.x+x, b.y+y)
        except (OutOfBoard, BottomReached) as e:
            raise e
        if (newa != b and not newa.isclear()) or (newb != a nd not newb.isclear()):
            raise PositionOccupied("Collision occured")
        acolor = a.color
        bcolor = b.color
        a.clear()
        b.clear()
        newa.setcolor(acolor) 
        newb.setcolor(bcolor)
        self.block.setblocks(newa, newb)

    def rotateblock(self):
        """
        Rotate the block. 
        """
        transform = (
            # vertical to horizontal
            ((Pos(1, 0), Pos(0, 1)),
             (Pos(0, 0), Pos(-1, 1))),
            # horizontal to vertical
            ((Pos(0, 0), Pos(-1, -1)),
             (Pos(0, 1), Pos(-1, 0)))
        )
 
