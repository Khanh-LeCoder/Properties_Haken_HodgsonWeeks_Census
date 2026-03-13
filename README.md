## Compute properties of Haken manifolds from the Hodson Weeks census
The code and data in this project are in companion with the paper "Detecting embedded surfaces using finite quotients" with Tam Cheetam-West. 


In this project, we compute and record various properties of Haken QHS^3 from the Hodson--Weeks census. [The file](https://github.com/Khanh-LeCoder/Properties_Haken_HodgsonWeeks_Census/blob/main/Haken_List.txt) contains the list of Haken 3-manifold from the Hodgson Weeks census. The software Regina was used to certify Hakeness of these manifolds. We note that a few Haken manifold maybe missing from the list. Using SnapPy, we pick out Haken QHS^3 from the the list, compute and record various properties in [the file](https://github.com/Khanh-LeCoder/HodsonWeeksHakenProperties/blob/main/Haken_QHS3_Data.md). 

For each Haken QHS^3 $M$ from the list, we compute

1. Whether or not $\pi_1(M)$ admits an infinite dihedral quotient
2. The dimension of the $SL_2(C)$-character variety of $\pi_1(M)$


We note that the computations involving the $SL_2(C)$-character variety is time-consuming. To be able to handle a large number of examples, we set a timeout = 5s for the process of computing the ideal defining the character variety and of computing the dimension of the character variety. The output "Equation computation timed out" means that we can't compute the defining ideal of the variety in the time limit. The output "Dimension timed out" indicates that we do have the ideal defining the variety but can't compute the dimension. The output "None" indicates that we don't have the defining ideal of the character variety. 


