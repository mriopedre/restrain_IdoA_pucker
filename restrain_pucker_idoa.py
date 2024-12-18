# This script generates dihedral restraints for monosaccharide puckering angles in GROMACS topology files.
# It identifies atom selections for the sugar molecule from an `.itp` file and formats the dihedral restraints for inclusion in the topology file.

# The formatting is as follows:

# #ifdef PUCKER
# [ dihedral_restraints ]
#    C1    O5    C5    C4     1    -60.0      2.5       DIHRES_FC 
#    O5    C5    C4    C3     1     60.0      2.5       DIHRES_FC 
#    C5    C4    C3    C2     1    -60.0      2.5       DIHRES_FC 
#    C4    C3    C2    C1     1     60.0      2.5       DIHRES_FC  
#    C3    C2    C1    O5     1    -60.0      2.5       DIHRES_FC 
#    C2    C1    O5    C5     1     60.0      2.5       DIHRES_FC  
# #endif   

#Usage:
#    - Provide the path to the `.itp` file containing the sugar topology.
#    - The script will parse the atom definitions and output formatted restraints.
#    - Copy the printed restraints to the end of the `.itp` file.

#Note:
#    - In GLYCAM, IdoA (Iduronic acid) is denoted as YuA.
#    - In CHARMM, it is denoted as AIDOA.


import numpy as np
from ordered_set import OrderedSet as oset

def get_dict_selections(file):
    """
    Parse the `.itp` file to extract atom indices for relevant dihedral restraints.

    Args:
        file (str): Path to the `.itp` file.

    Returns:
        dict: A dictionary where keys are atom names and residue IDs, and 
              values are the corresponding atom indices.
    """

    with open(file, 'r') as f:
        lines = f.readlines()

    start = False
    dictionary = {}
    for i, line in enumerate(lines):
        # Stop parsing when reaching the bonds section
        if '[ bonds ]' in lines[i+1]:
            break

        if start:
            line = line.split()
            # Look for IdoA residues (YuA in GLYCAM, AIDOA in CHARMM)
            if any(idoa in line[3] for idoa in ['YuA', 'AIDOA']):
                # Check for relevant atom names
                if any(atom in line[4] for atom in ['C1', 'O5', 'C5', 'C4', 'C2', 'C3']):
                    string = f"{line[4]}_{line[2]}"  # AtomName_ResidueID
                    dictionary[string] = line[0]  # Atom index

        # Start parsing at the atoms section
        if '[ atoms ]' in lines[i-1]:
            start = True
        
    return dictionary

def format_restraint(dictio):
    """
    Format the dihedral restraints for inclusion in the `.itp` file.

    Args:
        dictio (dict): Dictionary of atom indices from `get_dict_selections`.

    Prints:
        str: Formatted dihedral restraints to be included in the topology file.
    """

    string = '#ifdef PUCKER\n'
    string += '[ dihedral_restraints ]\n'
    resids = oset([k.split('_')[1] for k in dictio.keys()])  # Unique residue IDs

    for resid in resids:
        # Extract atom indices for the given residue
        c1 = dictio[f'C1_{resid}']
        o5 = dictio[f'O5_{resid}']
        c5 = dictio[f'C5_{resid}']
        c4 = dictio[f'C4_{resid}']
        c3 = dictio[f'C3_{resid}']
        c2 = dictio[f'C2_{resid}']

        # Add dihedral restraints
        string += f'    {c1}   {o5}   {c5}   {c4}     1    -60.0      2.5       DIHRES_FC ; C1    O5    C5    C4\n'
        string += f'    {o5}   {c5}   {c4}   {c3}     1     60.0      2.5       DIHRES_FC ; O5    C5    C4    C3\n'
        string += f'    {c5}   {c4}   {c3}   {c2}     1    -60.0      2.5       DIHRES_FC ; C5    C4    C3    C2\n'
        string += f'    {c4}   {c3}   {c2}   {c1}     1     60.0      2.5       DIHRES_FC ; C4    C3    C2    C1\n'
        string += f'    {c3}   {c2}   {c1}   {o5}     1    -60.0      2.5       DIHRES_FC ; C3    C2    C1    O5\n'
        string += f'    {c2}   {c1}   {o5}   {c5}     1     60.0      2.5       DIHRES_FC ; C2    C1    O5    C5\n'

    string += '#endif'
    print(string)


# Example usage: 
# Just select the itp with the topology of the sugar
# The restraint is printed, and can be copy pasted at the end of the file

file = 'EXAMPLE_PATH_TO_FILE.itp'

dictio = get_dict_selections(file)
format_restraint(dictio)
