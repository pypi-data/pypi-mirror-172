
import threading
from typing import Any, List


def run_in_threads_if_required(background_thread: bool,
                               func,
                               args: List[Any],
                               thread_name: str):
    """
    it's wrapper function which run the `func`
    in another thread if multi_threading option is True
    else it calls the `func` in the same thread
    :param multi_threading: Flag to determine if run in multi-threading
    :type multi_threading: Boolean
    :param func: Function need to be called
    :type func: Function
    :param args: List of arguments for `func`
    :type args: List[Any]
    :param thread_name: Name of thread if `func` runs
    in another thread
    :type args: str
    """
    if background_thread:
        thread = threading.Thread(target=func, args=args)
        thread.daemon = True
        thread.setName(thread_name)
        thread.start()
    else:
        func(*args)