import snappy
from Text_Processing import *

# The names of the input and output files for these computations.
# The file "Haken_List.txt" contains all Haken 3-manifolds found in the Hodgson Weeks census.
INITIAL_HAKEN_FILE = "Haken_List.txt"

# The file "Haken_QHS_List.txt" contains all Haken QHS in "Haken_List.txt"
HAKEN_QHS_FILE = "Haken_QHS_List.txt"

FINAL_FILE_NAME = "HakenQHS_Dihedral_Data.md"

def read_name(file_name):
    """
    Input:  The name of the file containing a list of 3-manifolds (of any kind)
    Output: The list of name of 3-manifolds from the file
    """
    with open(file_name, 'r') as open_file:
        content = open_file.readlines() # read the content as a list of strings

    mfld_list = []
    for name in content:
        if name.find("\n") != -1:
            mfld_list.append(name[:name.find("\n")])
        else:
            mfld_list.append(name)
    return mfld_list

def is_QHS3(name):
    """
    The function test if an orientable closed 3-manifold is a QHS by computing the first betti number
    Input:  The name of a 3-manifold from the census. Assume that the 3-manifold is orientable
    Output: True if the first betti number of the manifold is 0 and False otherwise
    """
    M = snappy.Manifold(name)
    return M.homology().betti_number() == 0


def filter_QHS3(file_name):
    """
    Given a list of closed orientable 3-manifolds, filter out a list of QHS
    Input:  The name of the file containing the list of 3-manifolds from the census. Assume they are all orientable
    Output: The list of names of 3-manifolds from the file_name that are QHS3.
    """
    mfld_list = read_name(file_name)

    return [name for name in mfld_list if is_QHS3(name)]


def write_QHS(file_name):
    """
    Starting from the list of 3-manifold in "Haken_List.txt" filter out QHS, write to the file and return the count of QHS
    Input:  The name of the file containing the list of 3-manifolds from the census. Assume they are all orientable
    Output: The list of names of 3-manifolds from the file_name that are QHS3 and return the total number of QHS
    """
    mfld_list = read_name(file_name)
    count = 0

    # Ensuring that the file is empty to begin with
    with open(HAKEN_QHS_FILE, "w") as open_file:
        pass

    with open(HAKEN_QHS_FILE, "a") as open_file:
        for name in mfld_list:
            if is_QHS3(name):
                count += 1
                open_file.write(name + "\n")
    print("There are", count, "Haken QHS.")

write_QHS(INITIAL_HAKEN_FILE)
