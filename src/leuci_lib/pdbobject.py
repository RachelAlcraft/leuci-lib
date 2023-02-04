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
    def __init__(self, pdb_code, location="", delete=True):
        # PUBLIC INTERFACE
        self.pdb_code = pdb_code        
        self.ebi_link = f"https://www.ebi.ac.uk/pdbe/entry/pdb/{pdb_code}"
        self.cif_link = f"https://www.ebi.ac.uk/pdbe/entry-files/download/{pdb_code}.cif"
        self.pdb_link = f"https://www.ebi.ac.uk/pdbe/entry-files/download/pdb{pdb_code}.ent"
        self.resolution = ""
        # PRIVATE INTERFACE
        self._location = location
        self._delete = delete
        self._filepath_cif = f"{location}{pdb_code}.cif"
        self._filepath_pdb = f"{location}{pdb_code}.pdb"

        self.valid = self._fetch_pdbdata_pdb()
        self._fetch_maplink()
        self._fetch_mapdata()

    #################################################
    ############ PRIVATE INTERFACE ##################
    #################################################
    def _fetch_pdbdata_cif(self):        
        try:
            if not exists(self._filepath_cif):            
                    urllib.request.urlretrieve(self.cif_link, self._filepath_cif)                            
                    return False
            structure = MMCIFParser().get_structure(self.pdb_code, self._filepath_cif)
            self._struc_dict = MMCIF2Dict(self._filepath_cif)
            self.resolution = structure.header["resolution"]
            if self._delete and exists(self._filepath_cif):
                os.remove(self._filepath_cif)  # tidy up
        except:
            return False
        return True

    def _fetch_pdbdata_pdb(self):        
        try:
            if not exists(self._filepath_pdb):            
                urllib.request.urlretrieve(self.pdb_link, self._filepath_pdb)                
            structure = PDBParser(PERMISSIVE=True).get_structure(self.pdb_code, self._filepath_pdb)
            self._struc_dict = MMCIF2Dict(self._filepath_pdb)
            self.resolution = structure.header["resolution"]
            if self._delete and exists(self._filepath_pdb):
                os.remove(self._filepath_pdb)  # tidy up
        except:
            return False
        return True
    
    def _fetch_maplink(self):
        ccp4_link = ""
        em_link = ""

    def _fetch_mapdata(self):
        ccp4_link = ""
        em_link = ""
