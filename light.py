import pygame
from constants import *
from vector import Vector2
from ray import Ray

"""Just follows the mouse around the screen and sends out light rays.
For testing this can be defined as the player."""
class LightSource(object):
    def __init__(self):
        '''Gets a list of all of the segments'''
        self.segments = []
        self.position = Vector2(0, 0)
        self.rays = []
        #self.createRays()
        #self.createTestRays()
        
        self.endpoints = []
        #self.vertices = []

    def updatePosition(self, pos):
        self.position.x = pos[0]
        self.position.y = pos[1]

    def setVisibleShapes(self, shapes):
        for shape in shapes:
            self.segments += shape.segments
        print("Check " + str(len(self.segments)) + " segments")

    def createTestRays(self):
        '''Create a ray that points from this light source to a defined vertex'''
        self.rays.append(Ray(self.position, self.segments[4].tail.position))
        
    def createRays(self):
        '''Create a ray that points from origin to each vertex of each shape'''
        for segment in self.segments:
            self.rays.append(Ray(self.position, segment.tail.position))
            #self.rays.append(Ray(self.positionVec, segment.end))
            #for vertex in shape.vertices:
            #    self.rays.append(Ray(self.position, vertex))
        #print("Number of rays: " + str(len(self.rays)))

    def update(self):
        self.updatePosition(pygame.mouse.get_pos())
        self.endpoints = []
        for ray in self.rays:
            ray.update(self.position)
            ray.intersect(self.segments)
            self.endpoints += ray.allpoints
        self.endpoints = list(set(self.endpoints))
        #print("")
            
    def render(self, screen):
        pygame.draw.circle(screen, WHITE, self.position.asTuple(), 8)
        for ray in self.rays:
            ray.render(screen)

        print("There are " + str(len(self.endpoints)) + " end points")
        for endpoint in self.endpoints:
            print(endpoint)
            #pos = endpoint.asInt()
            #print(pos)
            pygame.draw.circle(screen, RED, endpoint, 5)
        print("")
