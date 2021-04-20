"""
A Segment is a line with endpoints.
The direction of a segment should not matter, but for purposes of detecting intersections one end
of the segment needs to be designated as the start of the segment and the other end as the end of the segment.
"""
from vector import Vector2

class Segment(object):
    def __init__(self, vertex0, vertex1):
        self.tail = vertex0
        self.head = vertex1
        #self.start = vertex0.position
        #self.end = vertex1.position
        self.vec = self.head.position - self.tail.position
        #self.norm = self.vec.normalize()
        self.thresh = 0.000000001
        #self.neighbors = [] #Other segments that are connected to this segment

    def __str__(self):
        return "Segment: " + str(self.tail) + " ===> " + str(self.head)

    def __eq__(self, other):
        '''Two segments are equal if they have the same start and end vertices'''
        if self.tail == other.tail and self.head == other.head:
            return True
        return False
    
    def intersect(self, ray):
        '''Return the T value where the ray intersects the segment'''
        denom = self.vec.cross(ray.norm)
        if denom != 0:
            vec = ray.start - self.tail.position
            num1 = vec.cross(ray.norm)
            num2 = vec.cross(self.vec)
            t = num1 / denom
            s = num2 / denom
            t = self.compareSmallValues(t)            

            #if t <= self.thresh: t = 0
            #if abs(t-1) <= self.thresh: t = 1
            
            if s > 0 and 0 <= t <= 1:
                return t, s
            else:
                return t, -1
            
        return -1, -1

    def compareSmallValues(self, value):
        if abs(1-value) < self.thresh:
            return 1
        if abs(value) < self.thresh:
            return 0
        return value

    def getVertex(self, value):
        if value == 0: return self.tail
        return self.head

    """
    #def addNeighbor(self, segment):
    #    self.neighbors.append(segment)
    
    def getNeighbor(self, value):
        '''Input either a 0 or a 1.  If 0, then return the neighbor with same self.start.  otherwise return self.end neighbor'''
        if value == 0:
            vertex = self.start
        if value == 1:
            vertex = self.end

        for n in self.neighbors:
            if n.start == vertex or n.end == vertex:
                return n
        return None
    
    def getVector(self, reverse=False):
        if not reverse:
            return self.end - self.start
        else:
            return self.start - self.end

    def canStopRay(self, value, r):
        other = self.getNeighbor(value)
        if other is not None:
            if value == 0:
                
                
                v = self.getVector()
                if other.start == self.start:
                    w = self.getVector()
                else:
                    w = other.getVector(True)

            elif value == 1:
                v = self.getVector(True)
                if other.start == self.end:
                    w = other.getVector()
                else:
                    w = other.getVector(True)
            
            
            #v = self.end - self.start
            #if self.start == other.end:
            #    w = other.end - other.start
            #else:
            #w = other.start - other.end
            if (r.cross(v) > 0 and r.cross(w) > 0 or
                r.cross(v) < 0 and r.cross(v) < 0):
                return False
        return True
        """
