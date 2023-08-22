"""Imported from the recipes section of the itertools documentation.

All functions taken from the recipes section of the itertools library docs
[1]_.
Some backward-compatible usability improvements have been made.

.. [1] http://docs.python.org/library/itertools.html#recipes

"""
import math
import operator
<<<<<<< HEAD
=======
import warnings
>>>>>>> 72864d1 (Tue 22 Aug 2023 02:44:06 PM CDT)

from collections import deque
from collections.abc import Sized
from functools import reduce
from itertools import (
    chain,
    combinations,
    compress,
    count,
    cycle,
    groupby,
    islice,
<<<<<<< HEAD
=======
    product,
>>>>>>> 72864d1 (Tue 22 Aug 2023 02:44:06 PM CDT)
    repeat,
    starmap,
    tee,
    zip_longest,
)
from random import randrange, sample, choice
<<<<<<< HEAD
=======
from sys import hexversion
>>>>>>> 72864d1 (Tue 22 Aug 2023 02:44:06 PM CDT)

__all__ = [
    'all_equal',
    'batched',
    'before_and_after',
    'consume',
    'convolve',
    'dotproduct',
    'first_true',
<<<<<<< HEAD
    'flatten',
    'grouper',
    'iter_except',
=======
    'factor',
    'flatten',
    'grouper',
    'iter_except',
    'iter_index',
    'matmul',
>>>>>>> 72864d1 (Tue 22 Aug 2023 02:44:06 PM CDT)
    'ncycles',
    'nth',
    'nth_combination',
    'padnone',
    'pad_none',
    'pairwise',
    'partition',
    'polynomial_from_roots',
    'powerset',
    'prepend',
    'quantify',
    'random_combination_with_replacement',
    'random_combination',
    'random_permutation',
    'random_product',
    'repeatfunc',
    'roundrobin',
    'sieve',
    'sliding_window',
    'subslices',
    'tabulate',
    'tail',
    'take',
<<<<<<< HEAD
=======
    'transpose',
>>>>>>> 72864d1 (Tue 22 Aug 2023 02:44:06 PM CDT)
    'triplewise',
    'unique_everseen',
    'unique_justseen',
]

_marker = object()


def take(n, iterable):
    """Return first *n* items of the iterable as a list.

        >>> take(3, range(10))
        [0, 1, 2]

    If there are fewer than *n* items in the iterable, all of them are
    returned.

        >>> take(10, range(3))
        [0, 1, 2]

    """
    return list(islice(iterable, n))


def tabulate(function, start=0):
    """Return an iterator over the results of ``func(start)``,
    ``func(start + 1)``, ``func(start + 2)``...

    *func* should be a function that accepts one integer argument.

    If *start* is not specified it defaults to 0. It will be incremented each
    time the iterator is advanced.

        >>> square = lambda x: x ** 2
        >>> iterator = tabulate(square, -3)
        >>> take(4, iterator)
        [9, 4, 1, 0]

    """
    return map(function, count(start))


def tail(n, iterable):
    """Return an iterator over the last *n* items of *iterable*.

    >>> t = tail(3, 'ABCDEFG')
    >>> list(t)
    ['E', 'F', 'G']

    """
    # If the given iterable has a length, then we can use islice to get its
    # final elements. Note that if the iterable is not actually Iterable,
    # either islice or deque will throw a TypeError. This is why we don't
    # check if it is Iterable.
    if isinstance(iterable, Sized):
        yield from islice(iterable, max(0, len(iterable) - n), None)
    else:
        yield from iter(deque(iterable, maxlen=n))


def consume(iterator, n=None):
    """Advance *iterable* by *n* steps. If *n* is ``None``, consume it
    entirely.

    Efficiently exhausts an iterator without returning values. Defaults to
    consuming the whole iterator, but an optional second argument may be
    provided to limit consumption.

        >>> i = (x for x in range(10))
        >>> next(i)
        0
        >>> consume(i, 3)
        >>> next(i)
        4
        >>> consume(i)
        >>> next(i)
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
        StopIteration

    If the iterator has fewer items remaining than the provided limit, the
    whole iterator will be consumed.

        >>> i = (x for x in range(3))
        >>> consume(i, 5)
        >>> next(i)
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
        StopIteration

    """
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(islice(iterator, n, n), None)


