import snappy


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

    
    
    
    


  
