## Compute properties of Haken manifolds from the Hodson Weeks census

In this project, we compute and record various properties of Haken QHS^3 from the Hodson--Weeks census. [The file](https://github.com/Khanh-LeCoder/HodsonWeeksHakenProperties/blob/main/HakenList.txt) contains the list of Haken 3-manifold from the Hodgson Weeks census. The software Regina was used to certify Hakeness of these manifolds. We note that a few Haken manifold maybe missing from the list. Using SnapPy, we pick out Haken QHS^3 from the the list, compute and record various properties in [the file](https://github.com/Khanh-LeCoder/HodsonWeeksHakenProperties/blob/main/Haken_QHS3_Data.md). 

For each Haken QHS^3 $M$ from the list, we compute

1. The volume of $M$
2. The homology of $M$
3. Whether or not $\pi_1(M)$ admits an infinite dihedral quotient
4. The dimension of the $SL_2(C)$-character variety of $\pi_1(M)$
5. If the dimension of the $SL_2(C)$-character variety of $\pi_1(M)$ is zero, then whether or not there exists algebraic non-integral characters.

We note that the computations involving the $SL_2(C)$-character variety is time-consuming. To be able to handle a large number of examples, we set a timeout = 60s for the process of computing the ideal defining the character variety and of computing the dimension of the character variety. The output "Equation timed out!" means that we can't compute the defining ideal of the variety in out time limit. The output "Dimension timed out!" or "Dimension error" indicates that we do have the ideal defining the variety. However, the computation of the dimension is not possible within the time limit or sage threw an error in this computation.  

The file containing the ideal defining the character variety is too large to be made available on GitHub, but is available per request.

We will subsequently update the last column about ANI point on character variety. 