def nth(iterable, n, default=None):
    """Returns the nth item or a default value.

    >>> l = range(10)
    >>> nth(l, 3)
    3
    >>> nth(l, 20, "zebra")
    'zebra'

    """
    return next(islice(iterable, n, None), default)


def all_equal(iterable):
    """
    Returns ``True`` if all the elements are equal to each other.

        >>> all_equal('aaaa')
        True
        >>> all_equal('aaab')
        False

    """
    g = groupby(iterable)
    return next(g, True) and not next(g, False)


def quantify(iterable, pred=bool):
    """Return the how many times the predicate is true.

    >>> quantify([True, False, True])
    2

    """
    return sum(map(pred, iterable))


def pad_none(iterable):
    """Returns the sequence of elements and then returns ``None`` indefinitely.

        >>> take(5, pad_none(range(3)))
        [0, 1, 2, None, None]

    Useful for emulating the behavior of the built-in :func:`map` function.

    See also :func:`padded`.

    """
    return chain(iterable, repeat(None))


padnone = pad_none


def ncycles(iterable, n):
    """Returns the sequence elements *n* times

    >>> list(ncycles(["a", "b"], 3))
    ['a', 'b', 'a', 'b', 'a', 'b']

    """
    return chain.from_iterable(repeat(tuple(iterable), n))


def dotproduct(vec1, vec2):
    """Returns the dot product of the two iterables.

    >>> dotproduct([10, 10], [20, 20])
    400

    """
    return sum(map(operator.mul, vec1, vec2))


def flatten(listOfLists):
    """Return an iterator flattening one level of nesting in a list of lists.

        >>> list(flatten([[0, 1], [2, 3]]))
        [0, 1, 2, 3]

    See also :func:`collapse`, which can flatten multiple levels of nesting.

    """
    return chain.from_iterable(listOfLists)


def repeatfunc(func, times=None, *args):
    """Call *func* with *args* repeatedly, returning an iterable over the
    results.

    If *times* is specified, the iterable will terminate after that many
    repetitions:

        >>> from operator import add
        >>> times = 4
        >>> args = 3, 5
        >>> list(repeatfunc(add, times, *args))
        [8, 8, 8, 8]

    If *times* is ``None`` the iterable will not terminate:

        >>> from random import randrange
        >>> times = None
        >>> args = 1, 11
        >>> take(6, repeatfunc(randrange, times, *args))  # doctest:+SKIP
        [2, 4, 8, 1, 8, 4]

    """
    if times is None:
        return starmap(func, repeat(args))
    return starmap(func, repeat(args, times))


def _pairwise(iterable):
    """Returns an iterator of paired items, overlapping, from the original

    >>> take(4, pairwise(count()))
    [(0, 1), (1, 2), (2, 3), (3, 4)]

    On Python 3.10 and above, this is an alias for :func:`itertools.pairwise`.

    """
    a, b = tee(iterable)
    next(b, None)
    yield from zip(a, b)


try:
    from itertools import pairwise as itertools_pairwise
except ImportError:
    pairwise = _pairwise
else:

    def pairwise(iterable):
        yield from itertools_pairwise(iterable)

    pairwise.__doc__ = _pairwise.__doc__


class UnequalIterablesError(ValueError):
    def __init__(self, details=None):
        msg = 'Iterables have different lengths'
        if details is not None:
            msg += (': index 0 has length {}; index {} has length {}').format(
                *details
            )

        super().__init__(msg)


def _zip_equal_generator(iterables):
    for combo in zip_longest(*iterables, fillvalue=_marker):
        for val in combo:
            if val is _marker:
                raise UnequalIterablesError()
        yield combo


def _zip_equal(*iterables):
    # Check whether the iterables are all the same size.
    try:
        first_size = len(iterables[0])
        for i, it in enumerate(iterables[1:], 1):
            size = len(it)
            if size != first_size:
                break
        else:
            # If we didn't break out, we can use the built-in zip.
            return zip(*iterables)

        # If we did break out, there was a mismatch.
        raise UnequalIterablesError(details=(first_size, i, size))
    # If any one of the iterables didn't have a length, start reading
    # them until one runs out.
    except TypeError:
        return _zip_equal_generator(iterables)


