import block
import dublock
import ex
import random

from pygame import Surface
from block import block, Color
from colors import black, blue, darkblue, darkgray, red, white, yellow
from dublock import dublock
from utils import Pos

"""
Create the board. We want to use the blocks to fill up the board
with a starting setup and allow blocks to fall as they do.
"""
width = 10
height = 20
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
        self._display = Surface((140, 300))
        self._board = []
        for h in range(0, height):
            self._board.append([])
            for w in range(0, width):
                self._board[h].append(block(w, h))
        self._dublock = None

    def spawndublock(self):
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
                raise ex.PositionOccupied("Block is not clear at spawn point.")
        colors = (random.randint(1, 3), # Choose the block colors.
                  random.randint(1, 3))
        for i in (0, 1): # Set the block colors.
            blocks[i].setcolor(colors[i])
        self._dublock = dublock(blocks)
          
    def movedublock(self, direction):
        """
        Move the block in a direction.
        """
        a, b = self.dublock.blocks # Get the two individuals blocks of the 
                                   # dublock.
        directdict = {"down" : (0, 1), # Get the direction and how to move the block.
                      "left" : (-1, 0),
                      "right" : (1, 0)}
        (x, y) = directdict[direction]
        try: # Check if we've reached the bottom of the board.
            newa = self.block(a.x+x, a.y+y)
            newb = self.block(b.x+x, b.y+y)
        except (ex.OutOfBoard, ex.BottomReached) as e:
            raise e
        if (newa != b and not newa.isclear()) or (newb != a and not newb.isclear()):
            raise ex.PositionOccupied("Collision occured")
        acolor = a.color
        bcolor = b.color
        a.clear()
        b.clear()
        newa.setcolor(acolor) 
        newb.setcolor(bcolor)
        self.dublock.setblocks(newa, newb)

    def rotatedublock(self):
        """
        Rotate the dublock. 
        """
        transform = (
            # vertical to horizontal
            ((Pos(1, 0), Pos(0, 1)),
             (Pos(0, 0), Pos(-1, 1))),
            # horizontal to vertical
            ((Pos(0, 0), Pos(-1, -1)),
             (Pos(0, 1), Pos(-1, 0)))
        )
        section = int(self.dublock.ishorizontal())
        origin = self.dublock.blocks
        for offset in transform[section]:
            try:
                i = not section
                j = not i
                newblocks = (
                    self.block(origin[i].x + offset[i].x, origin[i].y + offset[i].y),
                    self.block(origin[j].x + offset[j].x, origin[j].y + offset[j].y),
                ) 
                # Don't overwrite blocks.
