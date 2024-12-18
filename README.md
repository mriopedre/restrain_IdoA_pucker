# restrain_IdoA_pucker

This script generates dihedral restraints for monosaccharide puckering angles in GROMACS topology files.
It identifies atom selections for the sugar molecule from an `.itp` file and formats the dihedral restraints for inclusion in the topology file.

IMPORTANT - the restraints are for 1C4 conformation. for 4C1, changing the "-60" values to "60" and viceversa is enough.

The formatting is as follows:

```plaintext
#ifdef PUCKER
[ dihedral_restraints ]
   C1    O5    C5    C4     1    -60.0      2.5       DIHRES_FC
   O5    C5    C4    C3     1     60.0      2.5       DIHRES_FC
   C5    C4    C3    C2     1    -60.0      2.5       DIHRES_FC
   C4    C3    C2    C1     1     60.0      2.5       DIHRES_FC
   C3    C2    C1    O5     1    -60.0      2.5       DIHRES_FC
   C2    C1    O5    C5     1     60.0      2.5       DIHRES_FC
#endif
```

Usage:
   - Provide the path to the `.itp` file containing the sugar topology.
   - The script will parse the atom definitions and output formatted restraints.
   - Copy the printed restraints to the end of the `.itp` file.

Note:
   - In GLYCAM, IdoA (Iduronic acid) is denoted as YuA.
   - In CHARMM, it is denoted as AIDOA.