def grouper(iterable, n, incomplete='fill', fillvalue=None):
    """Group elements from *iterable* into fixed-length groups of length *n*.

    >>> list(grouper('ABCDEF', 3))
    [('A', 'B', 'C'), ('D', 'E', 'F')]

    The keyword arguments *incomplete* and *fillvalue* control what happens for
    iterables whose length is not a multiple of *n*.

    When *incomplete* is `'fill'`, the last group will contain instances of
    *fillvalue*.

    >>> list(grouper('ABCDEFG', 3, incomplete='fill', fillvalue='x'))
    [('A', 'B', 'C'), ('D', 'E', 'F'), ('G', 'x', 'x')]

    When *incomplete* is `'ignore'`, the last group will not be emitted.

    >>> list(grouper('ABCDEFG', 3, incomplete='ignore', fillvalue='x'))
    [('A', 'B', 'C'), ('D', 'E', 'F')]

    When *incomplete* is `'strict'`, a subclass of `ValueError` will be raised.

    >>> it = grouper('ABCDEFG', 3, incomplete='strict')
    >>> list(it)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    UnequalIterablesError

    """
    args = [iter(iterable)] * n
    if incomplete == 'fill':
        return zip_longest(*args, fillvalue=fillvalue)
    if incomplete == 'strict':
        return _zip_equal(*args)
    if incomplete == 'ignore':
        return zip(*args)
    else:
        raise ValueError('Expected fill, strict, or ignore')


def roundrobin(*iterables):
    """Yields an item from each iterable, alternating between them.

        >>> list(roundrobin('ABC', 'D', 'EF'))
        ['A', 'D', 'E', 'B', 'F', 'C']

    This function produces the same output as :func:`interleave_longest`, but
    may perform better for some inputs (in particular when the number of
    iterables is small).

    """
    # Recipe credited to George Sakkis
    pending = len(iterables)
    nexts = cycle(iter(it).__next__ for it in iterables)
    while pending:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = cycle(islice(nexts, pending))


def partition(pred, iterable):
    """
    Returns a 2-tuple of iterables derived from the input iterable.
    The first yields the items that have ``pred(item) == False``.
    The second yields the items that have ``pred(item) == True``.

        >>> is_odd = lambda x: x % 2 != 0
        >>> iterable = range(10)
        >>> even_items, odd_items = partition(is_odd, iterable)
        >>> list(even_items), list(odd_items)
        ([0, 2, 4, 6, 8], [1, 3, 5, 7, 9])

    If *pred* is None, :func:`bool` is used.

        >>> iterable = [0, 1, False, True, '', ' ']
        >>> false_items, true_items = partition(None, iterable)
        >>> list(false_items), list(true_items)
        ([0, False, ''], [1, True, ' '])

    """
    if pred is None:
        pred = bool

    evaluations = ((pred(x), x) for x in iterable)
    t1, t2 = tee(evaluations)
    return (
        (x for (cond, x) in t1 if not cond),
        (x for (cond, x) in t2 if cond),
    )


def powerset(iterable):
    """Yields all possible subsets of the iterable.

        >>> list(powerset([1, 2, 3]))
        [(), (1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)]

    :func:`powerset` will operate on iterables that aren't :class:`set`
    instances, so repeated elements in the input will produce repeated elements
    in the output. Use :func:`unique_everseen` on the input to avoid generating
    duplicates:

        >>> seq = [1, 1, 0]
        >>> list(powerset(seq))
        [(), (1,), (1,), (0,), (1, 1), (1, 0), (1, 0), (1, 1, 0)]
        >>> from more_itertools import unique_everseen
        >>> list(powerset(unique_everseen(seq)))
        [(), (1,), (0,), (1, 0)]

    """
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def unique_everseen(iterable, key=None):
    """
    Yield unique elements, preserving order.

        >>> list(unique_everseen('AAAABBBCCDAABBB'))
        ['A', 'B', 'C', 'D']
        >>> list(unique_everseen('ABBCcAD', str.lower))
        ['A', 'B', 'C', 'D']

    Sequences with a mix of hashable and unhashable items can be used.
    The function will be slower (i.e., `O(n^2)`) for unhashable items.

    Remember that ``list`` objects are unhashable - you can use the *key*
    parameter to transform the list to a tuple (which is hashable) to
    avoid a slowdown.

        >>> iterable = ([1, 2], [2, 3], [1, 2])
        >>> list(unique_everseen(iterable))  # Slow
        [[1, 2], [2, 3]]
        >>> list(unique_everseen(iterable, key=tuple))  # Faster
        [[1, 2], [2, 3]]

    Similary, you may want to convert unhashable ``set`` objects with
    ``key=frozenset``. For ``dict`` objects,
    ``key=lambda x: frozenset(x.items())`` can be used.

    """
    seenset = set()
    seenset_add = seenset.add
    seenlist = []
    seenlist_add = seenlist.append
    use_key = key is not None

    for element in iterable:
        k = key(element) if use_key else element
        try:
            if k not in seenset:
                seenset_add(k)
                yield element
        except TypeError:
            if k not in seenlist:
                seenlist_add(k)
                yield element


