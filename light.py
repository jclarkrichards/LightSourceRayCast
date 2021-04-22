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
        
        #self.endpoints = []
        self.vertex_points = []
        self.nonvertex_points = []
        self.vertices = []

    def updatePosition(self, pos):
        self.position.x = pos[0]
        self.position.y = pos[1]
       

    def setVisibleShapes(self, shapes):
        for shape in shapes:
            self.segments += shape.segments
        #print("Check " + str(len(self.segments)) + " segments")

    def setVertices(self, shapes):
        for shape in shapes:
            self.vertices += shape.vertices
        print("Number of vertices = " + str(len(self.vertices)))

    def createTestRays(self):
        '''Create a ray that points from this light source to a defined vertex'''
        self.rays.append(Ray(self.position, self.segments[4].tail.position))
        
    def createRays(self):
        '''Create a ray that points from origin to each vertex of each shape'''
        for segment in self.segments:
            self.rays.append(Ray(self.position, segment.tail.position))

    def createRay(self, vertex):
        '''Create a ray from light position to the vertex.  Return the ray if the vertex is reachable only'''
        ray = Ray(self.position, vertex)
        ray.intersect(self.segments)
        if len(ray.vertex_point) != 0:
            #if ray.reachable:
            return ray
        return None

    def update(self):
        self.updatePosition(pygame.mouse.get_pos())
        self.vertices = self.orderRays()
        #self.endpoints = []
        self.vertex_points = []
        self.nonvertex_points = []
        self.rays = []
        for vertex in self.vertices:
            ray = self.createRay(vertex)
            if ray is not None:
                self.rays.append(ray)
                #self.endpoints += ray.allpoints
                self.vertex_points += ray.vertex_point
                self.nonvertex_points += ray.nonvertex_points
                
        #self.endpoints = list(set(self.endpoints))
        
    def orderRays(self):
        '''We need to order the rays in order to connect all of the endpoints'''
        probe = self.vertices[0]
        v = probe.position - self.position
        tempVertices = []
        tempVertices.append(probe)
        self.vertices.remove(probe)
        angles = []
        for vertex in self.vertices:
            angles.append(v.angle(vertex.position - self.position))

        while len(angles) > 0:
            index = angles.index(min(angles))
            tempVertices.append(self.vertices[index])
            self.vertices.pop(index)
            angles.pop(index)

        return tempVertices

    
            
    def render(self, screen):
        pygame.draw.circle(screen, WHITE, self.position.asTuple(), 8)
        #print(str(len(self.rays)) + " rays to draw")
        for ray in self.rays:
            ray.render(screen)

        #print("There are " + str(len(self.endpoints)) + " end points")
        for endpoint in self.vertex_points:
            #for endpoint in self.endpoints:
            #print(endpoint)
            #pos = endpoint.asInt()
            #print(pos)
            pygame.draw.circle(screen, RED, endpoint, 5)

        for endpoint in self.nonvertex_points:
            pygame.draw.circle(screen, BLUE, endpoint, 5)
        #print("")
        #self.endpoints.sort()
        #pygame.draw.polygon(screen, YELLOW, self.endpoints, 0)
