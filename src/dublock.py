class dublock(object):
    """
    A dublock is a block made of 2 square parts, blocka and blockb.
    This is the megavitamin of Dr. Mario that the player controls.
    """
    def __init__(self, blocks):
        self._blocks = blocks
        self._images = None 

    def getorient(self):
        """
        Get the orientation (from the list o) of each block in the dublock (megavitamin).
        This is used for sprite purposes.
        """
        a, b = self.blocks # Get the two individuals blocks of the 
                                   # dublock.
        if a.y < b.y:
            o = ["bottom", "top"]
        elif a.y > b.y:
            o = ["top", "bottom"]
        elif a.x < b.x:
            o = ["left", "right"] 
        elif a.x > b.x:
            o =  ["right", "left"]
        return o

    def setblocks(self, blocka, blockb):
        self._blocks = (blocka, blockb)

    @property
    def blocks(self):
        return self._blocks

    def ishorizontal(self):
        return self.blocks[0].y == self.blocks[1].y
 