def unique_justseen(iterable, key=None):
    """Yields elements in order, ignoring serial duplicates

    >>> list(unique_justseen('AAAABBBCCDAABBB'))
    ['A', 'B', 'C', 'D', 'A', 'B']
    >>> list(unique_justseen('ABBCcAD', str.lower))
    ['A', 'B', 'C', 'A', 'D']

    """
    return map(next, map(operator.itemgetter(1), groupby(iterable, key)))


def iter_except(func, exception, first=None):
    """Yields results from a function repeatedly until an exception is raised.

    Converts a call-until-exception interface to an iterator interface.
    Like ``iter(func, sentinel)``, but uses an exception instead of a sentinel
    to end the loop.

        >>> l = [0, 1, 2]
        >>> list(iter_except(l.pop, IndexError))
        [2, 1, 0]

    Multiple exceptions can be specified as a stopping condition:

        >>> l = [1, 2, 3, '...', 4, 5, 6]
        >>> list(iter_except(lambda: 1 + l.pop(), (IndexError, TypeError)))
        [7, 6, 5]
        >>> list(iter_except(lambda: 1 + l.pop(), (IndexError, TypeError)))
        [4, 3, 2]
        >>> list(iter_except(lambda: 1 + l.pop(), (IndexError, TypeError)))
        []

    """
    try:
        if first is not None:
            yield first()
        while 1:
            yield func()
    except exception:
        pass


def first_true(iterable, default=None, pred=None):
    """
    Returns the first true value in the iterable.

    If no true value is found, returns *default*

    If *pred* is not None, returns the first item for which
    ``pred(item) == True`` .

        >>> first_true(range(10))
        1
        >>> first_true(range(10), pred=lambda x: x > 5)
        6
        >>> first_true(range(10), default='missing', pred=lambda x: x > 9)
        'missing'

    """
    return next(filter(pred, iterable), default)


def random_product(*args, repeat=1):
    """Draw an item at random from each of the input iterables.

        >>> random_product('abc', range(4), 'XYZ')  # doctest:+SKIP
        ('c', 3, 'Z')

    If *repeat* is provided as a keyword argument, that many items will be
    drawn from each iterable.

        >>> random_product('abcd', range(4), repeat=2)  # doctest:+SKIP
        ('a', 2, 'd', 3)

    This equivalent to taking a random selection from
    ``itertools.product(*args, **kwarg)``.

    """
    pools = [tuple(pool) for pool in args] * repeat
    return tuple(choice(pool) for pool in pools)


def random_permutation(iterable, r=None):
    """Return a random *r* length permutation of the elements in *iterable*.

    If *r* is not specified or is ``None``, then *r* defaults to the length of
    *iterable*.

        >>> random_permutation(range(5))  # doctest:+SKIP
        (3, 4, 0, 1, 2)

    This equivalent to taking a random selection from
    ``itertools.permutations(iterable, r)``.

    """
    pool = tuple(iterable)
    r = len(pool) if r is None else r
    return tuple(sample(pool, r))


def random_combination(iterable, r):
    """Return a random *r* length subsequence of the elements in *iterable*.

        >>> random_combination(range(5), 3)  # doctest:+SKIP
        (2, 3, 4)

    This equivalent to taking a random selection from
    ``itertools.combinations(iterable, r)``.

    """
    pool = tuple(iterable)
    n = len(pool)
    indices = sorted(sample(range(n), r))
    return tuple(pool[i] for i in indices)


def random_combination_with_replacement(iterable, r):
    """Return a random *r* length subsequence of elements in *iterable*,
    allowing individual elements to be repeated.

        >>> random_combination_with_replacement(range(3), 5) # doctest:+SKIP
        (0, 0, 1, 2, 2)

    This equivalent to taking a random selection from
    ``itertools.combinations_with_replacement(iterable, r)``.

    """
    pool = tuple(iterable)
    n = len(pool)
    indices = sorted(randrange(n) for i in range(r))
    return tuple(pool[i] for i in indices)


