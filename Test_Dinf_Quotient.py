import snappy
from Filter_QHS import *

UPPER_BOUND = 12 # This parameter is optimal in the sense that there is no new example ruled out up to 100.
HAKEN_QHS_DIHEDRAL_FILE = "HakenQHS_Dihedral_Data.txt"

def has_all_finite_dihedral_quotients(name,upper_bound):
    """
    This function tests if the fundamental group of a manifold has all finite dihedral quotients of order 2p for all p less than upper_bound.
    Input:  The SnapPy name of the manifold and the number of primes p for which the test will be performed
    Output: True if the fundamental group of the manifold has all finite dihedral quotients of order 2p for all num_primes initial primes p.
    """
    # Initialize the manifold and its fundamental group
    M = snappy.Manifold(name)
    G = M.fundamental_group()
    G_as_gap_string = G.gap_string()
    Ggap = gap(G_as_gap_string)

    check = True
    for p in primes(1,upper_bound):
        if check == True:
            D = DihedralGroup(p) # The dihedral group of order 2p
            try:
                epi_to_D = Ggap.GQuotients(D)
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

def double_cover_test(file_name):
    # read the content of HAKEN_QHS_DIHEDRAL_FILE
    with open(file_name, "r") as open_file:
        original_content = open_file.readlines()

    qhs_list = [line[find_nth_occurrence(line," ",1)+1:find_nth_occurrence(line," ",2)] for line in original_content[2:]]

    # Write heading of the table. The content of the file is overwritten here
    with open(file_name, "w") as open_file:
        open_file.write("| Name | Finite Dihedral Test | Double Cover Test | Search Epimorphism |\n|---|---|---|---|\n")

    count = 0
    for name in qhs_list:
        print(name)
        index_of_name = qhs_list.index(name)
        line = original_content[index_of_name+2]
        index_of_col = find_nth_occurrence(line,"|",3)
        if is_pos_b1_deg2cover(name) == False:
            count += 1
            with open(file_name, "a") as open_file:
                open_file.write(line[:index_of_col+2] + "No D_inf quotient" + line[index_of_col+1:])
        else:
            with open(file_name, "a") as open_file:
                open_file.write(line[:index_of_col+2] + "Maybe" + line[index_of_col+1:])

    print("There are", count, "QHS ruled out by testing the double covers.\n")

############################

def inverse_aff(affine_map):
    """
    Compute the inverse of an affine homeomorphism on R f(x) = m * x + b which is f^-1(x) = m^-1 * x - m^-1 * b
    Input:  A list of numbers [m,b] representing f(x) = m * x + b
    Output: [m^-1, -m^-1*b]
    """
    m = affine_map[0]
    b = affine_map[1]
    return [m^-1, -(m^-1) * b]

def compose_aff(f,g):
    """
    Given two affine maps f(x) and g(x) return f(g(x))
    """
    mg = g[0]
    bg = g[1]
    mf = f[0]
    bf = f[1]
    return [mf * mg, mf * bg + bf]

# def substitute_aff(word,hom):
#     """
#     Compute the image of a word in "a,b" or "a,b,c" under a candidate homomorphism
#     Input:  A word in "a,b,A,B" or "a,b,c,A, B,C" and a candidate homomorphism given as a list of two strings or three strings of affine maps
#     Output: The image of word under the homomorphism
#     """
#     # Initialize the output with the identity map
#     hom_word = [1,0]
#     # Initialize the homeomorphism in hom as ha,hb, and hc
#     ha = hom[0]
#     hb = hom[1]
#     if len(hom) == 3:
#         hc = hom[2]
#
#     for letter in word[::-1]:
#         if letter == "a":
#             hom_word = compose_aff(ha,hom_word)
#         elif letter == "b":
#             hom_word = compose_aff(hb, hom_word)
#         elif letter == "c":
#             hom_word = compose_aff(hc, hom_word)
#         elif letter == "A":
#             hom_word = compose_aff(inverse_aff(ha), hom_word)
#         elif letter == "B":
#             hom_word = compose_aff(inverse_aff(hb), hom_word)
#         elif letter == "C":
#             hom_word = compose_aff(inverse_aff(hc), hom_word)
#
#     return hom_word

