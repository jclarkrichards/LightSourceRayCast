from vector import Vector2
from vertex import Vertex
from segment import Segment
from ray import Ray
from shape import Shape

box = Shape(((10,10), (20,10), (20,20), (10,20)))

for segment in box.segments:
    print(segment)

p0 = Vector2(10,10)
p1 = Vector2(20,10)
p2 = Vector2(12,10)
p3 = Vector2(20,15)
p4 = Vector2(13,20)
p5 = Vector2(10,18)
p6 = Vector2(20,20)
p7 = Vector2(10, 20)

points = [p0, p1, p2, p3, p4, p5, p6, p7]
for p in points:
    print(p)
    for segment in box.segments:
        if segment.containsPoint(p):
            print(segment)
    print("")

#vertex = box.segments[0].tail #test on the first vertex in the shape (10,10)
#print("Test vertex = " + str(vertex))

#for p in points:
#    print("Point " + str(p) + " ....................")
#    ray = Ray(p, vertex)
#    ray.intersectQuick(box.segments)
#    #print(str(p) + " intersects before vertex?  " + str(ray.intersectQuick(box.segments)))
#    print("")