#                for b in newblocks:
#                    if not (b.isclear() and b.pos != origin[0].pos and b.pos != origin[1].pos):
#                        raise ex.InvalidOperation("New block is occupied.")

                if self.dublock.ishorizontal():
                    # standard colors
                    colors = (origin[0].color, origin[1].color)
                else:
                    # swap colors
                    colors = (origin[1].color, origin[0].color)

                for k in range(0, 2):
                    origin[k].clear()
                    newblocks[k].setcolor(colors[k])
                self.dublock.setblocks(*newblocks)
            except (ex.OutOfBoard, ex.InvalidOperation) as e:
                continue
            else:
                break

    def checkmatch(self, blocks):
        """
        If there's a match, make them disppear.
        """
        match = False
        for block in blocks:
            if block.isclear():
                continue # If the block is cleared, we need to see what 
                         # it matched to.
            # Check the horizontal and vertical directions to get the matches.
            horizontal = set(self.getmatchesindirection(block, 1, 0) + self.getmatchesindirection(block, -1, 0))
            vertical = set(self.getmatchesindirection(block, 0, 1) + self.getmatchesindirection(block, 0, 1))
            for matches in (horizontal, vertical):
                # For the matches, check if they're 3 or more blocks.
                # If they are, they disappear.
                if len(matches) >= 3:
                    match = True
                    for nextblock in matches:
                        nextblock.clear()
                    block.clear()
        return match

    def getmatchesindirection(self, block, xdir, ydir):
        """
        Get the matches in the x and y directions. 
        """
        matches = []
        x = block.x + xdir
        y = block.y + ydir
        while True:
            try:
                nextblock = self.block(x, y)
            except:
                break
            if nextblock.isclear():
                break
            matches.append(nextblock)
            x += xdir
            y += ydir
        return matches 

    def checkblocksinair(self):
        """
        If one part of a block is cleared, the second part should drop.
        This function runs on all the blocks that have been changed. It
        checks each block one by one.
        """
        changed = True
        while changed:
            changed = False
            for x in range(0, width):
                for y in range(0, height):
                    block = self.block(x, y)
                    blockchanged = self.checkblockinair(block)
                    if blockchanged:
                        changed = True

    def checkblockinair(self, block):
        """
        Check a single block in the air.
        """
        if block.isclear() or block.isfalling():
            return False
        try:
            bottomblock = self.block(block.x, block.y+1)
        except ex.BottomReached as e:
            return False
        rightblock = None
        leftblock = None
        try:
            rightblock = self.block(block.x+1, block.y+1)
        except ex.OutOfBoard as e:
            pass
        try:
            leftblock = self.block(block.x-1, block.y-1)
        except ex.OutOfBoard as e:
            pass    
        if (bottomblock.isclear() or bottomblock.isfalling()) and \
             (not rightblock or rightblock.isclear()) and \
             (not leftblock or leftblock.isclear()):
            block.setfalling(True)
            return True
        return False

    def getfallingblocks(self):
        """
        Get the blocks that are falling by checking their
        .isfalling() status.
        """
        return [block for rows in reversed(self._board)
                for block in rows
                if block.isfalling()]

    def handlefallingblocks(self):
        """
        Check the falling blocks.
        """
        blocks = self.getfallingblocks()
        if not blocks:
            return []
        blocksatbottom = []
        for block in blocks:
            try:
                bottomblock = self.block(block.x, block.y+1)
            except ex.BottomReached:
                blocksatbottom.append(block)
                block.setfalling(False)
                continue

            if bottomblock.isclear():
                bottomblock.setcolor(block.color)
                bottomblock.setfalling(True)
                block.clear()
                block.setfalling(False)
            else:
                blocksatbottom.append(block)
                block.setfalling(False)
        return blocksatbottom

    def handlecollision(self):
        """
        Check the collisions for matches.
        """
        self.checkmatch(self._dublock.blocks)
        while True:
            self.checkblocksinair()
            blocks = []
            while self.getfallingblocks():
                blocks.extend(self.handlefallingblocks())
            if not self.checkmatch(blocks):
                break
        self.spawndublock()

    def render(self):
        self._display.fill(black)
        for h in range(0, height):
            for w in range(0, width):
                self.renderblock(self._display, self.block(w, h))
        return self._display

    def renderblock(self, display, block):
        if block.color == Color.clear:
            return
        elif block.color == Color.red:
            color = red
        elif block.color == Color.blue:
            color = blue
        elif block.color == Color.yellow:
            color = yellow
        else:
            raise ex.InvalidParameter("Block has invalid color: {}".format(block.color))

        display.fill(color,
                     (block.xpixels,
                      block.ypixels,
                      14,
                      20))

    def block(self, x, y):
        if x < 0 or y < 0:
            raise ex.OutOfBoard("Trying to get block at negative position")

        if y <= len(self._board)-1:
            if x <= len(self._board[y])-1:
                return self._board[y][x]
            else:
                raise ex.OutOfBoard("Position ({}, {}) not on board".format(x, y))
        else:
            raise ex.BottomReached("Bottom reached by block")

    @property
    def dublock(self):
        return self._dublock

    @property
    def display(self):
        return self._display 
