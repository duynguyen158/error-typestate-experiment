from functools import wraps
from typing import TypeVar, ParamSpec, Callable, Union, Any
from dataclasses import dataclass
# from typing_extensions import TypeVar

# TypeVar()

# P = ParamSpec("P")
# R = TypeVar("R")

def propagate_exception[R, **P](func: Callable[P, R]) -> Callable[P, R | Exception]:
    """Decorator to propagate exceptions from a function.

    Args:
        func (Callable[P, R]): The function to decorate.

    Returns:
        Callable[P, R | Exception]: The decorated function.
    """
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | Exception:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return e
        
    return wrapper

@dataclass
class Success[R]:
    result: R
    
# @dataclass
# class Failure[E: Exception]:
#     exception: E

# def propagate_exception_with_type[E, R, **P]() -> Callable[[Callable[P, R]], Callable[P, R | E]]:
#     def decorator(func: Callable[P, R]) -> Callable[P, R | E]:
#         @wraps(func)
#         def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | E:
#             try:
#                 return func(*args, **kwargs)
#             except Exception as e:
#                 return e
            
#         return wrapper
        
#     return decorator

# Doing this as a class instead of a function means we can type-hint the exception type before passing in the function to decorate
class propagate_exception_with_type[E: Exception]: # When Python 3.13 is released and we can use TypeVar with defaults: propagate_exception_with_type[E: Exception = Exception] will be possible
    """
    Decorator to propagate exceptions from a function, with a specific exception type indicating it should be handled.
    """
    def __call__[R, **P](self, func: Callable[P, R]) -> Callable[P, Success[R] | E | Exception]:
        """Returns a decorated function that propagates exceptions of a specific type.

        Args:
            func (Callable[P, R]): The function to decorate.

        Returns:
            Callable[P, Success[R] | E | Exception]: The decorated function, which returns a Success object if successful or an exception (of the specified type if it should be handled, or a generic exception if it should be raised) in case of failure.
        """
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Success[R] | E | Exception:
            try:
                return Success(result=func(*args, **kwargs))
            except Exception as e:
                return e
            
        return wrapper

# @propagate_exception
# @propagate_exception_with_type[Exception]() # When Python 3.13 is released and we can use TypeVar with defaults: @propagate_exception_with_type() alone is enough
@propagate_exception_with_type[ZeroDivisionError | AssertionError]()
def divide(a: float, b: float, *, assert_fails: bool) -> float:
    assert not assert_fails, "Assertion failed"
    
    raise ValueError("This is a test")
    
    return a / b


if __name__ == "__main__":
    # Print custom error message if zero division error occurs, else print generic error if other error, else print result
    match divide(1, 2, assert_fails=False):
        case Success(result):
            print(result)
        case ZeroDivisionError():
            print("Cannot divide by zero")
        case AssertionError():
            print("Assertion failed")
        case uncaught_exception:
            print("UNCAUGHT EXCEPTION")
            raise uncaught_exception