import snappy

"""
Starting with a list of Haken 3-manifolds from the Hodgson-Weeks census, find all QHS^3 and store them in the file "Haken_QHS3_Data.md"
"""

def read_name(file_name):
  """
  Input: The name of the file containing the list of 3-manifolds from the census
  Output: The list of name of 3-manifolds from the file
  """

  with open(file_name, 'r') as open_file:
    content = open_file.readlines()
  
  mfld_list = []    
  for name in content: 
    if name.find("\n") != -1:
      mfld_list.append(name[:name.find("\n")])
    else:
      mfld_list.append(name)

  return mfld_list

def is_QHS3(name):
  """
  Input: The name of a 3-manifold from the census. Assume that the 3-manifold is orientable
  Output: True if the first betti number of the manifold is 0 and False otherwise
  """

  M = snappy.Manifold(name)
  return M.homology().betti_number() == 0

def filter_QHS3(file_name):
  """
  Input: The name of the file containing the list of 3-manifolds from the census. Assume they are all orientable
  Output: The list of names of 3-manifolds from the file_name that are QHS3.
  """
  mfld_list = read_name(file_name)

  return [name for name in mfld_list if is_QHS3(name)]

"""
The following functions are used to test whether pi1 has infinite dihedral quotient  
"""

def elem_div_factor(name):
  """
  Input: The name of a 3-manifold
  Output: The number of elementary divisors in the first homology
  """
  M = snappy.Manifold(name)
  return len(M.homology().elementary_divisors())

def sum_b1_deg2cover(name):
  """
  Input: The name of a 3-manifold
  Output: The sum of the betti number of all degree two cover
  """
  M = snappy.Manifold(name)
  cov2 = M.covers(2)
  
  sum_b1 = 0
  if len(cov2) > 0:
    for N in cov2:
      sum_b1 += N.homology().betti_number()

  return sum_b1

def is_deg2cover_zero_b1(name):
  """
  Input: The name of a 3-manifold
  Output: True if the number of elementary divisor factors is at least two and there is a positive betti number among degree two cover 
  """
  if elem_div_factor(name) and sum_b1_deg2cover(name) > 0:
    return True
  else:
    return False

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

def s3_permutations(tup):
    """
    Input:  A list of length 3
    Output: A list of all permutations of the original list
    """
    a = tup[0]
    b = tup[1]
    c = tup[2]
    return [[a,b,c],[a,c,b],[b,a,c],[b,c,a],[c,a,b],[c,b,a]]

def candidate_hom(num_generators):
    """
    Input: The number of generator which has to be either 2 or 3
    Output: The candidate homomorphisms from F2 or F3 onto the group C2 * C2 = <x,y|x^2,y^2> 
    """
    if num_generators == 2:
        # the first generator is either x or xy to be onto up to relabeling x and y (no need to consider y or yx).
        # The case [x, ]: the second entry is y or xy since [x,yx] is conjugate to [x,xy].
        # The case [xy,]: the second entry is x or y. But [xy,y] becomes [yx,x] by symmetry and [xy,x] by conjugation.
        return [["x","y"],["x","xy"],["xy","x"]]
    else:
        # currently missing some cases where the image of a generator is trivial. 
        # Case 1: one generator dies.
        # Either both are mapped to order-two elements or one order-two element and one infinite order element. 
        one_gen_trivial = s3_permutations(["x","y",""]) + s3_permutations(["x","xy",""])
        # Case 2: no generator dies. There are a few cases: 
        # All order-two, two order-two, or one order two-way 
        no_gen_trivial = s3_permutations(["x","x","y"]) + s3_permutations(["xy","x","x"]) 
        return [["xy","x","x"],["x","xy","x"],["x","x","xy"]] + [["x","xy","xy"],["xy","x","xy"],["xy","xy","x"]] + [["x","y","xy"],["y","xy","x"],["xy","x","y"],["x","xy","y"],["xy","y","x"],["y","x","xy"]] + [["x","y","yx"],["y","yx","x"],["yx","x","y"],["x","yx","y"],["yx","y","x"],["y","x","yx"]]
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

