import pygame
from vector import Vector2
from constants import *
from segment import Segment

class Shape(object):
    def __init__(self, vertices, width=0, color=(255, 255, 255)):
        '''vertices is a list or tuple of (x,y) pairs.  ((2,3), (3,4), (8, 9))
        Set the width to 0 if you want the shape filled in.
        Change the color to something else if you want other than white'''
        self.vertices = vertices
        self.segments = []
        self.width = width
        self.color = color
        self.segmentize()
        self.defineNeighbors()
        
    def segmentize(self):
        '''Break this shape down into segments.  For example, a triangle will have 3 segments'''
        #print(self.vertices)
        #print(type(self.vertices))
        vertices = list(self.vertices) + [self.vertices[0]]
        for i in range(len(vertices)-1):
            #index_start = i
            #index_end = i+1
            #if index_end == len(self.vertices):
            #    index_end = 0
            self.segments.append(Segment(vertices[i], vertices[i+1]))

        #print("SEGMENTS OF THIS SHAPE")
        #for segment in self.segments:
        #    print(segment)
        #print("")

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
        pygame.draw.polygon(screen, self.color, self.vertices, self.width)