def word_equation(word,hom):
    """
    Compute the equation defined by word given a homomorphism to the multiplicative group {1,-1}
    Input:  A word in "a,b,A,B" or "a,b,c,A,B,C" and a candidate homomorphism given as a list of two strings or three strings
    Output: A list of coefficients of
    """
    prod = 1
    coeff_a = 0
    coeff_b = 0
    coeff_c = 0
    for letter in word[::-1]:
        if letter == "a":
            coeff_a = coeff_a + prod
            prod = prod * hom[0]
        elif letter == "A":
            coeff_a = coeff_a - prod
            prod = prod * hom[0]
        if letter == "b":
            coeff_a = coeff_b + prod
            prod = prod * hom[1]
        elif letter == "B":
            coeff_a = coeff_b - prod
            prod = prod * hom[1]
        if letter == "c":
            coeff_a = coeff_c + prod
            prod = prod * hom[2]
        elif letter == "C":
            coeff_a = coeff_c - prod
            prod = prod * hom[2]
    if len(hom) == 2:
        return [coeff_a, coeff_b]
    else:
        return [coeff_a, coeff_b, coeff_c]

def relations_equation(relations, hom):
    return [word_equation(word,hom) for word in relations]

def substitute(word,hom):
    """
    Compute the image of a word in "a,b" or "a,b,c" under a candidate homomorphism
    Input: A word in "a,b,A,B" or "a,b,c,A,B,C" and a candidate homomorphism given as a list of two strings or three strings
    Output: The image of word under the homomorphism
    """
    new_word = ""
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
    Input: A word in "x,y"
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
    Input:  The number of generators of the group which is either 2 or 3
    Output: The list candidate homomorphisms from the group to the infinite dihedral group
    """
    if num_generators == 2:
        return [["x","y"],["x","xy"],["xy","x"]]
    else:
        return [["x","y",""],["x","","y"],["","x","y"],["x","xy",""],["x","","xy"],["","x","xy"],["xy","x",""],["xy","","x"],["","xy","x"]] + [["x","x","y"],["x","y","x"],["y","x","x"]] + [["x","y","xy"],["x","xy","y"],["y","x","xy"],["y","xy","x"],["xy","x","y"],["xy","y","x"]] + [["x","y","yx"],["x","yx","y"],["y","x","yx"],["y","yx","x"],["yx","x","y"],["yx","y","x"]] + [["x","x","xy"],["x","xy","x"],["xy","x","x"]] + [["x","xy","xy"],["xy","x","xy"],["xy","xy","x"]] + [["x","xy","yx"],["x","yx","xy"],["xy","x","yx"],["xy","yx","x"],["yx","x","xy"],["yx","xy","x"]]

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
    relations = G.relators()

    num_generators = len(G.generators())
    hom_list = candidate_hom(num_generators)
    check = False
    if num_generators == 2:
        for hom in hom_list:
            hom_relations = sub_relation(relations,hom)
            check = check or is_relations_hold(hom_relations)
        return check
    elif num_generators == 3:
        for hom in hom_list:
            hom_relations = sub_relation(relations,hom)
            check = check or is_relations_hold(hom_relations)
        if check:
            return check
        else:
            return None


def search_homomorphism(file_name):
    # read the content of HAKEN_QHS_DIHEDRAL_FILE
    with open(file_name, "r") as open_file:
        original_content = open_file.readlines()

    qhs_list = [line[find_nth_occurrence(line, " ", 1) + 1:find_nth_occurrence(line, " ", 2)] for line in
                original_content[2:]]

    # Write heading of the table. The content of the file is overwritten here
    with open(file_name, "w") as open_file:
        open_file.write("| Name | Finite Dihedral Test | Double Cover Test | Search Epimorphism |\n|---|---|---|---|\n")

    count = 0
    num_three_generated = 0
    for name in qhs_list:
        print(name)
        index_of_name = qhs_list.index(name)
        line = original_content[index_of_name + 2]
        # Find the index of the 4th column separation character "|"
        index_of_col = find_nth_occurrence(line, "|", 4)
        if is_pos_b1_deg2cover(name) > 0:
            if is_Dinfty_quotient(name) == False:
                with open(file_name, "a") as open_file:
                    open_file.write(line[:index_of_col + 2] + "No D_inf quotient" + line[index_of_col + 1:])
                count += 1
            elif is_Dinfty_quotient(name) == True:
                with open(file_name, "a") as open_file:
                    open_file.write(line[:index_of_col + 2] + "Yes D_inf quotient" + line[index_of_col + 1:])
            elif is_Dinfty_quotient(name) == None:
                with open(file_name, "a") as open_file:
                    open_file.write(line[:index_of_col + 2] + "Maybe" + line[index_of_col + 1:])
                num_three_generated += 1
        else:
            with open(file_name, "a") as open_file:
                open_file.write(line[:index_of_col + 2] + "No D_inf quotient" + line[index_of_col + 1:])

    print("There are", count, " additional QHS ruled out by searching for homomorphisms.")
    print("There are", num_three_generated, " 3-generated QHS left to test.")

search_homomorphism(HAKEN_QHS_DIHEDRAL_FILE)



