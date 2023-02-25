"""

RSA 25/2/23
This class handles transformations in 3d space from a plabe defined by 3 given points to the origin

"""

import math
from . import vectorthree as v3

class SpaceTransform(object):
    def __init__(self, central, linear, planar, log=False):
        # PUBLIC INTERFACE
        self.central = central
        self.linear = linear
        self.planar = planar

        #There are a set of transformations that need to be done in 1 order or the other to convert to the origin and then away.
        self._1_translation = v3.VectorThree(0,0,0)
        self._2_rotationXY = 0.0
        self._3_rotationXZ = 0.0
        self._4_rotationYZ = 0.0        
        #orthogonal unit axes       
        self.xAxis = v3.VectorThree(0,0,0)
        self.yAxis = v3.VectorThree(0,0,0)
        self.zAxis = v3.VectorThree(0,0,0)
        self.xOrthog = v3.VectorThree(0,0,0)
        self.yOrthog = v3.VectorThree(0,0,0)
        self.zOrthog = v3.VectorThree(0,0,0)
        self.centre = v3.VectorThree(0,0,0)

        self.M_PI = 3.14159265358979323846;

        self._calculate_transformation(log)

    
    ##### INTERNAL INTERFACE #######
    def _calculate_transformation(self,log):
        #First transformation is to the origin, a translation
        self._1_translation = self.central
        lin = self.linear
        pla = self.planar
        lin = v3.v3_subtract(lin,self._1_translation)
        pla = v3.v3_subtract(pla,self._1_translation)
        
        #Rotation vectors                    
        vR = v3.VectorThree(0,0,0)

        #Second transformation is to rotate the linear vector to make y=0                        
        self._2_rotationXY = self.get_rotation_angle(lin.A, lin.B)
        vR = self.rotate(lin.A, lin.B, self._2_rotationXY)
        lin.A = vR.A
        lin.B = vR.B
        vR = self.rotate(pla.A, pla.B, self._2_rotationXY)
        pla.A = vR.A
        pla.B = vR.B

        #Third transformation is to rotate the linear vector to make z=0            
        self._3_rotationXZ = self.get_rotation_angle(lin.A, lin.C)
        vR = self.rotate(lin.A, lin.C, self._3_rotationXZ)
        lin.A = vR.A
        lin.C = vR.B
        vR = self.rotate(pla.A, pla.C, self._3_rotationXZ)
        pla.A = vR.A
        pla.C = vR.B

        #Fourth transformation is to rotate the planar vector to make z=0    
        self._4_rotationYZ = self.get_rotation_angle(pla.B, pla.C)
        vR = self.rotate(pla.A, pla.C, self._4_rotationYZ) 
        pla.B = vR.A
        pla.C = vR.B

        #We have the transformations, now set up the orthogonal axes
        #Centre (0,0,0) should go to the central point            
        self.centre = self.apply_transformation(v3.VectorThree(0, 0, 0))
        self.xOrthog = self.apply_transformation(v3.VectorThree(1, 0, 0))
        self.xAxis = v3.v3_subtract(self.xOrthog,self.centre)
        self.yOrthog = self.apply_transformation(v3.VectorThree(0, 1, 0))
        self.yAxis = v3.v3_subtract(self.yOrthog, self.centre)
        self.zOrthog = self.apply_transformation(v3.VectorThree(0, 0, 1))
        self.zAxis = v3.v3_subtract(self.zOrthog, self.centre)

        #If these are othogonal the dot products will be zero, this is a debugging check
        if log:
            ortho = v3.VectorThree(1, 0, 0)
            o0 = ortho.dot_product(v3.VectorThree(0, 1, 0))
            o1 = self.xAxis.dot_product(self.yAxis)
            o2 = self.xAxis.dot_product(self.zAxis)
            o3 = self.zAxis.dot_product(self.yAxis)
            print(o0, o1, o2, o3)

    def get_rotation_angle(self, x, y):        
        theta = 0.0
        qStart = self._get_quadrant(x, y)
        vA = v3.VectorThree(0,0,0)
        axis = v3.VectorThree(0,0,0)
        mag = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
        if mag > 0.0001:
            vA.A = x
            vA.B = y
            axis.A = mag
            axis.B = 0
            theta = vA.get_angle(axis)
            #We want to go claockwise to the positive x-axis and this is just the absolute difference, so:        
            if qStart == 4 or qStart == 3:
                theta = 2 * self.M_PI - theta
            if theta < 0:
                theta = 2 * self.M_PI + theta
        
        return theta

    def rotate(self,x, y, angle):        
        angle_left = angle
        x_now = x
        y_now = y
        pointPrime = v3.VectorThree(0,0,0)
        while (angle_left > self.M_PI / 2):                    
            pointPrime = self._rotate_ninety(x_now, y_now)
            x_now = pointPrime.A
            y_now = pointPrime.B
            angle_left -= self.M_PI / 2        
        pointPrime = self._rotate_quadrant(x_now, y_now, angle_left)
        return pointPrime

    def apply_transformation(self, point):        
        pointPrime = v3.VectorThree(point.A, point.B, point.C)
        point2 = v3.VectorThree(0,0,0)

        rotationYZ_4 = self._4_rotationYZ;
        rotationXZ_3 = self._3_rotationXZ;
        rotationXY_2 = self._2_rotationXY;

        point2 = self.rotate(pointPrime.B, pointPrime.C, 2 * self.M_PI - rotationYZ_4)
        pointPrime.B = point2.A
        pointPrime.C = point2.B

        point2 = self.rotate(pointPrime.A, pointPrime.C, 2 * self.M_PI - rotationXZ_3)
        pointPrime.A = point2.A
        pointPrime.C = point2.B

        point2 = self.rotate(pointPrime.A, pointPrime.B, 2 * self.M_PI - rotationXY_2)
        pointPrime.A = point2.A
        pointPrime.B = point2.B

        pointPrime = v3.v3_add(pointPrime, self._1_translation)

        return pointPrime

    def reverse_transformation(self, point):        
        pointPrime = v3.VectorThree(point.A, point.B, point.C)
        point2 = v3.VectorThree(0,0,0)

        rotationYZ_4 = self._4_rotationYZ
        rotationXZ_3 = self._3_rotationXZ
        rotationXY_2 = self._2_rotationXY

        pointPrime = v3.v3_subtract(pointPrime, self._1_translation)

        point2 = self.rotate(pointPrime.A, pointPrime.B, rotationXY_2)
        pointPrime.A = point2.A
        pointPrime.B = point2.B

        point2 = self.rotate(pointPrime.A, pointPrime.C, rotationXZ_3)
        pointPrime.A = point2.A
        pointPrime.C = point2.B

        point2 = self.rotate(pointPrime.B, pointPrime.C, rotationYZ_4)
        pointPrime.B = point2.A
        pointPrime.C = point2.B

        return pointPrime
                        
