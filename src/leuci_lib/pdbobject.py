"""
RSA 4/2/23


"""

import os
from os.path import exists
import urllib.request
from Bio.PDB.MMCIFParser import MMCIFParser        
from Bio.PDB.MMCIF2Dict import MMCIF2Dict
from Bio.PDB.PDBParser import PDBParser

import warnings
from Bio import BiopythonWarning
warnings.simplefilter('ignore', BiopythonWarning)

class PdbObject(object):
    def __init__(self, pdb_code, directory="", delete=False, cif=False):
        # PUBLIC INTERFACE
        self.pdb_code = pdb_code        
        self.em_code = ""
        self.ebi_link = f"https://www.ebi.ac.uk/pdbe/entry/pdb/{pdb_code}"                
        self.em_link = ""
        self.resolution = ""
        self.exp_method = ""
        self.map_header = {}
        # Private data
        self._ccp4_binary = None
        self._diff_binary = None        
        self.loaded = False        
        # PRIVATE INTERFACE
        self._directory = directory
        self._delete = delete
        self._cif=cif
        if cif:
            self._filepath = f"{directory}{pdb_code}.cif"
            self.pdb_link = f"https://www.ebi.ac.uk/pdbe/entry-files/download/{pdb_code}.cif"
        else:        
            self._filepath = f"{directory}{pdb_code}.pdb"
            self.pdb_link = f"https://www.ebi.ac.uk/pdbe/entry-files/download/pdb{pdb_code}.ent"
        
        self._filepath_ccp4 = f"{self._directory}{self.pdb_code}.ccp4"
        self._filepath_diff = f"{self._directory}{self.pdb_code}_diff.ccp4"
        self.ccp4_link = f"https://www.ebi.ac.uk/pdbe/entry-files/{self.pdb_code}.ccp4"
        self.diff_link = f"https://www.ebi.ac.uk/pdbe/entry-files/{self.pdb_code}_diff.ccp4"
                                
    def exists(self):
        if self.exists_pdb():
            if self.exists_map():
                return True
        
        return False
    
    def exists_pdb(self):
        if exists(self._filepath):
            return True
        else:
            return False
    
    def exists_map(self):
        self.load_pdb()
        if 'x-ray' in self.exp_method:
            if exists(self._filepath_ccp4) and exists(self._filepath_diff):                
                self.loaded = True
                return True        
            else:
                return False
        elif 'electron' in self.exp_method.lower():
            if exists(self._filepath_ccp4):
                self.loaded = True
                return True
            else:
                return False
        else:
            self.loaded = True
            return True # it doesn;t NOT exists anyway
    
    def download(self):
        if not self.exists_pdb():
            self.download_pdb()
        if not self.exists_map():
            self.download_map()
    
    def download_pdb(self):
        self._fetch_pdbdata()

    def download_map(self):
        if not self.loaded:
            self.load_pdb()            
        if 'x-ray' in self.exp_method:
            self._fetch_maplink_xray()            
        elif 'electron' in self.exp_method:
            self._fetch_maplink_em()
        self.loaded = True
    
    def load(self):
        self.load_pdb()
        if 'x-ray' in self.exp_method:            
            self.load_map()

    def load_pdb(self):
        if self._cif:
            structure = MMCIFParser().get_structure(self.pdb_code, self._filepath)
        else:
            structure = PDBParser(PERMISSIVE=True).get_structure(self.pdb_code, self._filepath)
        self._struc_dict = MMCIF2Dict(self._filepath)
        self.resolution = structure.header["resolution"]
        self.exp_method = structure.header["structure_method"]            

    def load_map(self):
        try:
            with open(self._filepath_ccp4, mode='rb') as file:
                self._ccp4_binary = file.read()        
            with open(self._filepath_diff, mode='rb') as file:
                self._diff_binary = file.read()
            self._create_mapheader()
            self.loaded = True
        except:        
            self.loaded = False

    #################################################
    ############ PRIVATE INTERFACE ##################
    #################################################
    def _fetch_pdbdata(self):
        try:
            print(self.pdb_link, self._filepath)            
            urllib.request.urlretrieve(self.pdb_link, self._filepath)                                
        except:            
            return False
        return True
        
    def _fetch_maplink_xray(self):                
        if not exists(self._filepath_ccp4):            
            urllib.request.urlretrieve(self.ccp4_link, self._filepath_ccp4)
        if not exists(self._filepath_diff):            
            urllib.request.urlretrieve(self.diff_link, self._filepath_diff)
        self.em_code = self.pdb_code

                        
    def _fetch_maplink_em(self):     
        """
        cif file
        EMDB EMD-6240 'associated EM volume' . 
        pdb file
        REMARK 900 RELATED ID: EMD-6240   RELATED DB: EMDB                              
        """
        self.em_code = ""
        with open(self._filepath,"r") as fr:
            lines = fr.read_lines()
            print(lines)
        
        self.diff_link = "" # there is no difference density for cryo-em   
        self.ccp4_link = "https://ftp.ebi.ac.uk/pub/databases/emdb/structures/EMD-" + self.em_code + "/map/emd_" + self.em_code + ".map.gz"        
        self.em_link = f"https://www.ebi.ac.uk/emdb/EMD-{self.em_code}"
        

    def _create_mapheader(self):
        headers = [] #https://www.ccp4.ac.uk/html/maplib.html#description
        headers.append(["01_NC","int",4])           # of Columns    (fastest changing in map)
        headers.append(["02_NR","int",4])           # of Rows
        headers.append(["03_NS","int",4])           # of Sections   (slowest changing in map)
        headers.append(["04_MODE","int",4])         # Data type   0 = signed bytes (from-128 lowest to 127 highest) 1 = Integer*2 2 = Image stored as Reals 3 = Complex Integer*2 4 = Complex Reals 5 == 0
        headers.append(["05_NCSTART","int",4])      # Number of first COLUMN  in map
        headers.append(["06_NRSTART","int",4])      # Number of first ROW     in map
        headers.append(["07_NSSTART","int",4])      # Number of first SECTION in map
        headers.append(["08_NX","int",4])           # Number of intervals along X
        headers.append(["09_NY","int",4])           # Number of intervals along Y
        headers.append(["10_NZ","int",4])           # Number of intervals along Z
        headers.append(["11_X_length","double",4])  # Cell Dimensions (Angstroms)
        headers.append(["12_Y_length","double",4])  #             "
        headers.append(["13_Z_length","double",4])  #             "
        headers.append(["14_Alpha","double",4])     # Cell Angles     (Degrees)
        headers.append(["15_Beta","double",4])      #             "
        headers.append(["16_Gamma","double",4])     #             "
        headers.append(["17_MAPC","int",4])         # Which axis corresponds to Cols.  (1,2,3 for X,Y,Z)
        headers.append(["18_MAPR","int",4])         # Which axis corresponds to Rows   (1,2,3 for X,Y,Z)
        headers.append(["19_MAPS","int",4])         # Which axis corresponds to Sects. (1,2,3 for X,Y,Z)
        headers.append(["20_AMIN","double",4])      # Minimum density value
        headers.append(["21_AMAX","double",4])      # Maximum density value
        headers.append(["22_AMEAN","double",4])     # Mean    density value    (Average)
        headers.append(["23_ISPG","int",4])         # Space group number
        headers.append(["24_NSYMBT","int",4])       # Number of bytes used for storing symmetry operators
        headers.append(["25_LSKFLG","int",4])       # Flag for skew transformation, =0 none, =1 if foll
                        
        i=0
        for header, typ,inc  in headers:
            if typ == "int":
                self.map_header[header] = int.from_bytes(self._ccp4_binary[i:i+4], byteorder='little', signed=False)
            i+=inc
        
                        
    def _create_mapdata_em(self):
        ccp4_link = ""
        em_link = ""


    def cleanup(self):
        pass
