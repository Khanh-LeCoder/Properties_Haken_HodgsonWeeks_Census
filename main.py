from Auxiliary_Functions import find_nth_occurrence

with open("HakenQHS_Dihedral_Data.md", "r") as dihedral_file:
    dihedral_data = dihedral_file.readlines()[2:]

print(dihedral_data[0])

with open("Char_Var_Data.md", "r") as variety_file:
    variety_data = variety_file.readlines()[2:]

print(variety_data[0])

with open("Haken_QHS_Data.md", "w") as summary_file:
    summary_file.write("| Name | Dihedral Quotient | Ideal | Dimension |\n|---|---|---|---|\n")

for line in dihedral_data:

    # Record the name of the manifold
    name_start_index = find_nth_occurrence(line,"|", 1)
    name_end_index = find_nth_occurrence(line,"|", 2)
    name = line[name_start_index+2:name_end_index-1]

    # Record the result of the dihedral test
    dihedral_start_index = find_nth_occurrence(line,"|", 3)
    dihedral_end_index = find_nth_occurrence(line,"|", 4)
    if line[dihedral_start_index+2:dihedral_end_index-1] == "No D_inf quotient":
        dihedral_result = "No"
    elif line[dihedral_start_index+2:dihedral_end_index-1] == "Yes":
        dihedral_result = "Yes"

    # Find the line in the variety data
    variety_line = variety_data[variety_data.index(name)]
    print(name)
    print(variety_line)