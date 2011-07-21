"""
Reimplementations of constructs introduced in Python 2.5 for compatibility with
Python 2.4
"""
#XXX: When we drop Python 2.4 support, replace minkey, iff, all, and any
# with their builtin equivalents.
def minkey(sequence, key):
    """
    Implements the min() function with the key argument.

    This is because the key argument isn't supported in Python 2.4.  The
    argument works the same as the key argument to sorted. `key` should be a
    function on the elements of `sequence` that returns objects that are
    comparable with each other, such as integers.  If more than one element
    of the sequence is the smallest with respect to key, then the first one
    will be returned.  This only supports the sequence version of min().

    == Example ==

    >>> from sympy.utilities.iterables import minkey
    >>> minkey(['ab', 'a', 'abc', 'x'], key=len)
    'a'

    """
    # Note, we must not implement this using indexing, because not all
    # container objects support indexing (like sets)!
    first = True
    for item in sequence:
        if first:
            smallest = item
            smallestkey = key(item)
            first = False

        keyi = key(item)
        if keyi < smallestkey:
            smallest = item
            smallestkey = keyi
    return smallest

def iff(condition, result1, result2):
    """
    Return result1 if condition else result2

    This is a replacement for the conditional if statement that is part of
    python 2.5+. If the condition must should not be called unless the
    condition is met, then wrap the result in a lambda; it will be called
    to return the result:

    >>> from sympy import iff
    >>> x = 0.5
    >>> iff(x == 0, x, lambda: 1/x)
    2.0
    >>> x = 0
    >>> iff(x == 0, x, lambda: 1/x)
    0
    """

    if condition:
        rv = result1
    else:
        rv = result2
    # XXX this is fragile; is there a better way to tell if it's a lambda?
    if '<lambda>' in str(rv):
        return rv()
    else:
        return rv

try:
    from __builtins__ import all
except ImportError:
    def all(iterable):
        """
        Return True if all elements are set to True. This
        function does not support predicates explicitly,
        but this behavior can be simulated easily using
        list comprehension.

        >>> from sympy import all
        >>> all( [True, True, True] )
        True
        >>> all( [True, False, True] )
        False
        >>> all( [ x % 2 == 0 for x in [2, 6, 8] ] )
        True
        >>> all( [ x % 2 == 0 for x in [2, 6, 7] ] )
        False

        NOTE: Starting from Python 2.5 this a built-in.
        """
        for item in iterable:
            if not item:
                return False
        return True

try:
    from __builtins__ import all
except ImportError:
    def any(iterable):
        """
        Return True if at least one element is set to True.
        This function does not support predicates explicitly,
        but this behavior can be simulated easily using
        list comprehension.

        >>> from sympy import any
        >>> any( [False, False, False] )
        False
        >>> any( [False, True, False] )
        True
        >>> any( [ x % 2 == 1 for x in [2, 6, 8] ] )
        False
        >>> any( [ x % 2 == 1 for x in [2, 6, 7] ] )
        True

        NOTE: Starting from Python 2.5 this a built-in.
        """
        for item in iterable:
            if item:
                return True
        return False

def iterable(i, exclude=(basestring, dict)):
    """
    Return a boolean indicating whether i is an iterable in the sympy sense.

    When sympy is working with iterables, it is almost always assuming
    that the iterable is not a string or a mapping, so those are excluded
    by default. If you want a pure python definition, make exclude=None. To
    exclude multiple items, pass them as a tuple.

    See also: ordered_iter

    Examples:

    >>> from sympy.utilities.iterables import iterable
    >>> from sympy import Tuple
    >>> things = [[1], (1,), set([1]), Tuple(1), (j for j in [1, 2]), {1:2}, '1', 1]
    >>> for i in things:
    ...     print iterable(i), type(i)
    True <type 'list'>
    True <type 'tuple'>
    True <type 'set'>
    True <class 'sympy.core.containers.Tuple'>
    True <type 'generator'>
    False <type 'dict'>
    False <type 'str'>
    False <type 'int'>

    >>> iterable({}, exclude=None)
    True
    >>> iterable({}, exclude=str)
    True
    >>> iterable("no", exclude=str)
    False

    """
    try:
        iter(i)
    except TypeError:
        return False
    if exclude:
        return not isinstance(i, exclude)
    return True

