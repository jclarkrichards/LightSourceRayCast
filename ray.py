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

        self.vertex_point = None #If the ray reaches the vertex then this will be not be None (Vertex)
        self.end_point = None #If the end point for the ray is not its vertex, then this will not be None (x, y)

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
            #while len(svalues) > 0:
            while not finished:
                if len(svalues) > 0:
                    i = svalues.index(min(svalues))
                    best_s = svalues[i]
                    best_t = tvalues[i]
                    best_segment = segments[i]
                    if best_t == 0 or best_t == 1:
                        
                        #self.reachable = True
                        vertex = best_segment.getVertex(best_t)
                        if vertex == self.vertex:
                            self.vertex_point = vertex #.position.asInt()
                            #self.vertex_point.append(vertex.position.asInt())
                        #else:
                        #    self.nonvertex_points.append(vertex.position.asInt())
                            
                        if vertex.dividingRay(self):
                            finished = True
                        else:                            
                            #self.addEndPoint(vertex.position)
                            svalues.remove(best_s)
                            tvalues.remove(best_t)
                            segments.remove(best_segment)
                    else:
                        finished = True
                        end = self.start + self.norm * best_s
                        self.end_point = end.asInt()
                        #self.nonvertex_points.append(end.asInt())
                    
                else:
                    finished = True
            

            self.end = self.start + self.norm * best_s
            #self.addEndPoint(self.end)


            
            
    #def addEndPoint(self, point):
    #    pointInt = point.asInt()
    #    if pointInt not in self.allpoints:
    #        self.allpoints.append(pointInt)
                
            
    def render(self, screen):
        pygame.draw.line(screen, YELLOW, self.start.asTuple(), self.end.asTuple(), 1)
            
