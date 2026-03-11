import snappy
from Filter_QHS import *
from multiprocessing import Process, Queue
import time

EQUATION_DATA = "Equation_Data.md"
CHAR_VAR_DATA = "Char_Var_Data.md"

# Define some helper functions to compute ideal of character variety and dimension with time out.
def worker(func, args, queue):
    try:
        result = func(*args)
        queue.put(("result", result))
    except Exception as e:
        queue.put(("error", e))


def run_with_timeout(func, *args, timeout):
    queue = Queue()
    process = Process(
        target=worker,
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

def write_eqn_data(input_file):
    """
    From the list of QHS, try to compute the ideal defining the character variety of the manifold with a timeout of 5 second
    Input:  The input file contains the names of a manifold on each line
    output: None. Write the defining ideal to EQUATION_DATA or "Equation computation timed out"
    """
    # Read the names of manifolds in the input file
    qhs_list = read_name(input_file)

    # Write the headings in the equation files:
    with open(EQUATION_DATA, "w") as eqn_file:
        eqn_file.write("| Name | Equation |\n|---|---|\n")

    count = 0
    for name in qhs_list:
        print(name)
        char_var_ideal = "Equation computation timed out"
        try:
            char_var_ideal = run_with_timeout(SL2_char_var_ideals,name, timeout=5)
            count += 1
        except TimeoutError as e:
            with open(EQUATION_DATA, "a")  as eqn_file:
                eqn_file.write("| " + name + " | " + str(char_var_ideal) + " |\n")
        except Exception as e:
            with open(EQUATION_DATA, "a")  as eqn_file:
                eqn_file.write("| " + name + " | " + str(char_var_ideal) + " |\n")

        with open(EQUATION_DATA, "a") as eqn_file:
            eqn_file.write("| " + name + " | " + str(char_var_ideal) + " |\n")


    print("Computed the character variety of", count, "manifold.")

write_eqn_data(HAKEN_QHS_FILE)

def SL2_char_var_dim(ideal_char):
    return ideal_char.dimension()

def write_dimension_data(file_name):
    # Read the content of EQUATION_DATA
    with open(file_name, "r") as open_file:
        original_content = open_file.readlines()

    # Read the names of the QHS and the equation in EQUATION_DATA create a hash table of {QHS:Equation} and a list of QHS
    eqn_table = {}
    qhs_list = []
    for line in original_content[2:]:
        name = line[find_nth_occurrence(line, "|", 1) + 2:find_nth_occurrence(line, "|", 2)-1]
        eqn  = line[find_nth_occurrence(line, "|", 2) + 2:find_nth_occurrence(line, "|", 3)-1]
        eqn_table[name] = eqn
        qhs_list.append(name)

    with open(CHAR_VAR_DATA, "w") as open_file:
        open_file.write("| Name | Equation | Dimension |\n|---|---|---|\n")

    count = 0
    count_one_dim = 0
    count_zero_dim = 0
    count_timeout = 0
    for name in qhs_list:
        print(name)
        ideal = eqn_table[name]
        if ideal == "Equation computation timed out":
            with open(CHAR_VAR_DATA, "a") as open_file:
                open_file.write("| " + name + " | Equation computation timed out | None |\n")
        else:
            dimension = "Dimension timed out"
            try:
                dimension = run_with_timeout(SL2_char_var_dim,ideal, timeout=5)
                count += 1
            except TimeoutError as e:
                with open(CHAR_VAR_DATA, "a") as open_file:
                    open_file.write("| " + name + " | " + Yes + " | " + dimension + " |\n")

            with open(CHAR_VAR_DATA, "a") as open_file:
                open_file.write("| " + name + " | " + Yes + " | " + dimension + " |\n")

            if dimension == 1:
                count_one_dim += 1
            elif dimension == 0:
                count_zero_dim += 1
            elif dimension == "Dimension timed out":
                count_timeout += 1

    print("Computed the dimension of", count, "character variety.")
    print("There are", count_one_dim, "examples with one-dimensional character variety.")
    print("There are", count_zero_dim, "examples with zero-dimensional character variety.")
    print("There are", count_timeout, "examples.")
write_dimension_data(EQUATION_DATA)





