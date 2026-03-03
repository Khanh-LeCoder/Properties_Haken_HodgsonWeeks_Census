import snappy

INITIAL_HAKEN_FILE = "Haken_List.txt"
HAKEN_QHS_FILE = "Haken_QHS_List.txt"
FINAL_FILE_NAME = "Haken_QHS3_Data.md"


# Starting with a list of Haken 3-manifolds from the Hodgson-Weeks census, find all QHS^3 and store them in the file "Haken_QHS_List.txt"


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


def write_QHS3(file_name):
    """
    Input: The name of the file containing the list of 3-manifolds from the census. Assume they are all orientable
    Output: The list of names of 3-manifolds from the file_name that are QHS3
    """

    mfld_list = read_name(file_name)

    with open(HAKEN_QHS_FILE, "a") as open_file:
        for name in mfld_list:
            if is_QHS3(name):
                open_file.write(name + "\n")

write_QHS3(INITIAL_HAKEN_FILE)