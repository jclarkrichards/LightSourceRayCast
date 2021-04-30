import pygame
from constants import *
from vector import Vector2


class Ray(object):
    def __init__(self, start, vertex):
        #print("Create ray")
        self.start = start  #follows the light source.  Is a Vector2
        #self.end = end  #End end of this ray will change as the light source moves around
        self.vertex = vertex #Vertex this ray is always pointing towards
        self.end = vertex.position
        #self.anchor = end #never changes.  Where the ray is always pointing towards
        self.setNormVec()
        self.intersectorTest = None #just for testing to show where ray is intersecting

        self.vertex_point = None #If the ray reaches the vertex then this will not be None (x, y)
        self.end_point = None #If the end point for the ray is not its vertex, then this will not be None (x, y)
        self.no_end_point_test = False
        
    def update(self, start):
        '''Update the origin of each ray as the light source moves around'''
        self.start = start
        self.setNormVec()
        
    def setNormVec(self):
        '''A unit vector that always points towards the anchor
        Also create 2 probes that point to the left and right of the anchor'''
        s = self.vertex.position - self.start
        self.norm = s.normalize()

    def intersectQuick(self, allsegments):
        '''This is just a quick test to see if this ray intersects with any segment.  Return True if so'''
        for segment in allsegments:
            t, s = segment.intersect(self)
            print(segment)
            print(t, s)
            
   
        
    def checkVertexSegmentSide(self):  #Return 0 for left side and 1 for right side
        '''Determine if the segments attached to vertex ray points to is on the left or right side of ray'''
        val0 = self.norm.cross(self.vertex.vectors[0])
        val1 = self.norm.cross(self.vertex.vectors[1])
        if val0 > 0 or val1 > 0: return 1
        return 0

       
        
    def intersect(self, allsegments):
        '''Given a list of segments, determine which segments we are intersecting with and where
        The closest segment is the one we are interested in.'''
        svalues = []
        tvalues = []
        segments = []
        self.allpoints = []
        if self.norm.magnitudeSquared() != 0:
            for i, segment in enumerate(allsegments):
                t, s = segment.intersect(self)     
                if s != -1:
                    svalues.append(s)
                    tvalues.append(t)
                    segments.append(segment)

            #print("Only " + str(len(segments)) + " segments to test")
            #print(svalues)
            #print(tvalues)
            #print("")
            
            finished = False
            while not finished:
                if len(svalues) > 0:
                    i = svalues.index(min(svalues)) #lowest svalue is closest intersection
                    best_s = svalues[i]
                    best_t = tvalues[i]
                    best_segment = segments[i]
                    if best_t == 0 or best_t == 1:
                        
                        #self.reachable = True
                        vertex = best_segment.getVertex(best_t)
                        if vertex == self.vertex:
                            self.vertex_point = vertex.position.asInt()
                            
                        if vertex.dividingRay(self):
                            finished = True
                            self.no_end_point_test = True
                            
                        else:                            
                            svalues.remove(best_s)
                            tvalues.remove(best_t)
                            segments.remove(best_segment)

                            #if len(svalues) == 0 and self.end_point is None:
                            #    end = self.start + self.norm * best_s
                            #    self.end_point = end.asInt()
                            #    finished = True
                    else:
                        finished = True
                        end = self.start + self.norm * best_s
                        self.end_point = end.asInt()
                    
                else:
                    finished = True
            

            self.end = self.start + self.norm * best_s
            if self.end_point is None:
                #print(str(self.vertex) + " :: best_t = " + str(best_t))
                if best_t == 0 or best_t == 1:
                    #end = self.start + self.norm * best_s
                    self.end_point = self.end.asInt()

                else:
                    if not self.no_end_point_test:
                        self.end_point = self.end.asInt()


            
            
    #def addEndPoint(self, point):
    #    pointInt = point.asInt()
    #    if pointInt not in self.allpoints:
    #        self.allpoints.append(pointInt)
                
            
    def render(self, screen):
        pygame.draw.line(screen, YELLOW, self.start.asTuple(), self.end.asTuple(), 1)
            
