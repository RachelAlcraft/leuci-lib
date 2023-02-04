"""
RSA 4/2/23

This loads and examines a map file and it's corresponding cif file given the pdb code
It will automatically check what kind of electron ddensity is available - xray or cryo em
"""

########## INPUTS #################

pdb_code = "4rek"


########## INPUTS #################


import leuci_lib.pdbobject as pob

def show_pdb_map(pdb_code):
    print("Showing pdb map details")
    po = pob.PdbObject(pdb_code)
    print(po.pdb_code)
    print(po.pdb_link)
    print(po.ebi_link)
    #print(po.map_code)
    print(po.resolution)
    #print(po.map_source)
    #print(po.map_link)
    #print(po.map_header)
    print(po.valid)
    print("~")
    

show_pdb_map(pdb_code)
