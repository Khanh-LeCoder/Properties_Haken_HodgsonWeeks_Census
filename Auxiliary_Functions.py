from multiprocessing import Process, Queue

def find_nth_occurrence(str, char, n):
    """
    Find the index of the nth occurrence of char in str
    Input:  A string str, a char and, a positive integer n
    Output: The index in the str of the nth occurrence of char
    """
    start = str.find(char)
    while start >= 0 and n > 1:
        start = str.find(char, start + len(char))
        n -= 1
    return start

# Define some auxiliary functions to compute ideal of character variety and dimension with time out.
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