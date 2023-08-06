from queue import Queue
from threading import Thread, Event, Lock
from functools import wraps
from typing import List, Any, Callable, Tuple
import datetime
class RepeaterResult:

    def __init__(self, func, timer, get_nones, get_false, *args, **kwargs):
        self._func = func
        self._timer = timer
        self._get_nones = get_nones
        self._get_false = get_false
        self._queue = Queue()
        self._thread = Thread(target=self.__run, daemon=True, args=args, kwargs=kwargs)
        self._wait = Event().wait
        self._lock = Lock()
        self._running = True
        self._thread.start()

    def __run(self, *args, **kwargs):
        while self._running:
            result = self._func(*args, **kwargs)
            put_nones = bool((result is not None) or self._get_nones)
            put_non_nones = bool(result or self._get_false)
            if put_nones and put_non_nones:
                self._queue.put(result)
            self._wait(self._timer)

    def get(self) -> List:
        """Get accumulated results from queue"""
        res = []
        self._lock.acquire()
        while not self._queue.empty():
            res.append(self._queue.get())
            self._queue.task_done()
        self._lock.release()
        return res

    def stop(self):
        """Stop timer"""
        self._running = False
        self._thread.join()

class CashedResult:

    def __init__(self, func, timer, timeout, *args, **kwargs):
        self._func = func
        self._timer = timer
        self._timeout = timeout
        self._cashed_result = None
        self._result_time: datetime.datetime = None
        # self._latest_result = Queue()
        self._thread = Thread(target=self.__run, daemon=True, args=args, kwargs=kwargs)
        self._wait = Event().wait
        # self._lock = Lock()
        self._running = True
        self._thread.start()

    def __run(self, *args, **kwargs):
        while self._running:
            result = self._func(*args, **kwargs)
            op_time = datetime.datetime.now()
            # self._latest_result.put((result, op_time))
            # self._cashed_result, self._result_time = self._latest_result.get()
            # self._latest_result.task_done()
            self._cashed_result, self._result_time = result, op_time
            
            self._wait(self._timer)

    def get(self) -> Tuple[Any, datetime.datetime]:
        """Get cashed result"""
        # self._lock.acquire()
        while True:
            if not self._result_time:
                continue
            since_last_cash = (datetime.datetime.now() - self._result_time).total_seconds()
            if since_last_cash > self._timeout:
                return None, self._result_time
            return self._cashed_result, self._result_time
  
        # self._lock.release()


    def stop(self):
        """Stop timer"""
        self._running = False
        self._thread.join()
        self._cashed_result = None

def cash_timer(timer: float, timeout=None):
    """Launches a thread that will execute a function each 'timer' sec 
    to cash the result, call 'get' method to get the result, to stop timer call
    'stop' method

    Args:
        timer: float, delay between calls
        timeout: float, throw an error if the last call was >timeout ago
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs) -> CashedResult:
            return CashedResult(func, timer, timeout, *args, **kwargs)
    
        return wrapper
    return decorator


def repeat_timer(timer, get_nones=False, get_false=True):
    """Launches a thread that will execute a function each 'timer' sec, 
    to get accumulated results call 'get' method, to stop timer call 'stop' method 
    of returned value

    Args:
        timer: float, delay between calls
        get_nones: bool, put 'None' values in result
        get_false: bool, put bool() == False values in result
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs) -> RepeaterResult:
            return RepeaterResult(func, timer, get_nones, get_false, *args, **kwargs)
    
        return wrapper
    return decorator