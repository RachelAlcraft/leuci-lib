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
    def __init__(self, pdb_code, location="", delete=True, cif=False):
        # PUBLIC INTERFACE
        self.pdb_code = pdb_code        
        self.ebi_link = f"https://www.ebi.ac.uk/pdbe/entry/pdb/{pdb_code}"
        self.cif_link = f"https://www.ebi.ac.uk/pdbe/entry-files/download/{pdb_code}.cif"
        self.pdb_link = f"https://www.ebi.ac.uk/pdbe/entry-files/download/pdb{pdb_code}.ent"
        self.ccp4_link = f"https://www.ebi.ac.uk/pdbe/entry-files/{self.pdb_code}.ccp4"
        self.diff_link = f"https://www.ebi.ac.uk/pdbe/entry-files/{self.pdb_code}_diff.ccp4"
        self.resolution = ""
        self.exp_method = ""
        self.map_header = {}
        # Private data
        self._ccp4_binary = None
        self._diff_binary = None        
        # PRIVATE INTERFACE
        self._location = location
        self._delete = delete
        self._cif=cif
        self._filepath_cif = f"{location}{pdb_code}.cif"
        self._filepath_pdb = f"{location}{pdb_code}.pdb"
        self._filepath_ccp4 = f"{location}{pdb_code}.ccp4"
        self._filepath_diff = f"{location}{pdb_code}_diff.ccp4"
        
        if cif:
            self.valid = self._fetch_pdbdata_cif()
        else:
            self.valid = self._fetch_pdbdata_pdb()        
        
        if 'x-ray' in self.exp_method:
            self._fetch_maplink_xray()
            self._create_mapheader()
        else:
            self._fetch_maplink_em()
            self._create_mapdata_em()


    def getHeaders(self):
        mhs = []
        for mh in self.map_header.items():
            mhs.append(mh)
        return mhs

    #################################################
    ############ PRIVATE INTERFACE ##################
    #################################################
    def _fetch_pdbdata_cif(self):        
        try:
            if exists(self._filepath_cif) and self._delete:
                os.remove(self._filepath_cif)
            if not exists(self._filepath_cif):            
                urllib.request.urlretrieve(self.cif_link, self._filepath_cif)                    
            structure = MMCIFParser().get_structure(self.pdb_code, self._filepath_cif)
            self._struc_dict = MMCIF2Dict(self._filepath_cif)
            self.resolution = structure.header["resolution"]
            self.exp_method = structure.header["structure_method"]
            if self._delete and exists(self._filepath_cif):
                os.remove(self._filepath_cif)  # tidy up
        except:
            if self._delete and exists(self._filepath_cif):
                os.remove(self._filepath_cif)  # tidy up
            return False
        return True

    def _fetch_pdbdata_pdb(self):        
        try:
            if exists(self._filepath_pdb) and self._delete:
                os.remove(self._filepath_pdb)
            if not exists(self._filepath_pdb):
                urllib.request.urlretrieve(self.pdb_link, self._filepath_pdb)                
            structure = PDBParser(PERMISSIVE=True).get_structure(self.pdb_code, self._filepath_pdb)
            self._struc_dict = MMCIF2Dict(self._filepath_pdb)
            self.resolution = structure.header["resolution"]
            self.exp_method = structure.header["structure_method"]
            if self._delete and exists(self._filepath_pdb):
                os.remove(self._filepath_pdb)  # tidy up
        except:
            if self._delete and exists(self._filepath_pdb):
                os.remove(self._filepath_pdb)  # tidy up
            return False
        return True
    
    def _fetch_maplink_xray(self):                
        if not exists(self._filepath_ccp4):            
            urllib.request.urlretrieve(self.ccp4_link, self._filepath_ccp4)
        with open(self._filepath_ccp4, mode='rb') as file:
            self._ccp4_binary = file.read()

        if not exists(self._filepath_diff):            
            urllib.request.urlretrieve(self.diff_link, self._filepath_diff)
        with open(self._filepath_diff, mode='rb') as file:
            self._diff_binary = file.read()
        
        

    def _fetch_maplink_em(self):        
        em_link = ""

    def _create_mapheader(self):
        i=0
        self.map_header["01_NC"] = int.from_bytes(self._ccp4_binary[i:i+4], byteorder='little', signed=False)
        i+=4
        self.map_header["02_NR"] = int.from_bytes(self._ccp4_binary[i:i+4], byteorder='little', signed=False)
        i+=4
        self.map_header["03_NS"] = int.from_bytes(self._ccp4_binary[i:i+4], byteorder='little', signed=False)
        i+=4
        self.map_header["04_MODE"] = int.from_bytes(self._ccp4_binary[i:i+4], byteorder='little', signed=False)
        
        
        
    def _create_mapdata_em(self):
        ccp4_link = ""
        em_link = ""


    def cleanup(self):
        pass
