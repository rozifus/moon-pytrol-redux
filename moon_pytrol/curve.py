import math

class Bezier:
    def __init__(self, points):
        assert(len(points) == 4)
        (p0,p1,p2,p3) = points
        (self.x0, self.y0) = p0
        (self.x1, self.y1) = p1
        (self.x2, self.y2) = p2
        (self.x3, self.y3) = p3

    def __call__(self, t):
        assert(0 <= t and t <= 1)
        return ( self.x0*(1-t)**3 + self.x1*3*t*(1-t)**2 + \
                 self.x2*3*(t**2)*(1-t) + self.x3*t**3 , 
                 self.y0*(1-t)**3 + self.y1*3*t*(1-t)**2 + \
                 self.y2*3*(t**2)*(1-t) + self.y3*t**3 )

    def slope(self, t):
        assert(0 <= t and t <= 1)
        return ( -3*self.x0*(1-t)**2 + 3*self.x1*(3*t**2-4*t+1) + \
                 3*self.x2*t**2*(1-t) + 3*self.x3*t**2 ,
                 -3*self.y0*(1-t)**2 + 3*self.y1*(3*t**2-4*t+1) + \
                 3*self.y2*t**2*(1-t) + 3*self.y3*t**2 )

    def slope2(self, t):
        assert(0 <= t and t <= 1)
        return( -3*(self.x0*(t-1)**2 + (-3*t**2+4*t-1)*self.x1 + \
                t*(3*t*self.x2-t*self.x3-2*self.x2)),
                -3*(self.y0*(t-1)**2 + (-3*t**2+4*t-1)*self.y1 + \
                t*(3*t*self.y2-t*self.y3-2*self.y2))
              )

