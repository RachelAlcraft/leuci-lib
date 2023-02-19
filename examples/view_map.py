"""
RSA 4/2/23

This loads and examines a map file and it's corresponding cif file given the pdb code
It will automatically check what kind of electron ddensity is available - xray or cryo em
"""

########## INPUTS #################
#pdb_code = "6kj3"
#pdb_code = "3j9e" #em
#pdb_code = "1ejg"
#pdb_code = "6eex"
pdb_code = "3nir"


########## INPUTS #################
from pathlib import Path
DATADIR = str(Path(__file__).resolve().parent )+ "/data/"
CODEDIR = str(Path(__file__).resolve().parent.parent )+ "/src/"
import sys
sys.path.append(CODEDIR)

import leuci_lib.pdbobject as pob


def show_pdb_map(pdb_code):
    print("Showing pdb map details")
    po = pob.PdbObject(pdb_code, directory=DATADIR, delete=False, cif=False)
    if not po.exists():
        po.download()
    po.load()
    if po.em_loaded:
        print(po.pdb_code)
        print(po.pdb_link)
        print(po.ebi_link)
        #print(po.map_code)
        print(po.resolution)
        print(po.exp_method)
        #print(po.map_source)
        #print(po.map_link)
        #print(po.map_header)
        print(po.em_loaded)
        print(po.map_header)
        print(po.header_as_string)
        po.load_values()
        if po.values_loaded:
            print(len(po.values),"=",po.map_header["01_NC"] * po.map_header["02_NR"] * po.map_header["03_NS"])
            print(po.values[0])    
            print(po.values[len(po.values)-1])
    #print(po._struc_dict["_pdbx_database_related.details"])
    print("~")
    

show_pdb_map(pdb_code)
