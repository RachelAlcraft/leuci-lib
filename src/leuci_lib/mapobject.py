"""
RSA 4/2/23
https://pynative.com/make-python-class-json-serializable/#:~:text=Use%20toJSON()%20Method%20to%20make%20class%20JSON%20serializable&text=So%20we%20don't%20need,Python%20Object%20to%20JSON%20string.

"""

import os
from os.path import exists
import urllib.request
import struct
import json

class MapObject(object):
    def __init__(self, pdb_code):
        # PUBLIC INTERFACE
        self.pdb_code = pdb_code        
        self.em_code = ""        
        self.em_link = ""
        self.resolution = ""
        self.exp_method = ""
        self.map_header = {}
        self.header_as_string = ""        
        self.values = [] 
        self.diff_values = []        
        #self.values = {} #possible alternative if there are many 0s but it is much slower for high res xray data eg 4rek
        #self.diff_values = {}
        self.ebi_link = f"https://www.ebi.ac.uk/pdbe/entry/pdb/{pdb_code}"                
        self.ccp4_link = f"https://www.ebi.ac.uk/pdbe/entry-files/{self.pdb_code}.ccp4"
        self.diff_link = f"https://www.ebi.ac.uk/pdbe/entry-files/{self.pdb_code}_diff.ccp4"
        self.pdb_link = ""

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
    
    def fromJson(self, jsndic):
        self.pdb_code = jsndic["pdb_code"]
        self.em_code = jsndic["em_code"]
        self.em_link = jsndic["em_link"]
        self.resolution = jsndic["resolution"]
        self.exp_method = jsndic["exp_method"]
        self.map_header = jsndic["map_header"]
        self.header_as_string = jsndic["header_as_string"]
        self.values = jsndic["values"]
        self.diff_values = jsndic["diff_values"]
        #self.values = {} #possible alternative if there are many 0s but it is much slower for high res xray data eg 4rek
        #self.diff_values = {}
        self.ebi_link = jsndic["ebi_link"]
        self.ccp4_link = jsndic["ccp4_link"]
        self.diff_link = jsndic["diff_link"]
        self.pdb_link = jsndic["pdb_link"]
                                
    