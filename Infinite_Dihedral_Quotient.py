import snappy
from Auxiliary_Functions import *
from Filter_QHS import *

# The file "HakenQHS_Dihedral_Data.md" contains the result of testing for infinite dihedral quotients
HAKEN_QHS_DIHEDRAL_FILE = "HakenQHS_Dihedral_Data.md"

def write_QHS_Dihedral_data(input_file, output_file):
    """
    Read the content of "Haken_QHS_List.txt" and write it to "Haken_QHS_Dihedral_Data.md
    Input:  HAKEN_QHS_FILE
    Output: HAKEN_QHS_DIHEDRAL_FILE
    """
    # Read the list of manifolds from file_name
    mfld_list = read_name(input_file)

    # Write the table heading
    with open(output_file, "w") as open_file:
        open_file.write("| Name | Double Cover Test | Search Epimorphism |\n|---|---|---|\n")

    with open(output_file, "a") as open_file:
        for name in mfld_list:
            open_file.write("| " + name + " | | |\n")

    print("There are", len(mfld_list), "Haken QHS.")

def sum_b1_deg2cover(name):
    """
    Input:  The name of a 3-manifold
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
    """
    The function tests if the manifold has positive sum of the first betti number of all double covers
    """
    return sum_b1_deg2cover(name) > 0

def write_double_cover_test(file_name):
    """
    The function performs the double cover test which checks if the sum of the first betti number in all double covers is positive. The function outputs the result of the test in the file HakenQHS_Dihedral_Data.md
    """
    # read the content of HAKEN_QHS_DIHEDRAL_FILE
    with open(file_name, "r") as open_file:
        original_content = open_file.readlines()

    # read the content of the first column which contains the names of QHS
    qhs_list = [line[find_nth_occurrence(line," ",1)+1:find_nth_occurrence(line," ",2)] for line in original_content[2:]]

    # Write heading of the table. The content of the file is overwritten here
    with open(file_name, "w") as open_file:
        open_file.write("| Name | Double Cover Test | Search Epimorphism |\n|---|---|---|\n")

    count = 0
    for name in qhs_list:
        index_of_name = qhs_list.index(name)
        line = original_content[index_of_name+2]
        index_of_col = find_nth_occurrence(line,"|",2)
        if is_pos_b1_deg2cover(name) == False:
            count += 1
            with open(file_name, "a") as open_file:
                open_file.write(line[:index_of_col+2] + "No" + line[index_of_col+1:])
        else:
            with open(file_name, "a") as open_file:
                open_file.write(line[:index_of_col+2] + "Maybe" + line[index_of_col+1:])

    print("There are", count, "QHS ruled out by testing the double covers.\n")

# Now we use these functions to obtain a system equations over Z coming from letting a,b,c be f(x) = ma * x + va, g(x) = mb * x + vb, h(x) = mc * x + vc

def evaluate_Z2_hom(word,hom):
    """
    Given a word in a,b,A,B or in a,b,c,A,B,C and a candidate homomorphism from a group G to {1,-1} compute the image of word under the homomorphism
    Input:  a string in a,b,A,B or in a,b,c,A,B,C for word and a list of 2 or 3 elements each is either 1 or -1 representing the image of a,b or c under the candidate homorphism
    Output: Either 1 or -1
    """
    prod = 1
    for letter in word:
        if letter == "a" or letter == "A":
            prod = prod * hom[0]
        elif letter == "b" or letter == "B":
            prod = prod * hom[1]
        elif letter == "c" or letter == "C":
            prod = prod * hom[2]
    return prod

def eval_rel_Z2_hom(relations,hom):
    return [evaluate_Z2_hom(word,hom) for word in relations]

def candidate_Z2_hom(num_generators):
    """
    Return a list of list of candidate homomorphism from a 2- or 3- generated group to the multiplicative group {1,-1}
    """
    if num_generators == 2:
        return [[1,1],[1,-1],[-1,1],[-1,-1]]
    elif num_generators == 3:
        return [[1,1,1],[1,1,-1],[1,-1,1],[1,-1,-1],[-1,1,1],[-1,1,-1],[-1,-1,1],[-1,-1,-1]]

def check_relations_Z2_hom(relations,hom):
    check = True
    for word in relations:
        check = check and evaluate_Z2_hom(word,hom) == 1
    return check

def find_Z2_hom(name):
    """
    Return the list of homomorphisms from a 2- or 3- generated group to the multiplicative group {1,-1}
    """
    # Compute the fundamental group of the manifold given by name
    M = snappy.Manifold(name)
    G = M.fundamental_group()

    # Extract the list of relators
    relations = G.relators()
    num_generators = len(G.generators())

    # Returns the homomorphism if all relations are satisfied
    return [hom for hom in candidate_Z2_hom(num_generators) if check_relations_Z2_hom(relations,hom)]

def word_equation(word,hom):
    """
    Compute the equation defined by word given a homomorphism to the multiplicative group {1,-1}
    Input:  A word in "a,b,A,B" or "a,b,c,A,B,C" and a candidate homomorphism given as a list of two or three numbers
    Output: A list of coefficients of the equation defined by requiring that word get sent to the identity affine map of the line. In particular, the translation part of the image of word has to be zero. 
    """
    prod = 1

    # coeff_* denotes the translation of * as an affine map on the real line.
    coeff_a = 0
    coeff_b = 0
    coeff_c = 0
    for letter in word[::-1]:
        if letter == "a":
            coeff_a = coeff_a + prod
            prod = prod * hom[0]
        elif letter == "A":
            coeff_a = coeff_a - hom[0] * prod
            prod = prod * hom[0]
        if letter == "b":
            coeff_b = coeff_b + prod
            prod = prod * hom[1]
        elif letter == "B":
            coeff_b = coeff_b  - hom[1] * prod
            prod = prod * hom[1]
        if letter == "c":
            coeff_c = coeff_c + prod
            prod = prod * hom[2]
        elif letter == "C":
            coeff_c = coeff_c  - hom[2] * prod
            prod = prod * hom[2]
    if len(hom) == 2:
        return [coeff_a, coeff_b]
    elif len(hom) == 3:
        return [coeff_a, coeff_b, coeff_c]

def relations_equation(relations, hom):
    """
    Given a homomorphism hom to the multiplicative group {1,-1} and a list of relations as words in "a,b,A,B" or "a,b,c,A,B,C"
    Returns the coefficient matrix of coefficients of the linear system imposed by the group relations to get a group homomorphism to the infinite dihedral group viewed as a sugbroup of the affine maps on the real line.
    """
    return [word_equation(word,hom) for word in relations]

def system_equations(name):
    """
    Given the name of a 3-manifold 
    Returns the matrix of coefficients of the linear system imposed by the group relations to get a group homomorphism to the infinite dihedral group viewed as a sugbroup of the affine maps on the real line.
    """
    M = snappy.Manifold(name)
    G = M.fundamental_group()
    relations = G.relators()
    Z2_hom = find_Z2_hom(name)
    return [relations_equation(relations, hom) for hom in Z2_hom]

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

def s3_permute(tup):
    a = tup[0]
    b = tup[1]
    c = tup[2]
    return [[a,b,c],[a,c,b],[b,a,c],[b,c,a],[c,a,b],[c,b,a]]

def candidate_hom(num_generators):
    """
    Input:  The number of generators of the group which is either 2 or 3
    Output: The list candidate homomorphisms from the group to the infinite dihedral group. The output for the 3-generated case is determined by finding homomorphism obtained by solving linear systems coming the relations of groups from the list of Haken QHS. 
    """
    if num_generators == 2:
        return [["x","y"],["x","xy"],["xy","x"]]
    else:
        return [["x","y",""],["x","","y"],["","x","y"],["x","xy",""],["x","","xy"],["","x","xy"],["xy","x",""],["xy","","x"],["","xy","x"]] + [["x","x","y"],["x","y","x"],["y","x","x"]] + [["x","y","xy"],["x","xy","y"],["y","x","xy"],["y","xy","x"],["xy","x","y"],["xy","y","x"]] + [["x","y","yx"],["x","yx","y"],["y","x","yx"],["y","yx","x"],["yx","x","y"],["yx","y","x"]] + [["x","x","xy"],["x","xy","x"],["xy","x","x"]] + [["x","xy","xy"],["xy","x","xy"],["xy","xy","x"]] + [["x","xy","yx"],["x","yx","xy"],["xy","x","yx"],["xy","yx","x"],["yx","x","xy"],["yx","xy","x"]] + [["y","yxyxy","x"]] + s3_permute(["x","xy","yxyx"]) + s3_permute(["x","yxyx","yx"]) + s3_permute(["xy","yxy","x"]) + s3_permute(["x","xy","xyxy"]) + s3_permute(["x","y","xyxy"]) + s3_permute(["x","y","yxyx"]) + s3_permute(["x","y","yxy"]) + s3_permute(["x","y","yxyxy"])

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
    Input:  The name of the 3-manifold 
    Output: True if the manifold admits an infinite dihedral quotient coming from one of the homomorphism from hom_list and False otherwise.
    """
    # Compute the fundamental group and relatos
    M = snappy.Manifold(name)
    G = M.fundamental_group()
    relations = G.relators()

    # Initialize a list of candidate homomorphism depending of the number of generators of the fundamental group
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
        open_file.write("| Name | Double Cover Test | Search Epimorphism |\n|---|---|---|\n")

    count = 0
    num_three_generated = 0
    remaining_cases = []
    for name in qhs_list:
        index_of_name = qhs_list.index(name)
        line = original_content[index_of_name + 2]
        # Find the index of the 4th column separation character "|"
        index_of_col = find_nth_occurrence(line, "|", 3)
        if is_pos_b1_deg2cover(name) > 0:
            if is_Dinfty_quotient(name) == False:
                with open(file_name, "a") as open_file:
                    open_file.write(line[:index_of_col + 2] + "No" + line[index_of_col + 1:])
                count += 1
            elif is_Dinfty_quotient(name) == True:
                with open(file_name, "a") as open_file:
                    open_file.write(line[:index_of_col + 2] + "Yes" + line[index_of_col + 1:])
            elif is_Dinfty_quotient(name) == None:
                with open(file_name, "a") as open_file:
                    open_file.write(line[:index_of_col + 2] + "Maybe" + line[index_of_col + 1:])
                num_three_generated += 1
                remaining_cases.append(name)
        else:
            with open(file_name, "a") as open_file:
                open_file.write(line[:index_of_col + 2] + "No D_inf quotient" + line[index_of_col + 1:])

    print("There are", count, " additional QHS ruled out by searching for homomorphisms.")
    print("There are", num_three_generated, " 3-generated QHS left to test.")
    return remaining_cases

write_QHS_Dihedral_data(HAKEN_QHS_FILE,HAKEN_QHS_DIHEDRAL_FILE)
write_double_cover_test(HAKEN_QHS_DIHEDRAL_FILE)
search_homomorphism(HAKEN_QHS_DIHEDRAL_FILE)