def nth_combination(iterable, r, index):
    """Equivalent to ``list(combinations(iterable, r))[index]``.

    The subsequences of *iterable* that are of length *r* can be ordered
    lexicographically. :func:`nth_combination` computes the subsequence at
    sort position *index* directly, without computing the previous
    subsequences.

        >>> nth_combination(range(5), 3, 5)
        (0, 3, 4)

    ``ValueError`` will be raised If *r* is negative or greater than the length
    of *iterable*.
    ``IndexError`` will be raised if the given *index* is invalid.
    """
    pool = tuple(iterable)
    n = len(pool)
    if (r < 0) or (r > n):
        raise ValueError

    c = 1
    k = min(r, n - r)
    for i in range(1, k + 1):
        c = c * (n - k + i) // i

    if index < 0:
        index += c

    if (index < 0) or (index >= c):
        raise IndexError

    result = []
    while r:
        c, n, r = c * r // n, n - 1, r - 1
        while index >= c:
            index -= c
            c, n = c * (n - r) // n, n - 1
        result.append(pool[-1 - n])

    return tuple(result)


def prepend(value, iterator):
    """Yield *value*, followed by the elements in *iterator*.

        >>> value = '0'
        >>> iterator = ['1', '2', '3']
        >>> list(prepend(value, iterator))
        ['0', '1', '2', '3']

    To prepend multiple values, see :func:`itertools.chain`
    or :func:`value_chain`.

    """
    return chain([value], iterator)


def convolve(signal, kernel):
    """Convolve the iterable *signal* with the iterable *kernel*.

        >>> signal = (1, 2, 3, 4, 5)
        >>> kernel = [3, 2, 1]
        >>> list(convolve(signal, kernel))
        [3, 8, 14, 20, 26, 14, 5]

    Note: the input arguments are not interchangeable, as the *kernel*
    is immediately consumed and stored.

    """
    kernel = tuple(kernel)[::-1]
    n = len(kernel)
    window = deque([0], maxlen=n) * n
    for x in chain(signal, repeat(0, n - 1)):
        window.append(x)
        yield sum(map(operator.mul, kernel, window))


def before_and_after(predicate, it):
    """A variant of :func:`takewhile` that allows complete access to the
    remainder of the iterator.

         >>> it = iter('ABCdEfGhI')
         >>> all_upper, remainder = before_and_after(str.isupper, it)
         >>> ''.join(all_upper)
         'ABC'
         >>> ''.join(remainder) # takewhile() would lose the 'd'
         'dEfGhI'

    Note that the first iterator must be fully consumed before the second
    iterator can generate valid results.
    """
    it = iter(it)
    transition = []

    def true_iterator():
        for elem in it:
            if predicate(elem):
                yield elem
            else:
                transition.append(elem)
                return

    # Note: this is different from itertools recipes to allow nesting
    # before_and_after remainders into before_and_after again. See tests
    # for an example.
    remainder_iterator = chain(transition, it)

    return true_iterator(), remainder_iterator


def triplewise(iterable):
    """Return overlapping triplets from *iterable*.

    >>> list(triplewise('ABCDE'))
    [('A', 'B', 'C'), ('B', 'C', 'D'), ('C', 'D', 'E')]

    """
    for (a, _), (b, c) in pairwise(pairwise(iterable)):
        yield a, b, c


def sliding_window(iterable, n):
    """Return a sliding window of width *n* over *iterable*.

        >>> list(sliding_window(range(6), 4))
        [(0, 1, 2, 3), (1, 2, 3, 4), (2, 3, 4, 5)]

    If *iterable* has fewer than *n* items, then nothing is yielded:

        >>> list(sliding_window(range(3), 4))
        []

    For a variant with more features, see :func:`windowed`.
    """
    it = iter(iterable)
    window = deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


def subslices(iterable):
    """Return all contiguous non-empty subslices of *iterable*.

        >>> list(subslices('ABC'))
        [['A'], ['A', 'B'], ['A', 'B', 'C'], ['B'], ['B', 'C'], ['C']]

    This is similar to :func:`substrings`, but emits items in a different
    order.
    """
    seq = list(iterable)
    slices = starmap(slice, combinations(range(len(seq) + 1), 2))
    return map(operator.getitem, repeat(seq), slices)


