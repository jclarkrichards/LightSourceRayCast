import pygame
from constants import *
from vector import Vector2

class Ray(object):
    def __init__(self, start, end):
        #print("Create ray")
        self.start = start  #follows the light source
        self.end = end  #End end of this ray will change as the light source moves around
        self.anchor = end #never changes.  Where the ray is always pointing towards
        self.setNormVec()
        self.intersectorTest = None #just for testing to show where ray is intersecting
        self.allpoints = []
        
    def update(self, start):
        '''Update the origin of each ray as the light source moves around'''
        self.start = start
        self.setNormVec()
        
    def setNormVec(self):
        '''A unit vector that always points towards the anchor
        Also create 2 probes that point to the left and right of the anchor'''
        s = self.anchor - self.start
        self.norm = s.normalize()
        #self.probe1 = Vector2(self.norm.y, -self.norm.x)*20# * 0.00001
        #self.probe2 = Vector2(-self.norm.y, self.norm.x)*20# * 0.00001
        #print(self.rayprobe1)
        
    def intersect(self, segments):
        '''Given a list of segments, determine which segments we are intersecting with and where
        The closest segment is the one we are interested in.'''
        best_segment = segments[0]
        best_s = float('inf')
        best_t = 0
        self.allpoints = []
        if self.norm.magnitudeSquared() != 0:
            for segment in segments:
                t, s = segment.intersect(self)     
                if s != -1:
                    if s < best_s:
                        best_s = s
                        best_t = t
                        best_segment = segment

        #print("Best: " + str(best_segment) + " T = " + str(best_t) + " S = " + str(best_s))
        self.end = self.start + self.norm * best_s
        self.addEndPoint(self.end)

        if best_t == 0 or best_t == 1:          
            #print("Can the ray proceed?");
            vertex = best_segment.getVertex(best_t)
            #print(vertex)
            print(vertex.dividingRay(self))
               

            




    def intersect_Old(self, segments):
        '''Find closest intersection point given a list of segments'''
        Tvalues = []
        Svalues = []
        if self.norm.magnitudeSquared() != 0:
            for segment in segments:
                t, s = segment.intersect(self.start, self.norm)
                Tvalues.append(t)
                Svalues.append(s)

            #smallest svalue > 0 then use that t value to find the point on line
            #and set it as this rays end point
            sindices = [Svalues.index(k) for k in Svalues if k > 0]
            #print(sindices)
            if len(sindices) > 0:
                Tvalues_new = []
                Svalues_new = []
                segments_new = []
                for index in sindices:
                    #print(Svalues[index])
                    #if Svalues[index] >= 0:
                    Tvalues_new.append(Tvalues[index])
                    Svalues_new.append(Svalues[index])
                    segments_new.append(segments[index])
                    
                #print(Tvalues_new)
                #print(Svalues_new)
                #for segment in segments_new:
                #    print("    " + str(segment))
                #print("")
                #ignore_indices = []
                #This really needs to be in a loop where we find the closest point, but each time we need to make sure it's not an endpoint that can be ignored
                endpointFound = False
                self.allpoints = []
                while not endpointFound:
                    #T will either be 0, 1, or some value in between 0 <= T <= 1
                    index = Svalues_new.index(min(Svalues_new))
                    T = Tvalues_new[index]
                    segment = segments_new[index]
                    #print(T)
                    if T == 0 or T == 1:
                        #print(segment)
                        #We are hitting a vertex.  Get the two segments on this vertex
                        #other_segment = segment.getNeighbor(T)
                        #print(str(segment) + " :: " + str(other_segment))
                        #if other_segment is not None:
                        #Check if segment and other_segment is on one side of this ray or on both sides
                        #If on both sides, then this is where the ray stops
                        #If only on one side, then the ray continues, but we still make a note of this point
                        #We then need to find the next closest point for this ray until we find a point that causes the ray to stop
                        if segment.canStopRay(T, self.norm):
                            endpointFound = True
                            #break
                        else:
                            if len(Svalues_new) > 1:
                                Svalues_new.pop(index)
                                Tvalues_new.pop(index)
                                segments_new.pop(index)
                                self.addEndPoint(segment.tail.position + segment.vec * T)
                            else:
                                endpointFound = True
                    else:
                        endpointFound = True
                
                #if T == 0 or T == 1:
                    #print("check with the probes")
                    
                #    t1, s1 = segment.intersect(self.start, self.norm+self.rayprobe1)
                #    t2, s2 = segment.intersect(self.start, self.norm+self.rayprobe2)
                #    print("T="+str(T)+" :: t1="+str(t1) + ", t2=" + str(t2))
                #print("T = " + str(T) + " , end: " + str(self.end))
                #if self.end == segment.start:
                #self.intersectors.append(segment.start + segment.vec * T)
                #self.intersectorTest = segment.start + segment.vec * T
                self.end = segment.tail.position + segment.vec * T
                self.addEndPoint(self.end)
                #    pass
            else:
                #print("Hitting an end point")
                self.end = self.anchor
                #self.allpoints.append(self.end)
                self.intersectorTest = None
                
    def addEndPoint(self, point):
        if point not in self.allpoints:
            self.allpoints.append(point)
                
            
    def render(self, screen):
        pygame.draw.line(screen, YELLOW, self.start.asTuple(), self.end.asTuple(), 1)
            
