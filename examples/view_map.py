"""
RSA 4/2/23

This loads and examines a map file and it's corresponding cif file given the pdb code
It will automatically check what kind of electron ddensity is available - xray or cryo em
"""

########## INPUTS #################

pdb_code = "6kj3"
pdb_code = "3j9e"
#pdb_code = "1ejg"
#pdb_code = "6eex"


########## INPUTS #################
from pathlib import Path
DATADIR = str(Path(__file__).resolve().parent )+ "/data/"
CODEDIR = str(Path(__file__).resolve().parent.parent )+ "/src/"
import sys
sys.path.append(CODEDIR)

import leuci_lib.pdbobject as pob


def show_pdb_map(pdb_code):
    print("Showing pdb map details")
    po = pob.PdbObject(pdb_code, directory=DATADIR, delete=False, cif=True)
    if not po.exists():
        po.download()
    po.load()    
    print(po.pdb_code)
    print(po.pdb_link)
    print(po.ebi_link)
    #print(po.map_code)
    print(po.resolution)
    print(po.exp_method)
    #print(po.map_source)
    #print(po.map_link)
    #print(po.map_header)
    print(po.loaded)
    print(po.map_header)
    #print(po._struc_dict["_pdbx_database_related.details"])
    print("~")
    

show_pdb_map(pdb_code)
