import snappy
import Filter_QHS3.sage

def substitute(word,hom):
    """
    Input: A word and a candidate homomorphism 
    Output: The image of word under the homomorphism
    """
    new_word = ""
    if length(hom) == 2:
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
            word = word[:index] + word[index + 1:]
        if word.find('yy') != -1:
            index = word.find('yy')
            word = word[:index] + word[index + 1:]
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
    M = snappy.Manifold(name)
    G = M.fundamental_group()
    num_generators = len(G.generators())


  



