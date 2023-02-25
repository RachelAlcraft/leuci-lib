"""
RSA 25/2/23

This class handles 3d vectors
"""

import math

# class interface

class VectorThree(object):
    def __init__(self, a,b,c):    
        self.A = a
        self.B = b
        self.C = c        
        self.Valid = True
                        
    def make_from_key(self,key):                            
        key = key.Substring(1)
        key = key.Substring(0,key.Length-1)
        sk = key.Split(",")
        self.A = float(sk[0])
        self.B = float(sk[1])
        self.C = float(sk[2])        
        self.Valid = True
        
    def get_by_idx(self,idx):        
        if idx == 0:
            return self.A;
        elif idx == 1:
            return self.B;
        else:
            return self.C;
        
    def put_by_ind(self, idx, val):
        if idx == 0:
            self.A = val
        elif idx == 1:
            self.B = val
        else:
            self.C = val
        
    def distance(self,ABC):    
        dis = (self.A - ABC.A) * (self.A - ABC.A) + (self.B - ABC.B) * (self.B - ABC.B) + (self.C - ABC.C) * (self.C - ABC.C)
        return math.sqrt(dis)
    
    def magnitude(self):        
        mag = (self.A * self.A) + (self.B * self.B) + (self.C * self.C)
        return math.sqrt(mag)
                                                
    def get_angle(self, ABC):    
        BA = VectorThree(0 - self.A, 0 - self.B, 0 - self.C)
        BC = VectorThree(0 - ABC.A, 0 - ABC.B, 0 - ABC.C);
        dot = BA.dot_product(BC);
        magBA = BA.magnitude();
        magBC = BC.magnitude();
        cosTheta = dot / (magBA * magBC);
        theta = math.acos(cosTheta);
        return theta #in radians
    
    def dot_product(self, ABC):
        px = self.A * ABC.A
        py = self.B * ABC.B
        pz = self.C * ABC.C
        return px + py + pz
    
    def get_key(self,rnd = 4):
        strkey = "(" + str(round(self.A, rnd)) + ","
        strkey += str(round(self.B, rnd)) + ","  
        strkey += str(round(self.C, rnd)) + ")"  
        return strKey
            
    def get_point_pos(self, in_gap, in_width):    
        nums = int(in_width / in_gap)
        real_gap = in_width/nums
        real_width = real_gap * nums        
        PP = VectorThree(self.A, self.B, self.C)        
        PP.A = PP.A / real_gap
        PP.B = PP.B / real_gap
        PP.C = PP.C / real_gap
        adj = (real_width / (2 * real_gap))
        if (int)(nums % 2) != 0:
            adj -= 0.5
        PP.A += adj
        PP.B += adj                
        return PP

# static functions

def v3_add(ABC, PQR):        
    A = ABC.A + PQR.A
    B = ABC.B + PQR.B
    C = ABC.C + PQR.C
    return VectorThree(A,B,C)
    
def v3_subtract(ABC, PQR):        
    A = ABC.A - PQR.A
    B = ABC.B - PQR.B
    C = ABC.C - PQR.C
    return VectorThree(A,B,C)

def v3_divide(ABC, PQR):        
    A = ABC.A / PQR.A
    B = ABC.B / PQR.B
    C = ABC.C / PQR.C
    return VectorThree(A,B,C)

def v3_multiply(ABC, PQR):        
    A = ABC.A * PQR.A
    B = ABC.B * PQR.B
    C = ABC.C * PQR.C
    return VectorThree(A,B,C)
