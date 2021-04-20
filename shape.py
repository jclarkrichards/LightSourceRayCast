import pygame
from vector import Vector2
from constants import *
from segment import Segment
from vertex import Vertex

class Shape(object):
    def __init__(self, points, width=0, color=(255, 255, 255)):
        '''vertices is a list or tuple of (x,y) pairs.  ((2,3), (3,4), (8, 9))
        Set the width to 0 if you want the shape filled in.
        Change the color to something else if you want other than white'''
        self.points = points  #So we can easily draw the shape
        self.width = width
        self.color = color
        self.vertices = []
        self.createVertices(points)
        self.segments = [] #A list of the Segment objects that make up this shape used for detecting intersections      
        self.createSegments()
        #self.defineNeighbors()
        self.addSegmentsToVertices()

        for vertex in self.vertices:
            print("Vertex " + str(vertex) + " has " + str(len(vertex.vectors)) + " segments")
            print("          " + str(vertex.vectors[0]))
            print("          " + str(vertex.vectors[1]))

    def createVertices(self, points):
        for point in points:
            print("Vertices: " + str(point))
            self.vertices.append(Vertex(*point))
        
    def createSegments(self):
        '''Break this shape down into segments.  For example, a triangle will have 3 segments.
        It is assumed that each vertex is connected to neighboring vertices and that the first and
        last vertices are connected together.'''
        vertices = list(self.vertices) + [self.vertices[0]]
        for i in range(len(self.vertices)):
            segment = Segment(vertices[i], vertices[i+1])
            print("Segment: " + str(segment))
            self.segments.append(segment)
            #vertices[i].addSegment(segment)
            #vertices[i+1].addSegment(segment)

    def addSegmentsToVertices(self):
        for i, vertex in enumerate(self.vertices):
            #print("Vertex: " + str(vertex) + " segment indices: " + str(i) + ", " + str(i-1))
            #print("     Segment: " + str(self.segments[i]))
            #print("     Segment: " + str(self.segments[i-1]))
            vertex.addSegment(self.segments[i])
            vertex.addSegment(self.segments[i-1])

    def defineNeighbors(self):
        '''A neighbor segment is a segment that is connected to this segment by a single vertex'''
        for segment in self.segments:
            for other in self.segments:
                if segment != other:
                    if (segment.start == other.start or
                        segment.start == other.end or
                        segment.end == other.start or
                        segment.end == other.end):
                        segment.addNeighbor(other)

        print("Segments and their neighbors")
        for segment in self.segments:
            print(segment)
            for other in segment.neighbors:
                print("       " + str(other))
        print("")
            
    def render(self, screen):
        '''The vertices next to each other are connected together to make lines'''
        pygame.draw.polygon(screen, self.color, self.points, self.width)
