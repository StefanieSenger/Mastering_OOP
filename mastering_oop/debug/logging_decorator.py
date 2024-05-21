import logging, sys
import functools
from typing import Callable, TypeVar, List, Any, cast

# defining the type hints for mypy
FuncType = Callable[..., Any]
F = TypeVar("F", bound=FuncType)


def debug(function: F) -> F:
    """function decorator that adds logging before and after a function call"""

    @functools.wraps(function) # allows us to forward the correct function.__name__ and function.__doc__ as attributes of the result function
    def logged_function(*args, **kw): # gets function's args and kwargs somehow
        logging.debug("%s(%r, %r)", function.__name__, args, kw)
        result = function(*args, **kw)
        logging.debug("%s = %r", function.__name__, result)
        return result

    return cast(F, logged_function) # we return `logged_function` (which returns a new function, called `result`)


def debug_named(log_name: str) -> Callable[[F], F]:
    """function decorator that takes the logger's name (`log_name`) as an argument
    and adds logging before and after a function call;
    the `log_name` specifies the name of the log that the debugging output goes to"""
    log = logging.getLogger(log_name)

    def concrete_decorator(function: F) -> F:

        @functools.wraps(function)
        def wrapped(*args, **kw):
            log.debug("%s(%r, %r)", function.__name__, args, kw)
            result = function(*args, **kw)
            log.debug("%s = %r", function.__name__, result)
            return result

        return cast(F, wrapped)

    return concrete_decorator


print("############### Try Out ###############")

@debug
def ackermann(m: int, n: int) -> int:
    if m == 0:
        return n + 1
    elif m > 0 and n == 0:
        return ackermann(m - 1, 1)
    elif m > 0 and n > 0:
        return ackermann(m - 1, ackermann(m, n - 1))
    else:
        raise Exception(f"Design Error: {vars()}")

'''logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
ackermann(2, 4)
logging.shutdown()
'''

@debug_named("logger_ackermann")
def ackermann(m: int, n: int) -> int:
    if m == 0:
        return n + 1
    elif m > 0 and n == 0:
        return ackermann(m - 1, 1)
    elif m > 0 and n > 0:
        return ackermann(m - 1, ackermann(m, n - 1))
    else:
        raise Exception(f"Design Error: {vars()}")

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
ackermann(2, 4)
logging.shutdown()
