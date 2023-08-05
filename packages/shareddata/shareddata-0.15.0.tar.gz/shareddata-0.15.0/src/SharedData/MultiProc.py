
# SuperFastPython.com
# load many files concurrently with processes and threads in batch
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

# USAGE EXAMPLE:
# io_bound(thread_func, iterator, args)
# thread_func:define the task function to run parallel. Ie: read_files,days_trading_from_to
# iteration: single iteration items of parallel task
# args: commom task variables 

# thread_func EXAMPLES

# IO BOUND EXAMPLE
# def read_files(iteration, args):
#     fileid = iteration[0]    
#     file_list = args[0]
#     fpath = file_list[fileid]
#     df = pd.read_csv(fpath)
#     return [df]

# CPU BOUND EXAMPLE
# def days_trading_from_to(iteration, args):
#     cal = iteration[0]
#     start = iteration[1]
#     end = iteration[2]
#     calendars = args[0]
#     idx = (calendars[cal]>=start) & ((calendars[cal]<=end))
#     return [np.count_nonzero(idx)]

# return the contents of many files
def io_bound_process(thread_func, proc_iterator, args):
    # create a thread pool
    nproc_iterator = len(proc_iterator)
    with ThreadPoolExecutor(nproc_iterator) as exe:
        # load files
        futures = [exe.submit(thread_func, iteration, args) for iteration in proc_iterator]
        # collect data
        results = []
        for future in futures:
            res = future.result()
            results = [*results, *res]
    return results
 
# load all files in a directory into memory
def io_bound(thread_func, iterator, args):
    # determine chunksize
    
    n_workers = multiprocessing.cpu_count() - 2     
    niterator = len(iterator)
    chunksize = round(niterator / n_workers)
    # create the process pool
    with ProcessPoolExecutor(n_workers) as executor:        
        futures = list()
        # split the load operations into chunks
        for i in range(0, niterator, chunksize):
            # select a chunk of filenames
            proc_iterator = iterator[i:(i + chunksize)]
            # submit the task
            future = executor.submit(io_bound_process, thread_func, proc_iterator, args)
            futures.append(future)                     
        results = []
        # process all results
        for future in as_completed(futures):
            # open the file and load the data
            res = future.result()
            results = [*results, *res]

    return results


# return the contents of many files
def cpu_bound_process(thread_func, proc_iterator, args):
    return [thread_func(iteration, args) for iteration in proc_iterator]

def cpu_bound(thread_func, iterator, args):
    # determine chunksize
    
    n_workers = multiprocessing.cpu_count() - 2     
    niterator = len(iterator)
    chunksize = round(niterator / n_workers)
    # create the process pool
    with ProcessPoolExecutor(n_workers) as executor:        
        futures = list()
        # split the load operations into chunks
        for i in range(0, niterator, chunksize):
            # select a chunk of filenames
            proc_iterator = iterator[i:(i + chunksize)]
            # submit the task
            future = executor.submit(cpu_bound_process, thread_func, proc_iterator, args)
            futures.append(future)                     
        results = []
        # process all results
        for future in as_completed(futures):
            # open the file and load the data
            res = future.result()
            results = [*results, *res]

    return results

