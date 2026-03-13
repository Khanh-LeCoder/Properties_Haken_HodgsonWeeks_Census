def find_nth_occurrence(str, char, n):
    """
    Find the nth occurrence of char in str
    Input:  A string str, a char and, a positive integer n
    Output: The index in the str of the nth occurrence of char
    """
    start = str.find(char)
    while start >= 0 and n > 1:
        start = str.find(char, start + len(char))
        n -= 1
    return start