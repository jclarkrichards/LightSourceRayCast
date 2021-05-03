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
        self.triangles = []

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
        if ray.vertex_reached:
        #if ray.vertex_point is not None:
            #if ray.reachable:
            return ray
        return None

    def update(self):
        self.updatePosition(pygame.mouse.get_pos())
        #print("==============================")
        orderedVertices = self.orderVertices()
        #print("==============================")
        #print(str(len(orderedVertices)) + " out of " + str(len(self.vertices)) + " vertices used")
        #print("")
        
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
                #    self.vertex_points.append(ray.vertex_point)
                #if ray.end_point is not None:
                #    self.end_points.append(ray.end_point)
                
        #self.endpoints = list(set(self.endpoints))
        self.createVisibilityTriangles()
        #self.createVisibilityPolygon()

    def orderVertices(self):
        '''We need to order the vertices in order to connect all of the endpoints'''
        vertices = deepcopy(self.vertices) #do not modify the original list of vertices
        probe = vertices[0] #Make this the starting point, just as good as any
        v = probe.position - self.position #just a vector pointing towards the probe vertex
        tempVertices = []
        finalVertices = []
        #tempVertices.append(probe)
        #vertices.remove(probe)
        angles = []
        #Find all the angles of other vertices relative to this vertex
        for vertex in vertices:
            angle = v.angle(vertex.position - self.position)
            #print(str(vertex) + " :: Angle = " + str(angle))
            
            if angle in angles:
                index = angles.index(angle)
                prev_vertex = tempVertices[index]
                v_old = prev_vertex.position - self.position
                v_new = vertex.position - self.position
                if v_new.magnitudeSquared() < v_old.magnitudeSquared():
                    #print("new vertex is closer, so get rid of old one")
                    tempVertices.remove(prev_vertex)
                    tempVertices.append(vertex)
                    angles.remove(angle)
                    angles.append(angle)
            else:
                angles.append(angle)
                tempVertices.append(vertex)
                   
        #print("Final angles: " + str(angles))
        while len(angles) > 0:
            index = angles.index(min(angles))
            finalVertices.append(tempVertices.pop(index))
            #tempVertices.pop(index)
            angles.pop(index)
        
        #return vertices
        return finalVertices

    def getSegmentsFromPoint(self, point):
        '''Given a point, return a list of segments that contains this point'''
        result = []
        for segment in self.segments:
            if segment.containsPoint(Vector2(*point)):
                result.append(segment)
        return result

    def checkSegmentInBoth(self, segmentList1, segmentList2):
        '''Given two lists of segments, check to see if there is a segment in both'''
        for segment in segmentList1:
            if segment in segmentList2:
                return True
        return False

    #def getSegmentsFromPoint(self, point):
    #    '''Get the segments that this point lies on'''
    #    self.segmentTest = []
    #    for segment in self.segments:
    #        if segment.containsPoint(Vector2(*point)):
    #            self.segmentTest.append(segment)

    def pointInSegments(self, point):
        '''Check if the point is in on of the segments Tests'''
        for segment in self.segmentTest:
            if segment.containsPoint(Vector2(*point)):
                return True
        return False

    
    def createVisibilityTriangles(self):
        '''Going to create the area of visibility using triangles'''
        self.triangles = []
        for i in range(len(self.rays)):
            found = False
            r0 = self.rays[i]
            if (i+1) == len(self.rays):
                r1 = self.rays[0]
            else:
                r1 = self.rays[i+1]


            for i, r0p in enumerate(r0.points):
                for j, r1p in enumerate(r1.points):
                    #seglist0 = self.getSegmentsFromPoint(r0p)
                    #seglist1 = self.getSegmentsFromPoint(r1p)
                    seglist0 = r0.segments[i]
                    seglist1 = r1.segments[j]
                    if self.checkSegmentInBoth(seglist0, seglist1):
                        self.triangles.append((self.position.asInt(), r0p, r1p))
                        found = True
                        break
                if found:
                    break
            
          

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
            
    
    def render(self, screen, dt):
        
        #print(self.polygonPoints)
        #if len(self.polygonPoints) > 0:
        #    pygame.draw.polygon(screen, DARKYELLOW, self.polygonPoints, 0)

        #pygame.draw.circle(screen, WHITE, self.position.asTuple(), 8)
        #print(str(len(self.rays)) + " rays to draw")
        

        #print(str(len(self.triangles)) + " triangles")
        #print(str(len(self.triangles)) + " triangles")
        for triangle in self.triangles:
            pygame.draw.polygon(screen, DARKYELLOW, triangle, 0)

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


        #print("There are " + str(len(self.vertex_points)) + " vertex points")
        #for p in self.vertex_points:
        #    pygame.draw.circle(screen, RED, p, 5)

        #for endpoint in self.end_points:
        #    pygame.draw.circle(screen, BLUE, endpoint, 5)
        #print(str(len(self.rays)) + " rays")
       
        for ray in self.rays:
            #print("Ray has " + str(len(ray.points)) + " points")
            #print("Ray has " + str(len(ray.segments)) + " segments")
            #for i in range(len(ray.points)):
                #pygame.draw.circle(screen, BLUE, ray.points[i], 5)
                #print(str(i) + " ..... " + str(ray.points[i]))
                #print(ray.segments[i])
                #for s in ray.segments[i]:
                #    print(s)
                
            #print(ray.points)
            #print(ray.segments)
            #print("---------------------------------------------------------------")
            #print(str(ray) + " has " + str(len(ray.points)) + " points and " + str(len(ray.segments)) + " segments")
            for p in ray.points:
                pygame.draw.circle(screen, BLUE, p, 5)

        #print("")
        #self.endpoints.sort()
        #pygame.draw.polygon(screen, YELLOW, self.endpoints, 0)

        
