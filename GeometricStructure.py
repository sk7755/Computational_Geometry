import cv2 as cv
import numpy as np
import random

img = np.zeros((512,1024,3),np.uint8) + 255

def set_drawboard(width, height):
    img = np.zeros((height,width,3),np.uint8) + 255

class Point:
    def __init__(self, x,y):
        self.x = x
        self.y = y
    def __add__(self,other):
        return Point(self.x + other.x, self.y+ other.y)
    def __sub__(self,other):
        return Point(self.x - other.x, self.y- other.y)
    def __lt__(self,other):
        if self.x == other.x :
            return self.y < other.y
        return self.x < other.x
    def __repr__(self):
        return '('+str(self.x) +', '+str(self.y)+')'
    def reverse(self):
        self.x, self.y = self.x, self.y
        return self
    def get_tuple(self):
        return (self.x, self.y)
    def __mul__(self, other):
        return self.x * other.x + self.y * other.y

    def len(self):
        return int(np.sqrt(self.x ** 2 + self.y ** 2))
    
    def draw(self):
        cv.line(img, self.get_tuple(),self.get_tuple(), (0,0,0),5)
        cv.imshow('image',img)

class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def __repr__(self):
        return '[c='+self.center.__repr__()+', r= '+str(self.radius)+']'

    def draw(self):
        cv.circle(img,self.center.get_tuple(),self.radius,(0,0,0))
        cv.imshow('image',img)
    
class Line:
    def __init__(self, first, second):
        self.first, self.second = first, second

    def __repr__(self):
        return '['+self.first.__repr__()+', '+self.second.__repr__()+']'

    #right : negative, left : positive, onLine : zero 
    def turn_direction(self,r):
        p,q = self.first, self.second
        t = (p.x * q.y - p.y * q.x)
        t -= (p.x * r.y - p.y * r.x)
        t += (q.x * r.y - q.y * r.x)
        return t
    
    def intersection(self, other):
        t = self.turn_direction(other.first) * self.turn_direction(other.second)
        if t == 0: return True
        elif t > 0 : return False
        s = other.turn_direction(self.first) * other.turn_direction(self.second)
        if s == 0 : return True
        elif s > 0 : return False
        return True

    def vector_direction(self):
        return self.second - self.first
    
    def draw(self):
        cv.line(img,(self.first.x, self.first.y), (self.second.x, self.second.y),(0,0,0))
        cv.imshow('image',img)
