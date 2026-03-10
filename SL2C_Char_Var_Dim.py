import snappy
from Filter_QHS import *
from multiprocessing import Process, Queue
import time

EQUATION_DATA = "Equation_data.md"
CHAR_VAR_DATA = "Char_Var_data.md"

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

def write_eqn_data(input_file):
    """
    From the list of QHS, try to compute the ideal defining the character variety of the manifold with a timeout of 5 second
    Input:  The input file contains the names of a manifold on each line
    output: None. Write the defining ideal to EQUATION_DATA or "Equation computation timed out"
    """
    # Read the names of manifolds in the input file
    mfld_list = read_name(input_file)

    # Write the headings in the equation files:
    with open(EQUATION_DATA, "w") as eqn_file:
        eqn_file.write("| Name | Equation |\n|---|---|\n")

    for name in mfld_list:
        print(name)
        try:
            char_var_ideal = run_with_timeout(SL2_char_var_ideals,name, timeout=5)
            with open(EQUATION_DATA, "a")  as eqn_file:
                eqn_file.write("| " + name + " | " + char_var_ideal + " |\n")
        except TimeoutError as e:
            with open(EQUATION_DATA, "a")  as eqn_file:
                eqn_file.write("| " + name + " | Equation computation timed out |\n")
        except Exception as e:
            with open(EQUATION_DATA, "a")  as eqn_file:
                eqn_file.write("| " + name + " | Equation computation timed out |\n")

write_eqn_data(HAKEN_QHS_FILE)


def SL2_char_var_ideals(name):
    """
    Input:  The name of a manifold from the Hodson Weeks census
    Output: The dimension of the SL2C character variety of the manifold
    """
    M = snappy.Manifold(name)
    G = M.fundamental_group()
    I = G.character_variety_vars_and_polys("as_ideals")
    return I


def SL2_char_var_dim(ideal_char):
    return ideal_char.dimension()


for data in EQN_List:
    name = data[0]
    ideal = data[1]
    print(name)
    if ideal == "Time out!":
        with open("SL2_Char_Var_Dim", "a") as open_file:
            open_file.write("name" + " " + "Equation timed out!\n")
    else:
        try:
            result = run_with_timeout(SL2_char_var_dim, ideal, timeout=5)
            with open("SL2_Char_Var_Dim", "a") as open_file:
                open_file.write("name" + " " + str(result))
        except TimeoutError as e:
            with open("SL2_Char_Var_Dim", "a") as open_file:
                open_file.write("name" + " " + "Dimension timed out!\n")




