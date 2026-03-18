## Compute properties of Haken manifolds from the Hodson Weeks census
The code and data in this project are in companion with the paper "Detecting embedded surfaces using finite quotients" with Tam Cheetham-West. 


In this project, we compute and record various properties of Haken QHS^3 from the Hodson--Weeks census. [The file "Haken_List.txt"](https://github.com/Khanh-LeCoder/Properties_Haken_HodgsonWeeks_Census/blob/main/Haken_List.txt) contains the list of Haken 3-manifold from the Hodgson Weeks census. The software Regina was used to certify Hakeness of these manifolds. We note that a few Haken manifold maybe missing from the list. Using SnapPy, we pick out Haken QHS^3 from the the list, compute and record various properties in [the file "Haken_QHS_Data.md"](https://github.com/Khanh-LeCoder/Properties_Haken_HodgsonWeeks_Census/blob/main/Haken_QHS_Data.md)

For each Haken QHS^3 $M$ from the list, we compute

1. Whether or not $\pi_1(M)$ admits an infinite dihedral quotient
2. The dimension of the $SL_2(C)$-character variety of $\pi_1(M)$

Here is the brief summary of the files in this project:
* Code:
    1. Filter_QHS.py: The codes here are used to produce from the list of Haken 3-manifolds in Haken_List.txt the list Haken QHS in Haken_QHS_List.txt
    2. Infinite_Dihedral_Quotient.py: The codes here are used to produce from Haken_QHS_List.txt the result in the file HakenQHS_Dihedral_Data.md which records whether 3-manifolds in the list admits a infinite dihedral quotient. 
    3. SL2C_Char_Var_Dim.py: The codes here are used to produce from Haken_QHS_List.txt the result in the file Char_Var_Data.md which records whether 3-manifolds in the lists admits a curve in its SL2C-character variety.
    4. main.py: The codes here are used to combined the data from both files HakenQHS_Dihedral_Data.md and Char_Var_Data.md into a single file.
    5. Auxiliary_Functions.py: The file contains some auxilary functions that are used to process text files. 
* Data:
    1. Haken_List.txt is a (non exhaustive) list of Haken 3-manfiold from the Hodgson-Weeks census
    2. Haken_QHS_List.txt is a (non exhaustive) list of Haken QHS from the Hodgson-Weeks census
    3. HakenQHS_Dihedral_Data.md records whether 3-manifolds in the list admits a infinite dihedral quotient.
    4. Equation_Data.md records the result of computing the definining ideals of the SL2C-char. var. This file also contains the equation it is computed. Therefore, it is quite large.
    5. Char_Var_Data.md records the result of computing the dimension of the SL2C-char. var.
    6. Haken_QHS_Data.md records the combined result of all tests.     

We note that the computations involving the $SL_2(C)$-character variety is time-consuming. To be able to handle a large number of examples, we set a timeout = 5s for the process of computing the ideal defining the character variety and of computing the dimension of the character variety. The output "Equation computation timed out" means that we can't compute the defining ideal of the variety in the time limit. The output "Dimension timed out" indicates that we do have the ideal defining the variety but can't compute the dimension. The output "None" indicates that we don't have the defining ideal of the character variety. 


