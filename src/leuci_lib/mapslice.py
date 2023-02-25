"""
RSA 25/2/23
This is primarily a function class that takes a reference to a map data object
It deals with cross sections of a matrix


"""

import os
from os.path import exists
import urllib.request
import struct
import json

class MapObject(object):
    def __init__(self, pdb_code, mobj):
        # PUBLIC INTERFACE
        self.pdb_code = pdb_code        
        self.mobj = mobj        

    def get_slice(central, linear, planar):
        pass

                
                                
    