##### INTERNAL FUNCTIONS ###
    def _get_quadrant(self,x, y):                           
        qStart = 1
        #first if it is on an axis
        if (x == 0 and y > 0):
            qStart = 1
        elif (x == 0 and y < 0):
            qStart = 4
        elif (y == 0 and x > 0):
            qStart = 1
        elif (y == 0 and x < 0):
            qStart = 2
        elif (x < 0 and y < 0):
            qStart = 3
        elif (x < 0 and y > 0):
            qStart = 2
        elif (y < 0 and x > 0):
            qStart = 4
        return qStart
    
    def _rotate_ninety(self, x_now, y_now):
        q = self._get_quadrant(x_now, y_now)
        q -= 1
        if (q == 0):
            q = 4;
        nextQ = v3.VectorThree(abs(y_now), abs(x_now), 0)
        if (q == 2):
            nextQ.A *= -1
        elif (q == 3):        
            nextQ.A *= -1
            nextQ.B *= -1    
        elif (q == 4):   
            nextQ.B *= -1        
        return nextQ
        
    def _rotate_quadrant(self,x, y, angle):        
        if (abs(angle) > 0.001):        
            v = v3.VectorThree(0,0,0)
            #This assumes an angle that is positive and less or = than 90 that may turn only into the next quadrant.            
            #Choose quadrants
            qStart = self._get_quadrant(x, y)
            mag = math.sqrt(math.pow(x, 2) + math.pow(y, 2)) #the length of the vector
            if (mag > 0.0001):            
                sinA = abs(y) / mag;
                angleA = math.asin(sinA); #this is the angle made with the x-axis from the original vector
                angleB = angleA - angle; #this is the angle made with the x-axis with the rotated vector
                qEnd = qStart
                if (qStart == 1):                
                    if (angle > angleA):                    
                        angleB = angle - angleA
                        qEnd = 4                                    
                elif (qStart == 2):                
                    angleB = angle + angleA
                    if (angleA + angle > self.M_PI / 2):                    
                        angleB = self.M_PI - (angleA + angle)
                        qEnd = 1                                    
                elif (qStart == 3):                
                    if (angle > angleA):                    
                        angleB = angle - angleA
                        qEnd = 2                                    
                else: #must be q4                
                    angleB = angle + angleA
                    if (angleA + angle > self.M_PI / 2):                    
                        angleB = self.M_PI - (angle + angleA)
                        qEnd = 3                                    
                x2 = math.cos(angleB) * mag
                y2 = math.sin(angleB) * mag
                if (qEnd == 2 or qEnd == 3):
                    x2 *= -1
                if (qEnd == 3 or qEnd == 4):
                    y2 *= -1
                v.A = x2;#Math.Round(x2, 8);
                v.B = y2;#Math.Round(y2, 8);            
            return v        
        else:        
            return v3.VectorThree(x, y, 0)
                        