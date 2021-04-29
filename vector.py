import math

class Vector2(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.thresh = 0.000001

    def __str__(self):
        return "<"+str(self.x)+", "+str(self.y)+">"
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def __div__(self, scalar):
        if scalar != 0:
            return Vector2(self.x / float(scalar), self.y / float(scalar))
        return None

    def __truediv__(self, scalar):
        return self.__div__(scalar)

    def __eq__(self, other):
        if abs(self.x - other.x) < self.thresh:
            if abs(self.y - other.y) < self.thresh:
                return True
        return False

    def __hash__(self):
        return id(self)

    def magnitudeSquared(self):
        return self.x**2 + self.y**2

    def magnitude(self):
        return math.sqrt(self.magnitudeSquared())

    def dot(self, other):
        return self.x*other.x + self.y*other.y

    def copy(self):
        return Vector2(self.x, self.y)

    def normalize(self):
        mag = self.magnitude()
        if mag != 0:
            return self.__div__(mag)
        return Vector2(0, 0)

    def asTuple(self):
        return self.x, self.y
    
    def asInt(self):
        return int(self.x), int(self.y)

    def cross(self, other):
        return self.x*other.y - self.y*other.x

    def angle(self, other):
        '''Return the angle in radians that these 2 vectors make'''
        mag = self.magnitude()
        othermag = other.magnitude()
        if mag != 0 and othermag != 0:
            val = self.dot(other) / (mag * othermag)
            val = min(val, 1)
            val = max(val, -1)
            A = math.acos(val)

            if self.cross(other) < 0:
                A = 2*math.pi - A
                #return 2*math.pi - A

            if (A - int(A)) <= self.thresh:
                return int(A)
            return round(A, 4)
        return 999 #what should I return by default?  This really should never happen
