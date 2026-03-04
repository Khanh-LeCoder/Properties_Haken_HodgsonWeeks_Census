import snappy
from Filter_QHS import *

UPPER_BOUND = 20
HAKEN_QHS_DIHEDRAL_FILE = "HakenQHS_Dihedral_Data.txt"

def has_all_finite_dihedral_quotients(name,upper_bound):
    """
    This function tests if the fundamental group of a manifold has all finite dihedral quotients of order 2p for all p less than upper_bound.
    Input:  The SnapPy name of the manifold and the number of primes p for which the test will be performed
    Output: True if the fundamental group of the manifold has all finite dihedral quotients of order 2p for all num_primes initial primes p.
    """
    # Initialize the manifold and its fundamental group
    M = snappy.Manifold(name)
    G = gap(M.fundamental_group().gap_string())

    check = True
    for p in primes(1,upper_bound):
        if check == True:
            D = DihedralGroup(p) # The dihedral group of order 2p
            try:
                epi_to_D = G.GQuotients(D)
                check = check and (len(epi_to_D) > 0)
            except RuntimeError:
                check = True
    return check

def finite_dihedral_test(file_name):
    # Initialize the list of QHS
    qhs_list = read_name(file_name)
    print(len(qhs_list))
    # Write heading of the table
    with open(HAKEN_QHS_DIHEDRAL_FILE, "w") as open_file:
        open_file.write("| Name | Finite Dihedral Test | Double Cover Test | Search Epimorphism |\n|---|---|---|---|\n")

    # Initialize the count of QHS for which the test rules OUT the infinite dihedral quotient
    count = 0
    for name in qhs_list:
        print(name)
        if has_all_finite_dihedral_quotients(name, UPPER_BOUND) == False:
            count += 1
            with open(HAKEN_QHS_DIHEDRAL_FILE, "a") as open_file:
                open_file.write("| " + name + " | No D_inf quotient | | |\n")
        else:
            with open(HAKEN_QHS_DIHEDRAL_FILE, "a") as open_file:
                open_file.write("| " + name + " | Maybe | | |\n")
    print("There are", count, "QHS without finite dihedral quotient of order 2p for p <", UPPER_BOUND, ".\n" )

###########################

def sum_b1_deg2cover(name):
    """
    Input: The name of a 3-manifold
    Output: The sum of the betti number of all degree two cover
    """
    # Initialize M and compute all of its degree 2 covers
    M = snappy.Manifold(name)
    cov2 = M.covers(2)

    # compute the sum of b1 of all degree 2 cover of M
    sum_b1 = 0
    if len(cov2) > 0:
        for N in cov2:
            sum_b1 += N.homology().betti_number()
    return sum_b1

def is_pos_b1_deg2cover(name):
    return sum_b1_deg2cover(name) > 0

def degree2_cover_test(file_name):
    # read the content of HAKEN_QHS_DIHEDRAL_FILE
    with open(file_name, "r") as open_file:
        original_content = open_file.readlines()

    qhs_list = [line[find_nth_occurrence(line," ",1)+1:find_nth_occurrence(line," ",2)] for line in original_content[2:]]

    # Write heading of the table. The content of the file is overwritten here
    with open(file_name, "w") as open_file:
        open_file.readlines("| Name | Finite Dihedral Test | Double Cover Test | Search Epimorphism |\n|---|---|---|---|\n")

    for name in qhs_list:
        print(name)
        index_of_name = qhs_list.index()
        line = original_content[index_of_name]
        index_of_col = find_nth_occurrence(line,"|",3)
        count = 0
        if is_pos_b1_deg2cover(name) == False:
            count += 1
            with open(file_name, "a") as open_file:
                open_file.write(line[:index_of_col+2] + "No D_inf quotient" + line[index_of_col+1:])
        else:
            with open(file_name, "a") as open_file:
                open_file.write(line[:index_of_col+2] + "Maybe" + line[index_of_col+1:])
        print("There are", count, "QHS ruled out by testing the double covers.\n")


############################

def substitute(word,hom):
    """
    Input: A word and a candidate homomorphism 
    Output: The image of word under the homomorphism
    """
    new_word = ""
    if len(hom) == 2:
        for letter in word:
            if letter == "a":
                new_word += hom[0]
            elif letter == "A":
                new_word += hom[0][::-1]
            elif letter == "b":
                new_word += hom[1]
            elif letter == "B":
                new_word += hom[1][::-1]
    else: 
        for letter in word:
            if letter == "a":
                new_word += hom[0]
            elif letter == "A":
                new_word += hom[0][::-1]
            elif letter == "b":
                new_word += hom[1]
            elif letter == "B":
                new_word += hom[1][::-1]
            elif letter == "c":
                new_word += hom[2]
            elif letter == "C":
                new_word += hom[2][::-1]
    return new_word

def sub_relation(relations,hom):
    """
    Input: A list of relations and a candidate homomorphism
    Output: A list of images of the relations under the homorphism
    """
    return [substitute(word,hom) for word in relations]

def reduce_dihedral(word):
    """
    Input: A word
    Output: A reduced word in the infinite dihedral group
    """
    while word.find('xx') != -1 or word.find('yy') != -1:
        if word.find('xx') != -1:
            index = word.find('xx')
            word = word[:index] + word[index + 2:]
        if word.find('yy') != -1:
            index = word.find('yy')
            word = word[:index] + word[index + 2:]
    return word

def candidate_hom(num_generators):
    """
    Input: 
    Output:
    """
    if num_generators == 2:
        return [["x","y"],["x","xy"],["xy","x"]]
    else:
        return [["y","x","x"],["x","y","x"],["x","x","y"]] + [["xy","x","x"],["x","xy","x"],["x","x","xy"]] + [["x","xy","xy"],["xy","x","xy"],["xy","xy","x"]] + [["x","y","xy"],["y","xy","x"],["xy","x","y"],["x","xy","y"],["xy","y","x"],["y","x","xy"]] + [["x","y","yx"],["y","yx","x"],["yx","x","y"],["x","yx","y"],["yx","y","x"],["y","x","yx"]]

def is_trivial(word):
    """
    Input: A word
    Output: True if the word is empty False otherwise
    """
    if len(word) == 0:
        return True
    else:
        return False

def is_relations_hold(hom_relations):
    """
    Input: the set relations after applying the homomorphism
    Output: True if all relations are trivial
    """
    check = True
    for word in hom_relations:
        check = check and is_trivial(reduce_dihedral(word))
    return check

def is_Dinfty_quotient(name):
    """
    Input:
    Output:
    """
    M = snappy.Manifold(name)
    G = M.fundamental_group()
    num_generators = len(G.generators())
    relations = G.relators()
    hom_list = candidate_hom(num_generators)

    check = False
    for hom in hom_list:
        hom_relations = sub_relation(relations,hom)
        check = check or is_relations_hold(hom_relations)

    return check 



