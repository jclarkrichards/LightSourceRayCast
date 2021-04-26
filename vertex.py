"""
A Vertex is a point in space that has 2 segments connected to it.  
For this program a Vertex will always have exactly 2 segments connected to it.
The direction of each segment points away from this Vertex.
"""
from constants import *
from vector import Vector2

class Vertex(object):
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.segments = [] #should always have only 2 segments
        self.vectors = []

    def __str__(self):
        return "Vertex: " + str(self.position)

    def __eq__(self, other):
        '''2 Vertices are the same if they have the same (x,y) position'''
        if self.position == other.position:
            return True
        return False

    def addSegment(self, segment):
        #print(self.position)
        #print(segment.tail)
        #print(segment.head)
        #print("")
        if len(self.vectors) < 2:
            if segment.tail == self:
                vec = segment.head.position - segment.tail.position
                self.vectors.append(vec.normalize())
            elif segment.head == self:
                vec = segment.tail.position - segment.head.position
                self.vectors.append(vec.normalize())
            self.segments.append(segment)
        else:
            print("Too many segments, only 2 are allowed!")

    def dividingRay(self, ray):
        val1 = ray.norm.cross(self.vectors[0])
        val2 = ray.norm.cross(self.vectors[1])
        if val1 <= 0 and val2 <= 0 or val1 >= 0 and val2 >= 0:
            return False
        return True
