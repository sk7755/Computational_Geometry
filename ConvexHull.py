from GeometricStructure import *
# Compute convex hull of the set of points
# Input:    S = the list of points
# Output:   C = the list of line segments of convex hull
# TimeComplexity: O(nlogn)
class ConvexHull:
    def point(S):
        S = sorted(S)
        U = []
        for i in range(1,len(S)):
            while len(U)>= 1 and U[-1].turn_direction(S[i]) >= 0 :
                del U[-1]
            if len(U) == 0 :
                U.append(Line(S[0],S[i]))
            else :
                U.append(Line(U[-1].second, S[i]))

        S.reverse()
        L = []
        
        for i in range(1,len(S)):
            while len(L)>= 1 and L[-1].turn_direction(S[i]) >= 0 :
                del L[-1]
            if len(L) == 0 :
                L.append(Line(S[0],S[i]))
            else :
                L.append(Line(L[-1].second, S[i]))
                
        return U + L

    def unit_circle(C):
        r = C[0].radius
        S = [c.center for c in C]
        L = ConvexHull.point(S)
        U = []
        for l in L:
            d = l.vector_direction()
            d = Point(-d.y * r // d.len(), d.x * r // d.len())
            U.append(Line(l.first + d, l.second + d))
        return U


S = [Point(random.randrange(50+i//5,400-i//5), random.randrange(100 - i//5,300 + i//5)) for i in range(20)]
C = []
for p in S:
    C.append(Circle(p,30))
for c in C:
    c.draw()
    c.center.draw()

K = ConvexHull.unit_circle(C)

for k in K:
    k.draw()
