"""
Provides two powerful timeout decorators for different application scenarios.

- @timeout_process: Based on multiprocessing, robust and reliable.
Suitable for CPU-intensive tasks, can truly terminate tasks and reclaim resources.
But requires function parameters and return values to be pickle-able.
- @timeout_thread: Based on threading, lightweight and convenient.
Suitable for scenarios where pickle issues need to be avoided. It doesn't kill background threads,
but lets the main thread "give up waiting". Suitable for one-time scripts or internal tools 
that are not sensitive to resource leaks.
"""

import multiprocessing
import threading
import cProfile
import functools
import os
import sys
import signal
from queue import Empty
from .log import log_warning, log_info

multiprocessing.set_start_method('fork', force=True)
    
# --- Shared Components ---

class TimeoutException(Exception):
    """Exception raised when task execution times out."""
    pass

# --- 1. Process-based Timeout Solution ---

def _worker_wrapper_process_pg(func, args, kwargs, result_queue):
    """
    (Internal function) Runs in an independent "sandbox" process to safely execute the target task.
    """
    try:
        os.setpgrp()
        result = func(*args, **kwargs)
        result_queue.put(('success', result))
    except Exception as e:
        # raise e
        result_queue.put(('error', e))

profiler = cProfile.Profile()

def _dump_stats_and_exit(signum, frame):
    """Signal handler: Save profile and exit when receiving SIGTERM."""
    global profiler
    output_file = "profile.prof"
    
    profiler.disable()
    profiler.dump_stats(output_file)
    
    print("--- [Profiler] Profile file saved, subprocess exiting. ---")
    sys.exit(0)

def _worker_wrapper_process_pg_with_profile(func, args, kwargs, result_queue):
    global profiler
    
    signal.signal(signal.SIGTERM, _dump_stats_and_exit)
    
    os.setpgrp()
    profiler.enable()
    
    try:
        result = func(*args, **kwargs)
        result_queue.put(('success', result))
    except Exception as e:
        result_queue.put(('error', e))
    finally:
        profiler.disable()
        profiler.dump_stats("profile.prof")
        print("--- [Profiler] Profile file saved, subprocess exiting. ---")


def timeout_process(seconds: float, suppress_exceptions=False, logger_name: str = "", profile: bool = False):
    """
    A robust, process-based timeout decorator that can terminate entire process trees.
    Suitable for CPU-intensive tasks.
    """
    
    if os.name == 'nt':
        raise NotImplementedError("Timeout process is not supported on Windows.")
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result_queue = multiprocessing.Queue()
            
            sandbox_process = multiprocessing.Process(
                target=_worker_wrapper_process_pg_with_profile if profile else _worker_wrapper_process_pg, 
                args=(func, args, kwargs, result_queue)
            )
            sandbox_process.start()
            sandbox_process.join(timeout=seconds)
            
            if sandbox_process.is_alive():
                log_warning(logger_name, f"Function '{func.__name__}' [process] timed out ({seconds}s), terminating the whole process group...")
                
                try:
                    pid = sandbox_process.pid
                    if pid is None:
                        log_warning(logger_name, "Sandbox process PID is None (may already ended), cannot terminate.")
                        if suppress_exceptions:
                            return None 
                        else:
                            raise TimeoutException(f"Function '{func.__name__}' did not complete within {seconds} seconds and was forcibly terminated.")
                    else:
                        pgid = os.getpgid(pid)
                        os.killpg(pgid, signal.SIGTERM)
                        log_info(logger_name, f"Sent SIGTERM to process group {pgid}.")
                except ProcessLookupError:
                    log_warning(logger_name, f"Process group not found, skipping SIGTERM.")
                
                sandbox_process.join(timeout=1)
                if suppress_exceptions:
                    return None
                else:
                    raise TimeoutException(f"Function '{func.__name__}' did not complete within {seconds} seconds and was forcibly terminated.")

            try:
                status, result = result_queue.get(timeout=1)
                if status == 'success':
                    return result
                else: # status == 'error'
                    raise result
            except Empty:
                if suppress_exceptions:
                    return None
                else:
                    raise TimeoutException("Task process has ended or been terminated, but did not return any results.")

        return wrapper
    return decorator


# --- 2. Thread-based Timeout Solution ---

def _task_wrapper_thread(func, args, kwargs, result_container):
    """
    (Internal function) Executes task in a thread and puts result or exception into shared container.
    """
    try:
        result = func(*args, **kwargs)
        result_container.append(result)
    except Exception as e:
        result_container.append(e)

def timeout_thread(seconds: float, suppress_exceptions=False, logger_name: str=""):
    """
    A lightweight, thread-based timeout decorator.
    It doesn't kill background threads, but allows the main thread to give up waiting, and requires no pickle.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result_container = []
            
            thread = threading.Thread(
                target=_task_wrapper_thread, 
                args=(func, args, kwargs, result_container)
            )
            thread.daemon = True # Set as daemon thread to ensure main program can exit
            thread.start()
            thread.join(timeout=seconds)

            if thread.is_alive():
                log_warning(logger_name, f"Function '{func.__name__}' [thread] timed out ({seconds}s), main thread has given up waiting. Background thread is still running.")
                if suppress_exceptions:
                    return None
                else:
                    raise TimeoutException(f"Function '{func.__name__}' is still running in the background after {seconds} seconds, main thread has given up waiting.")

            if not result_container:
                return None

            final_result = result_container[0]
            if isinstance(final_result, Exception):
                raise final_result
            else:
                return final_result
        return wrapper
    return decorator
