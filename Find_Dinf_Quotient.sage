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

def sub_relation(relation,hom):
    """
    Input: A list of relations and a candidate homomorphism
    Output: A list of images of the relations under the homorphism
    """
    return [substitute(word,hom) for word in relation]

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
    if num_generators == 2:
        return [["x","y"],["x","xy"],["xy","x"]]
    else:
        return [["y","x","x"],["x","y","x"],["x","x","y"]] + [["xy","x","x"],["x","xy","x"],["x","x","xy"]] + [["x","xy","xy"],["xy","x","xy"],["xy","xy","x"]] + [["x","y","xy"],["y","xy","x"],["xy","x","y"],["x","xy","y"],["xy","y","x"],["y","x","xy"]] + [["x","y","yx"],["y","yx","x"],["yx","x","y"],["x","yx","y"],["yx","y","x"],["y","x","yx"]] 
                
  