def write_QHS3(file_name):
  """
  Input: The name of the file containing the list of 3-manifolds from the census. Assume they are all orientable
  Output: The list of names of 3-manifolds from the file_name that are QHS3 together with other data
  """
  
  mfld_list = read_name(file_name)
  
  with open("Haken_QHS3_data.txt", "w") as open_file:
    open_file.write("| Name | Volume | Homology | Dihedral Quotient | Large SL2C Char. Var. | Algebraic Non-integral |\n|---|---|---|---|---|---|\n")

  for name in mfld_list:
    if is_QHS3(name):
      M = snappy.Manifold(name)
      volume = str(M.volume())
      homology = str(M.homology())
      if elem_div_factor(name) >=2 and sum_b1_deg2cover(name) > 0:
        if is_Dinfty_quotient(name):
          with open("Haken_QHS3_data.txt", "a") as open_file: 
            open_file.write("| " + name + " | " + volume + " | " + homology + " | " + "Yes" + " | " + " | " + " |\n")
        else:
          with open("Haken_QHS3_data.txt", "a") as open_file: 
            open_file.write("| " + name + " | " + volume + " | " + homology + " | " + "No" + " | " + " | " + " |\n")
      elif elem_div_factor(name) >=2 and sum_b1_deg2cover(name) == 0: 
        with open("Haken_QHS3_data.txt", "a") as open_file: 
          open_file.write("| " + name + " | " + volume + " | " + homology + " | " + "No" + " | " + " | " + " |\n")
      else:  
        with open("Haken_QHS3_data.txt", "a") as open_file: 
          open_file.write("| " + name + " | " + volume + " | " + homology + " | " + "No" + " | " + " |\n")
write_QHS3("HakenList.txt")

"""
The following functions are used to compute the ideal of character variety of pi1
"""

from multiprocessing import Process, Queue
import time

def _worker(func, args, queue):
    try:
        result = func(*args)
        queue.put(("result", result))
    except Exception as e:
        queue.put(("error", e))


def run_with_timeout(func, *args, timeout):
    queue = Queue()
    process = Process(
        target=_worker,
        args=(func, args, queue)
    )

    process.start()
    process.join(timeout)

    if process.is_alive():
        process.terminate()
        process.join()
        raise TimeoutError(f"Function exceeded {timeout} seconds")

    status, value = queue.get()
    if status == "error":
        raise value
    return value

def SL2_char_var_ideals(name):
    """
    Input:  The name of a manifold from the Hodson Weeks census
    Output: The dimension of the SL2C character variety of the manifold
    """
    M = snappy.Manifold(name)
    G = M.fundamental_group()
    I = G.character_variety_vars_and_polys("as_ideals")
    return I

"""
The following functions are used to compute the dimension of the character variety and write it into the file. 
"""

def SL2_char_var_dim(ideal_char):
    return ideal_char.dimension()

for data in EQN_List:
    name = data[0]
    ideal_char = data[1]
    if ideal_char == "Time out!":
        with open("SL2_Char_Var_Dim.txt","a") as open_file:
            open_file.write(name + " " + "Equation timed out!\n")    
    else:
        try:
            result = run_with_timeout(SL2_char_var_dim,ideal_char, timeout=5)
            print(result)
            with open("SL2_Char_Var_Dim.txt","a") as open_file:
                open_file.write(name + " " + str(result) + "\n")
        except TimeoutError as e:
            with open("SL2_Char_Var_Dim.txt","a") as open_file:
                open_file.write(name + " " + "Dimension timed out!\n")  
        except RuntimeError:
            with open("SL2_Char_Var_Dim.txt","a") as open_file:
                open_file.write(name + " " + "Dimension error!\n")

with open("Haken_QHS3_data.txt", "r") as open_file1:
    line_lists1 = open_file1.readlines()

with open("SL2_Char_Var_Dim.txt", "r") as open_file2:
    line_lists2 = open_file2.readlines()

def find_nth_occurrence(str, char, n):
    start = str.find(char)
    while start >= 0 and n > 1:
        start = str.find(char, start + len(char)) # Use len(ch) for substrings
        n -= 1
    return start

with open("Haken_QHS3_final_data.txt", "w") as open_file:
        open_file.write("| Name | Volume | Homology | Dihedral Quotient | Dim SL2C Char. Var. | Algebraic Non-integral |\n|---|---|---|---|---|---|\n")

for index in range(0,len(line_lists2)):
    line1 = line_lists1[index + 2]
    line2 = line_lists2[index]
    vert_bar_idx = find_nth_occurrence(line1, "|", 5)
    space_idx = find_nth_occurrence(line2, " ", 1)
    new_line_idx = find_nth_occurrence(line2, "\n", 1)
    if line2[space_idx+1:space_idx+2] == "E" or line2[space_idx+1:space_idx+2] == "D":
        result = line1[:vert_bar_idx + 3] + line2[space_idx+1:new_line_idx] + " | " + " |\n"
    else:
        result = line1[:vert_bar_idx + 3] + line2[space_idx+1:space_idx+2] + " | " + " |\n"
    with open("Haken_QHS3_final_data.txt", "a") as open_file:
        open_file.write(result)

    
    
    
    


  
