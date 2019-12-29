class dublock(object):
    """
    A dublock is a block made of 2 square parts.
    """
    def init(self, blocks):
        self.blocks = blocks

    def setblocks(self, blocka, blockb):
        self.blocks = (blocka, blockb)

    @property
    def blocks(self):
        return self.blocks

    def ishorizontal(self):
        return self.blocks[0].y == self.blocks[1].y
