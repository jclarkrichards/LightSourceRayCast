import pygame
from constants import *
from vector import Vector2
from ray import Ray
from stack import Stack
from copy import deepcopy

"""Just follows the mouse around the screen and sends out light rays.
For testing this can be defined as the player."""
class LightSource(object):
    def __init__(self):
        '''Gets a list of all of the segments'''
        self.segments = []
        self.position = Vector2(0, 0)
        self.rays = []
        self.polygonPoints = [] #Points that make up the visibility polygon.  Each point is a tuple (x, y)
        self.segmentTest = []

        #self.endpoints = []
        self.vertex_points = []
        self.end_points = []
        self.vertices = []

        self.counter = 0
        self.timer = 0

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
        if ray.vertex_point is not None:
            #if ray.reachable:
            return ray
        return None

    def update(self):
        self.updatePosition(pygame.mouse.get_pos())
        orderedVertices = self.orderVertices()
        #self.endpoints = []
        self.vertex_points = []
        self.end_points = []
        self.rays = []
        for vertex in orderedVertices:
            ray = self.createRay(vertex)
            if ray is not None:
                self.rays.append(ray)
                #self.endpoints += ray.allpoints
                #if ray.vertex_point is not None:
                #    self.vertex_points.append(ray.vertex_point.position.asInt())
                #if ray.end_point is not None:
                #    self.end_points.append(ray.end_point)
                
        #self.endpoints = list(set(self.endpoints))
        self.createVisibilityPolygon()

    def orderVertices(self):
        '''We need to order the vertices in order to connect all of the endpoints'''
        vertices = deepcopy(self.vertices)
        probe = vertices[0] #Make this the starting point, just as good as any
        v = probe.position - self.position #just a vector pointing towards the probe vertex
        tempVertices = []
        #tempVertices.append(probe)
        #vertices.remove(probe)
        angles = []
        #Find all the angles of other vertices relative to this vertex
        for vertex in vertices:
            angle = v.angle(vertex.position - self.position)
            if angle in self.angles:
                index = angles.index(angle)
                prev_vertex = vertices[index]
                v_old = prev_vertex.position - self.position
                v_new = vertex.position - self.position
                if v_new.magnitudeSquared() < v_old.magnitudeSquared():
                    tempVertices.remove(prev_vertex)
                    tempVertices.append(vertex)
                    angles.remove(angle)
                    angles.append(angle)
            else:
                angles.append(angle)
                tempVertices.append(vertex)
        #Find any duplicate angles or angles with a 0 value.  For duplicates only keep the closest vertex
        
        
        while len(angles) > 0:
            index = angles.index(min(angles))
            tempVertices.append(vertices[index])
            self.vertices.pop(index)
            angles.pop(index)

        return tempVertices


    def getSegmentsFromPoint(self, point):
        '''Get the segments that this point lies on'''
        self.segmentTest = []
        for segment in self.segments:
            if segment.containsPoint(Vector2(*point)):
                self.segmentTest.append(segment)

    def pointInSegments(self, point):
        '''Check if the point is in on of the segments Tests'''
        for segment in self.segmentTest:
            if segment.containsPoint(Vector2(*point)):
                return True
        return False


    def createVisibilityPolygon(self):
        self.polygonPoints = []
        if len(self.rays) > 0:
        #if not self.rays.isEmpty():
            for ray in self.rays:   
                #ray = self.rays.pop()

                if ray.end_point is not None:
                    test = ray.checkVertexSegmentSide()
                    if test == 1: #Right side [end_point, vertex_point]
                        self.polygonPoints.append(ray.end_point)
                        self.polygonPoints.append(ray.vertex_point)
                        #print("Right side")
                    else: #Left side [vertex_point, end_point]
                        #print("Left side")
                        self.polygonPoints.append(ray.vertex_point)
                        self.polygonPoints.append(ray.end_point)
                        
                else:
                    self.polygonPoints.append(ray.vertex_point)
            
    """    
    def createVisibilityPolygon(self):
        '''We create the polygon by connecting all of the points in the ray list'''
        self.polygonPoints.clear()
        if not self.rays.isEmpty():
            ray = self.rays.pop()
            if ray.end_point is not None:
                self.polygonPoints.push(ray.end_point)
            self.polygonPoints.push(ray.vertex_point)
            self.getSegmentsFromPoint(self.polygonPoints.peek())

            while not self.rays.isEmpty():
                ray = self.rays.pop()

                if self.pointInSegments(ray.vertex_point):
                    self.polygonPoints.push(ray.vertex_point)
                    if ray.end_point is not None:
                        self.polygonPoints.push(ray.end_point)
          
                else:
                    if ray.end_point is not None:
                        if self.pointInSegments(ray.end_point):
                            self.polygonPoints.push(ray.end_point)
                            self.polygonPoints.push(ray.vertex_point)
                        else:
                            self.polygonPoints.swap()
                            self.getSegmentsFromPoint(self.polygonPoints.peek())

                            if self.pointInSegments(ray.vertex_point):
                                self.polygonPoints.push(ray.vertex_point)
                                if ray.end_point is not None:
                                    self.polygonPoints.push(ray.end_point)
                            else:
                                if self.pointInSegments(ray.end_point):
                                    self.polygonPoints.push(ray.end_point)
                                    self.polygonPoints.push(ray.vertex_point)
                                else:
                                    pass

                    else:
                        pass
                        #self.polygonPoints.swap()
                self.getSegmentsFromPoint(self.polygonPoints.peek())
                        
        
        
        #print(str(len(self.vertices)) + " >= " + str(len(self.vertex_points)))
        
        #while len(self.rays) > 0:
            


        #for ray in self.rays:
        #    self.polygonPoints.append(ray.vertex_point.position.asInt())
        #    if ray.end_point is not None:
        #        self.polygonPoints.append(ray.end_point)
            

    """
    def render(self, screen, dt):
        
        print(self.polygonPoints)
        if len(self.polygonPoints) > 0:
            pygame.draw.polygon(screen, DARKYELLOW, self.polygonPoints, 0)

        #pygame.draw.circle(screen, WHITE, self.position.asTuple(), 8)
        #print(str(len(self.rays)) + " rays to draw")
        for ray in self.rays:
            ray.render(screen)

        #self.timer += dt
        #if self.timer >= 0.5:
        #    self.counter += 1
        #    self.timer = 0
        #    if self.counter == len(self.vertex_points):
        #        self.counter = 0

        #print("There are " + str(len(self.endpoints)) + " end points")
        #for i, endpoint in enumerate(self.vertex_points):
            #for endpoint in self.endpoints:
            #print(endpoint)
            #pos = endpoint.asInt()
            #print(pos)
        #    if i == self.counter:
        #        pygame.draw.circle(screen, WHITE, endpoint, 8)
        #    else:
        #        pygame.draw.circle(screen, RED, endpoint, 5)

        #for endpoint in self.end_points:
        #    pygame.draw.circle(screen, BLUE, endpoint, 5)
        #print("")
        #self.endpoints.sort()
        #pygame.draw.polygon(screen, YELLOW, self.endpoints, 0)

        
