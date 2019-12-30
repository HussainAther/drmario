import pygame

class dublock(object):
    """
    A dublock is a block made of 2 square parts, blocka and blockb.
    This is the megavitamin of Dr. Mario that the player controls.
    """
    def __init__(self, blocks):
        self._blocks = blocks
        pygame.sprite.Sprite.__init___(self)
        
    def loadimage(name, colorkey=None):
        """
        Load the sprite from the img folder.
        """
        fullname = os.path.join("img", name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error as message:
            print("Cannot load image:", name)
            raise SystemExit(message)
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image, image.get_rect()

    def setblocks(self, blocka, blockb):
        self._blocks = (blocka, blockb)

    @property
    def blocks(self):
        return self._blocks

    def ishorizontal(self):
        return self.blocks[0].y == self.blocks[1].y
 
    def getorient(self):
        """
        Get the orientation of each block in the dublock (megavitamin).
        This is used for sprite purposes.
        """
        if self.blocks[0].y < self.blocks[1].y:
            return ("bottom", "top")
        elif self.blocks[1].y < self.blocks[0].y:
            return ("top", "bottom")
        elif self.blocks[0].x < self.blocks[1].x:
            return ("left", "right") 
        elif self.blocks[1].x < self.blocks[0].x:
            return ("right", "left")
