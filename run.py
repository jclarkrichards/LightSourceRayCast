"""

"""
import pygame
from pygame.locals import *
from vector import *
from constants import *
from shape import Shape
from light import LightSource
from segment import Segment

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.setBackground()
        self.shapes = []
        self.segments = []
        self.vertices = []
        self.player = None
        self.clock = pygame.time.Clock()
        
    def setBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def createShapes(self):
        self.addShapeToWorld(((0,0), (SCREENWIDTH, 0), SCREENSIZE, (0, SCREENHEIGHT)), width=1)
        self.addShapeToWorld(((50,50),  (100, 50), (50, 100)), color=(200, 200, 200))
        self.addShapeToWorld(((SCREENWIDTH-50, 50),  (SCREENWIDTH-50, 100), (SCREENWIDTH-100, 50)), color=(200, 200, 200))
        self.addShapeToWorld(((SCREENWIDTH-50, SCREENHEIGHT-50),  (SCREENWIDTH-100, SCREENHEIGHT-50), (SCREENWIDTH-50, SCREENHEIGHT-100)), color=(200, 200, 200))
        self.addShapeToWorld(((50, SCREENHEIGHT-50),  (100, SCREENHEIGHT-50), (50, SCREENHEIGHT-100)), color=(200, 200, 200))

        #self.addShapeToWorld(((500,50),  (520, 150), (450, 120)), color=(200, 200, 200))
        #self.addShapeToWorld(((200,100), (300, 220), (180, 350), (100, 300)), color=(0, 100, 180))
        #self.addShapeToWorld(((300,400), (250, 500), (210, 410)), color=(200, 0, 0))
        #self.addShapeToWorld(((550, 400), (550, 500), (450, 500), (450, 400)), color=(30,100,90))
        #self.addShapeToWorld(((600,150), (700, 160), (720, 400), (580, 280)), color=(70, 200, 100))

    def createPlayer(self):
        self.player = LightSource()
        self.player.setVisibleShapes(self.shapes)
        self.player.setVertices(self.shapes)
        #self.player.createTestRays()
        #self.player.createRays()

    def addShapeToWorld(self, vertices, color=(255,255,255), width=0):
        for vertex in vertices:
            self.vertices.append(Vector2(*vertex))
        self.shapes.append(Shape(vertices, width, color))
    
    def update(self):
        self.dt = self.clock.tick(30) / 1000.0
        if self.player is not None:
            self.player.update()
        self.checkEvents()
        self.render()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
                
    def render(self):
        self.screen.blit(self.background, (0, 0))
        for shape in self.shapes:
            shape.render(self.screen)
        if self.player is not None:
            self.player.render(self.screen, self.dt)
        pygame.display.update()


if __name__ == "__main__":
    game = GameController()
    game.createShapes()
    game.createPlayer()
    while True:
        game.update()