def ordered_iter(i, include=None):
    """
    Return a boolean indicating whether i is an ordered iterable in the sympy
    sense. If anything is iterable but doesn't have an index attribute, it
    can be included in what is considered iterable by using the 'include'
    keyword. If multiple items are to be included, pass them as a tuple.

    See also: iterable

    Examples:

    >>> from sympy.utilities.iterables import ordered_iter
    >>> from sympy import Tuple
    >>> ordered_iter([])
    True
    >>> ordered_iter(set())
    False
    >>> ordered_iter('abc')
    False
    >>> ordered_iter('abc', include=str)
    True

    """
    return (hasattr(i, '__getitem__') and
            iterable(i) or
            bool(include) and
            isinstance(i, include))

"""
Wrapping some imports in try/except statements to allow the same code to
be used in Python 3+ as well.
"""

try:
    callable = callable
except NameError:
    import collections
    def callable(obj):
        return isinstance(obj, collections.Callable)

try:
    from functools import reduce
except ImportError:
    reduce = reduce

def cmp_to_key(mycmp):
    """
    Convert a cmp= function into a key= function

    This code is included in Python 2.7 and 3.2 in functools.
    """
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K

try:
    import __builtin__
    cmp = __builtin__.cmp
except AttributeError:
    def cmp(a,b):
        return (a > b) - (a < b)

try:
    from itertools import product
except ImportError: # Python 2.5
    def product(*args, **kwds):
        # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
        # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
        pools = map(tuple, args) * kwds.get('repeat', 1)
        result = [[]]
        for pool in pools:
            result = [x+[y] for x in result for y in pool]
        for prod in result:
            yield tuple(prod)

try:
    from itertools import permutations
except ImportError: # Python 2.5
    def permutations(iterable, r=None):
        # permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
        # permutations(range(3)) --> 012 021 102 120 201 210
        pool = tuple(iterable)
        n = len(pool)
        r = n if r is None else r
        if r > n:
            return
        indices = range(n)
        cycles = range(n, n-r, -1)
        yield tuple(pool[i] for i in indices[:r])
        while n:
            for i in reversed(range(r)):
                cycles[i] -= 1
                if cycles[i] == 0:
                    indices[i:] = indices[i+1:] + indices[i:i+1]
                    cycles[i] = n - i
                else:
                    j = cycles[i]
                    indices[i], indices[-j] = indices[-j], indices[i]
                    yield tuple(pool[i] for i in indices[:r])
                    break
            else:
                return

try:
    from itertools import combinations, combinations_with_replacement
except ImportError: # < python 2.6
    def combinations(iterable, r):
        # combinations('ABCD', 2) --> AB AC AD BC BD CD
        # combinations(range(4), 3) --> 012 013 023 123
        pool = tuple(iterable)
        n = len(pool)
        if r > n:
            return
        indices = range(r)
        yield tuple(pool[i] for i in indices)
        while True:
            for i in reversed(range(r)):
                if indices[i] != i + n - r:
                    break
            else:
                return
            indices[i] += 1
            for j in range(i+1, r):
                indices[j] = indices[j-1] + 1
            yield tuple(pool[i] for i in indices)

    def combinations_with_replacement(iterable, r):
        # combinations_with_replacement('ABC', 2) --> AA AB AC BB BC CC
        pool = tuple(iterable)
        n = len(pool)
        if not n and r:
            return
        indices = [0] * r
        yield tuple(pool[i] for i in indices)
        while True:
            for i in reversed(range(r)):
                if indices[i] != n - 1:
                    break
            else:
                return
            indices[i:] = [indices[i] + 1] * (r - i)
            yield tuple(pool[i] for i in indices)
