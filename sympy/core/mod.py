from expr import Expr
from sympify import sympify

class Mod(Function):
    '''Represents a modulo operation on symbolic expressions.

    Receives two arguments, dividend and divisor. If both are Numbers, the
    result is evaluated immediately.

    The convention used is the same as python's: the remainder always has the
    same sign as the divisor.

    Examples:
    >>> from sympy.abc import x, y
    >>> x**2 % y
    Mod(x**2, y)
    >>> _.subs({x: 5, y: 6})
    1

    '''

    nargs = 2

    @classmethod
    def eval(cls, dividend, divisor):
        dividend, divisor = sympify(dividend, divisor)
        if dividend.is_Number and divisor.is_Number:
            return dividend % divisor
        return Expr.__new__(cls, *args)
