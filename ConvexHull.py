from GeometricStructure import *
import numpy as np
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
            d = Point(-d.y * r / (d.len()), d.x * r / (d.len()))
            U.append(Line(l.first + d, l.second + d))
        return U
    
    def circle(C):
        U_C = sorted(C, key = lambda c : c.center.x + c.radius)
        L_C = sorted(C, key = lambda c : c.center.x - c.radius)
        L_C.reverse()
        
        U_circle = []
        for i in range(0, len(U_C)):
            while len(U_circle) >= 1:
                flag = False
                if U_C[i].include(U_circle[-1]):
                    flag = True
                elif (tangent_dv(U_circle[-1], U_C[i]).vector_direction()).x < 0:
                    flag = True
                elif len(U_circle) >= 2 and vector_turn_direction(tangent_dv(U_circle[-2], U_circle[-1]), tangent_dv(U_circle[-1],U_C[i])) >= 0:
                    flag = True

                if flag:
                    U_circle[-1].draw(color = (255,0,255))
                    del U_circle[-1]
                else:
                    break
            U_circle.append(U_C[i])

        U_circle.reverse()
        for i in range(0, len(L_C)):
            if U_circle[-1].center.x - U_circle[-1].radius <= L_C[i].center.x - L_C[i].radius:
                continue
            while len(U_circle) >= 1:
                flag = False
                if L_C[i].include(U_circle[-1]):
                    flag = True
                elif (tangent_dv(L_C[i],U_circle[-1]).vector_direction()).x < 0:
                    flag = True
                elif len(U_circle) >= 2 and vector_turn_direction(tangent_dv(L_C[i],U_circle[-1]),tangent_dv(U_circle[-1], U_circle[-2])) >= 0:
                    flag = True

                if flag:
                    U_circle[-1].draw(color = (255,0,255))
                    del U_circle[-1]
                else:
                    break
            U_circle.append(L_C[i])
        U_circle.reverse()
    
        L_circle = []
        for i in range(0, len(L_C)):
            while len(L_circle) >= 1:
                flag = False
                if L_C[i].include(L_circle[-1]):
                    flag = True
                elif (tangent_dv(L_circle[-1], L_C[i]).vector_direction()).x > 0:
                    flag = True
                elif len(L_circle) >= 2 and vector_turn_direction(tangent_dv(L_circle[-2], L_circle[-1]), tangent_dv(L_circle[-1],L_C[i])) >= 0:
                    flag = True

                if flag:
                    L_circle[-1].draw(color = (255,0,255))
                    del L_circle[-1]
                else:
                    break
            L_circle.append(L_C[i])

           
        L_circle.reverse()
        for i in range(0, len(U_C)):
            if L_circle[-1].center.x + L_circle[-1].radius >= U_C[i].center.x + U_C[i].radius:
                continue
            while len(L_circle) >= 1:
                flag = False
                if U_C[i].include(L_circle[-1]):
                    flag = True
                elif (tangent_dv(U_C[i],L_circle[-1]).vector_direction()).x > 0:
                    flag = True
                elif len(L_circle) >= 2 and vector_turn_direction(tangent_dv(U_C[i],L_circle[-1]),tangent_dv(L_circle[-1], L_circle[-2])) >= 0:
                    flag = True

                if flag:
                    L_circle[-1].draw(color = (255,0,255))
                    del L_circle[-1]
                else:
                    break
            L_circle.append(U_C[i])
        L_circle.reverse()

        K = U_circle + L_circle[1:]
        K[0].draw()
        for i in range(1,len(K)):
            K[i].draw()
            tangent_dv(K[(i-1)],K[i]).draw() 
        return C

def tangent_dv(l_circle, r_circle):
    r1 = l_circle.radius
    r2 = r_circle.radius
    dv = r_circle.center - l_circle.center
    d = dv.len()
    sine = (r2 - r1) / d
    if( 1 - sine ** 2 < 0):
        print(l_circle,r_circle)
    cosine = np.sqrt(1 - sine ** 2)
    dv = Point(Point(cosine, -sine) * dv, Point(sine, cosine) *dv)
    translation = Point(-dv.y * r1 / (dv.len()), dv.x * r1 / (dv.len()))
    line = Line(l_circle.center + translation, l_circle.center + dv + translation)
    return line

def vector_turn_direction(src_l, dest_l):
    src_v = src_l.vector_direction()
    dest_v = dest_l.vector_direction()
    return Line(Point(0,0),src_v).turn_direction(src_v + dest_v)


S = [Point(random.randrange(200,500), random.randrange(200 ,400 )) for i in range(40)]
C = []
for p in S:
    C.append(Circle(p,random.randrange(50,100)))


K = ConvexHull.circle(C)