def polynomial_from_roots(roots):
    """Compute a polynomial's coefficients from its roots.

    >>> roots = [5, -4, 3]  # (x - 5) * (x + 4) * (x - 3)
    >>> polynomial_from_roots(roots)  # x^3 - 4 * x^2 - 17 * x + 60
    [1, -4, -17, 60]
    """
    # Use math.prod for Python 3.8+,
    prod = getattr(math, 'prod', lambda x: reduce(operator.mul, x, 1))
    roots = list(map(operator.neg, roots))
    return [
        sum(map(prod, combinations(roots, k))) for k in range(len(roots) + 1)
    ]


<<<<<<< HEAD
=======
def iter_index(iterable, value, start=0):
    """Yield the index of each place in *iterable* that *value* occurs,
    beginning with index *start*.

    See :func:`locate` for a more general means of finding the indexes
    associated with particular values.

    >>> list(iter_index('AABCADEAF', 'A'))
    [0, 1, 4, 7]
    """
    try:
        seq_index = iterable.index
    except AttributeError:
        # Slow path for general iterables
        it = islice(iterable, start, None)
        for i, element in enumerate(it, start):
            if element is value or element == value:
                yield i
    else:
        # Fast path for sequences
        i = start - 1
        try:
            while True:
                i = seq_index(value, i + 1)
                yield i
        except ValueError:
            pass


>>>>>>> 72864d1 (Tue 22 Aug 2023 02:44:06 PM CDT)
def sieve(n):
    """Yield the primes less than n.

    >>> list(sieve(30))
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    """
    isqrt = getattr(math, 'isqrt', lambda x: int(math.sqrt(x)))
<<<<<<< HEAD
    limit = isqrt(n) + 1
    data = bytearray([1]) * n
    data[:2] = 0, 0
    for p in compress(range(limit), data):
        data[p + p : n : p] = bytearray(len(range(p + p, n, p)))

    return compress(count(), data)
=======
    data = bytearray((0, 1)) * (n // 2)
    data[:3] = 0, 0, 0
    limit = isqrt(n) + 1
    for p in compress(range(limit), data):
        data[p * p : n : p + p] = bytes(len(range(p * p, n, p + p)))
    data[2] = 1
    return iter_index(data, 1) if n > 2 else iter([])
>>>>>>> 72864d1 (Tue 22 Aug 2023 02:44:06 PM CDT)


def batched(iterable, n):
    """Batch data into lists of length *n*. The last batch may be shorter.

    >>> list(batched('ABCDEFG', 3))
    [['A', 'B', 'C'], ['D', 'E', 'F'], ['G']]

    This recipe is from the ``itertools`` docs. This library also provides
    :func:`chunked`, which has a different implementation.
    """
<<<<<<< HEAD
=======
    if hexversion >= 0x30C00A0:  # Python 3.12.0a0
        warnings.warn(
            (
                'batched will be removed in a future version of '
                'more-itertools. Use the standard library '
                'itertools.batched function instead'
            ),
            DeprecationWarning,
        )

>>>>>>> 72864d1 (Tue 22 Aug 2023 02:44:06 PM CDT)
    it = iter(iterable)
    while True:
        batch = list(islice(it, n))
        if not batch:
            break
        yield batch
<<<<<<< HEAD
=======


def transpose(it):
    """Swap the rows and columns of the input.

    >>> list(transpose([(1, 2, 3), (11, 22, 33)]))
    [(1, 11), (2, 22), (3, 33)]

    The caller should ensure that the dimensions of the input are compatible.
    """
    # TODO: when 3.9 goes end-of-life, add stric=True to this.
    return zip(*it)


def matmul(m1, m2):
    """Multiply two matrices.
    >>> list(matmul([(7, 5), (3, 5)], [(2, 5), (7, 9)]))
    [[49, 80], [41, 60]]

    The caller should ensure that the dimensions of the input matrices are
    compatible with each other.
    """
    n = len(m2[0])
    return batched(starmap(dotproduct, product(m1, transpose(m2))), n)


def factor(n):
    """Yield the prime factors of n.
    >>> list(factor(360))
    [2, 2, 2, 3, 3, 5]
    """
    isqrt = getattr(math, 'isqrt', lambda x: int(math.sqrt(x)))
    for prime in sieve(isqrt(n) + 1):
        while True:
            quotient, remainder = divmod(n, prime)
            if remainder:
                break
            yield prime
            n = quotient
            if n == 1:
                return
    if n >= 2:
        yield n
>>>>>>> 72864d1 (Tue 22 Aug 2023 02:44:06 PM CDT)
