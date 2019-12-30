# Import the functionality of other files.
import board
import ex

# Import installed modules.
import pygame
import sys

# Import the Board class from the board.py file, the keyboard functions
# from pygame, the colors from colors.py, and the Pos (position) function from 
# utils.py.
from board import Board
from pygame.constants import KEYUP, KEYDOWN, K_DOWN, K_LEFT, K_RIGHT, K_SPACE, K_UP, K_q, QUIT 
from colors import black, blue, brightred, brightgreen, darkblue, darkgray, green, red, white, yellow
from utils import Pos

fps = 60 # frames per second
windowwidth = 400 # width of the overall window 
windowheight = 400 # height of the window

# where the Dr. Mario game box will be
boardoffsetx = (windowwidth - 140) / 2
boardoffsety = (windowheight - 400) / 2
boardborder = 1 # border thickness

blockfallinterval = 300 # time before the block falls automatically 
speedfallmultiplier = 100.0

def gameintro(self):
    """
    Display the menu until the user starts the game.
    """
    intro = True
    pygame.mixer.music.load("music/birabuto.wav")
    pygame.mixer.music.play(0)
    while intro:
        win = pygame.display.set_mode((400, 400))
        win.fill((0,0,0))
        titlefont = pygame.font.SysFont("Times New Roman", 36, bold = True) 
        instructionfont = pygame.font.SysFont("Times New Roman", 24) 
        startfont = pygame.font.SysFont("Times New Roman", 24) 
        title = titlefont.render("Dr. Mario", 36, (255, 255, 255))
        instruction1 = instructionfont.render("Use arrow keys to move", 1, (255, 255, 255))
        instruction2 = instructionfont.render("and space to rotate.", 1, (255, 255, 255))
        starttext1 = startfont.render("Press space to start", 1, (255, 255, 255))
        starttext2 = startfont.render("and q to quit.", 1, (255, 255, 255))
        self._display.blit(title, (20, 100))
        self._display.blit(instruction1, (20, 150))
        self._display.blit(instruction2, (20, 170))
        self._display.blit(starttext1, (20, 300))
        self._display.blit(starttext2, (20, 320))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_SPACE:
                intro = False

def text_objects(text, font):
    """
    Create a rectangular object around which to put text.
    """
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

class Game(object):
    """
    This is the class for the game itself. It's the main class that controls the 
    other parts of the game. It's in charge of the basic, fundamental functions and 
    processes that the game needs.
    """
    def __init__(self):
        self._board = Board()
        pygame.init()
        pygame.mixer.init()
        self.fpsClock = pygame.time.Clock()
        self._display = pygame.display.set_mode((windowwidth, windowheight), 0, 32)
        gameintro(self)
        pygame.mixer.music.load("music/fever.wav")
        pygame.mixer.music.play(-1)
        self.blockfalltimer = blockfallinterval
        self.speed = False
        scorefont = pygame.font.Font(None, 36)
        scoretext = scorefont.render(str(self._board.score), 14, white)
        self._display.blit(scoretext, (10, 200))
        pygame.display.update()

    def run(self):
        self.board.spawndublock()

        while True:
            for event in pygame.event.get():
                self.processevent(event)

            self.update(self.fpsclock.get_time())

            self._display.fill(darkgray)

            pygame.draw.rect(self._display, darkblue,
                             (boardoffsetx-boardborder, boardoffsety-boardborder,
                              140+boardborder*2,
                              400+boardborder*2))
            boarddisplay = self.board.render()
            self._display.blit(boarddisplay, (boardoffsetx, boardoffsety))
            scorefont = pygame.font.Font(None, 36)
            scoretext = scorefont.render(str(self._board.score), 14, white)
            self._display.blit(scoretext, (10, 200))
            self._display.blit(scoretext, (10, 200))
            pygame.display.update()
            self.fpsclock.tick(fps)

    def update(self, delta):
        if self.blockfalltimer <= 0:
            try:
                self.board.movedublock("down")
            except (ex.BottomReached, ex.PositionOccupied):
                self.handlecollision()
            self.blockfalltimer = blockfallinterval
        else:
            if self.speed:
                delta *= speedfallmultiplier
            self.blockfalltimer -= delta

    def handlecollision(self):
        self.board.handlecollision()

    def processevent(self, event):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == K_RIGHT:
                direction = "left" if event.key == K_LEFT else "right"
                self.movedublock(direction)
            elif event.key == K_DOWN:
                self.speed = True
            elif event.key == K_SPACE:
                self.board.rotatedublock()
            elif event.key == K_q:
               pygame.quit()
               sys.exit()
        elif event.type == KEYUP:
            if event.key == K_DOWN:
                self.speed = False

    def movedublock(self, direction):
        try:
            self.board.movedublock(direction)
        except (ex.OutOfBoard, ex.PositionOccupied):
            # If we can't move to a certain position,
            # simply ignore those. The dublock will not move at all.
            pass

    @property
    def board(self):
        """
        Define the board property.
        """
        return self._board

    @property
    def display(self):
        """
        Define the display property for the actual pygame display.
        """
        return self._display

    @property
    def fpsclock(self):
        """
        This is a neat clock based on the fps.
        """
        return self.fpsClock
