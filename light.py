import pygame
from constants import *
from vector import Vector2
from ray import Ray

"""Just follows the mouse around the screen and sends out light rays.
For testing this can be defined as the player."""
class LightSource(object):
    def __init__(self, segments):
        '''Gets a list of all of the segments'''
        self.segments = segments
        self.position = (10, 10)
        self.positionVec = Vector2(0, 0)
        self.rays = []
        self.createRays()
        #self.createTestRays()
        print("Number of rays: " + str(len(self.rays)))
        self.endpoints = []

    def createTestRays(self):
        self.rays.append(Ray(self.positionVec, self.segments[8].start))
        #self.rays.append(Ray(self.positionVec, self.segments[1].start))
        
    def createRays(self):
        '''Create a ray that points from origin to each end of each segment'''
        for segment in self.segments:
            self.rays.append(Ray(self.positionVec, segment.start))
            #self.rays.append(Ray(self.positionVec, segment.end))
            #for vertex in shape.vertices:
            #    self.rays.append(Ray(self.position, vertex))

    def update(self, dt):
        self.position = pygame.mouse.get_pos()
        self.positionVec = Vector2(self.position[0], self.position[1])
        self.endpoints = []
        for ray in self.rays:
            ray.update(dt, self.positionVec)
            ray.intersect(self.segments)
            self.endpoints += ray.allpoints
        #print("")
            
    def render(self, screen):
        pygame.draw.circle(screen, WHITE, self.position, 8)
        for ray in self.rays:
            ray.render(screen)

        print("There are " + str(len(self.endpoints)) + " end points")
        for endpoint in self.endpoints:
            pos = endpoint.asInt()
            pygame.draw.circle(screen, RED, pos, 5)
