# JANKY, NOT WORKING. USE THE DECORATOR INSTEAD

from __future__ import annotations
from typing import Generic, TypeVar, overload, Literal
from enum import StrEnum

class State(StrEnum):
    SUCCESS = "success"
    FAILURE = "failure"
    
S = TypeVar("S", bound=State)
R = TypeVar("R")
# E = TypeVar("E", bound=Exception)

class Returns(Generic[S, R]):
    @overload
    def __init__(self: Returns[Literal[State.SUCCESS], R], *, result: R) -> None:
        ...
        
    @overload
    def __init__(self: Returns[Literal[State.FAILURE], None], *, exception: Exception) -> None:
        ...
    
    def __init__(self, *, result: R | None = None, exception: Exception | None = None) -> None:
        self.result = result
        self.exception = exception
        
# def divide(a: int, b: int) -> Returns[float]