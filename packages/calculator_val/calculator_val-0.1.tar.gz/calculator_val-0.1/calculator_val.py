"""A simple calculator"""

__version__ = "0.1"

class Calculator:

    def sum(arg1: float, arg2: float) -> float:
        return (arg1 + arg2)

    def subtraction(arg1: float, arg2: float) -> float:
        return (arg1 - arg2)

    def nroot(base: float, root: float) -> float:
        return (base**(1/(root)))

    memory = 0

    def delete(result: float) -> float:
        memory= 0
        return(memory)

