import snappy
from Auxiliary_Functions import *
from Filter_QHS import *

UPPER_BOUND = 12 # This parameter is optimal in the sense that there is no new example ruled out up to 100.

def has_all_finite_dihedral_quotients(name,upper_bound):
    """
    This function tests if the fundamental group of a manifold has all finite dihedral quotients of order 2p for all p less than upper_bound.
    Input:  The SnapPy name of the manifold and the upper bound of the prime p for which the test is performed.
    Output: True if the fundamental group of the manifold has all finite dihedral quotients of order 2p for all num_primes initial primes p.
    """
    # Initialize the manifold and its fundamental group
    M = snappy.Manifold(name)
    G = M.fundamental_group()

    # Convert the snappy output to gap
    G_as_gap_string = G.gap_string()
    Ggap = gap(G_as_gap_string)


    check = True
    for p in primes(1,upper_bound):
        if check == True:
            D = DihedralGroup(p) # The dihedral group of order 2p
            try:
                epi_to_D = Ggap.GQuotients(D) # Compute all epimorphisms from G to D
                check = check and (len(epi_to_D) > 0)
            except RuntimeError:
                check = True
    return check

def finite_dihedral_test(file_name):
    # Initialize the list of QHS
    qhs_list = read_name(file_name)

    # Write heading of the table
    with open(HAKEN_QHS_DIHEDRAL_FILE, "w") as open_file:
        open_file.write("| Name | Finite Dihedral Test | Double Cover Test | Search Epimorphism |\n|---|---|---|---|\n")

    # Initialize the count of QHS for which the test rules OUT the infinite dihedral quotient
    count = 0
    for name in qhs_list:
        if has_all_finite_dihedral_quotients(name, UPPER_BOUND) == False:
            # if there is a finite dihedral quotient missing, write "No"
            count += 1
            with open(HAKEN_QHS_DIHEDRAL_FILE, "a") as open_file:
                open_file.write("| " + name + " | No | | |\n")
        else:
            # if we see all finite dihedral quotients up to the range, write "Maybe"
            with open(HAKEN_QHS_DIHEDRAL_FILE, "a") as open_file:
                open_file.write("| " + name + " | Maybe | | |\n")
    print("There are", count, "QHS without finite dihedral quotient of order 2p for p <", UPPER_BOUND, ".\n" )
