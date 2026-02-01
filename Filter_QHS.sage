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
  if M.homology().betti_number() == 0: 
    return True
  else:
    return False

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

def filter_QHS3(file_name):
  """
  Input: The name of the file containing the list of 3-manifolds from the census. Assume they are all orientable
  Output: The list of names of 3-manifolds from the file_name that are QHS3.
  """
  mfld_list = read_name(file_name)

  return [name for name in mfld_list if is_QHS3(name)]
  
  
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

def find_nth_occurrence(str, char, n):
    start = str.find(char)
    while start >= 0 and n > 1:
        start = str.find(char, start + len(char)) # Use len(ch) for substrings
        n -= 1
    return start

with open("Haken_QHS3_data.txt", "r") as open_file1:
    line_lists1 = open_file1.readlines()

with open("SL2_Char_Var_Dim", "r") as open_file2:
    line_lists2 = open_file2.readlines()

for line in line_lists1:
    find_nth_occurrence(line, "|", 5)
    
    

write_QHS3("HakenList.txt")
  
