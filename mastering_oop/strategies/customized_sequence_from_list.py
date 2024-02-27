from typing import List, cast, Any, Optional, Iterable, overload, Union, Iterator
import math


class StatsListLazy(list):
    """class extends list by inheriting from it and adding new methods: `mean` and `stdev`"""

    def __init__(self, iterable: Optional[Iterable[float]]) -> None: # complex type hint for list type, because we need numbers as members
        super().__init__(cast(Iterable[Any], iterable))

    @property # lazy calculation
    def mean(self) -> float:
        return sum(self) / len(self)

    @property # lazy calculation
    def stdev(self) -> float:
        n = len(self)
        return math.sqrt(n * sum(x ** 2 for x in self) - sum(self) ** 2) / n


class StatsListEager(list):
    """class extends list and eagerly computes stats by overwriting some methods;
    quite a lot methods need to be overwritten, because the MutableSequence() aka list() uses them all,
    see: https://docs.python.org/3.4/library/collections.abc.html#collections-abstract-base-classes"""

    def __init__(self, iterable: Optional[Iterable[float]]) -> None:
        self.sum0 = 0  # len(self), sometimes called "N"
        self.sum1 = 0.0  # sum(self)
        self.sum2 = 0.0  # sum(x**2 for x in self)
        super().__init__(cast(Iterable[Any], iterable))
        for x in self:
            self._new(x)

    def _new(self, value: float) -> None:
        self.sum0 += 1
        self.sum1 += value
        self.sum2 += value * value

    def _rmv(self, value: float) -> None:
        self.sum0 -= 1
        self.sum1 -= value
        self.sum2 -= value * value

    def insert(self, index: int, value: float) -> None:
        super().insert(index, value)
        self._new(value)

    def pop(self, index: int = 0) -> None:
        value = super().pop(index)
        self._rmv(value)
        return value

    def append(self, value: float) -> None:
        super().append(value)
        self._new(value)

    def extend(self, sequence: Iterable[float]) -> None:
        super().extend(sequence)
        for value in sequence:
            self._new(value)

    def remove(self, value: float) -> None:
        super().remove(value)
        self._rmv(value)

    def __iadd__(self, sequence: Iterable[float]) -> "StatsList2":
        for v in sequence:
            self.append(v)
        return self

    def __add__(self, sequence: Iterable[float]) -> "StatsList2":
        generic = super().__add__(cast(StatsList2, sequence))
        result = StatsList2(generic)
        return result

    @property
    def mean(self) -> float:
        return self.sum1 / self.sum0

    @property
    def stdev(self) -> float:
        return math.sqrt(self.sum0 * self.sum2 - self.sum1 * self.sum1) / self.sum0



class Explore(list):

    # There are two overloaded definitions, the type hints tend to be complex for this case
    def __getitem__(self, index):
        # slice objects have start, stop and step in their index.indices(len(self)),
        # the first three values are the inputs, the next three values are the absolute indices:
        print(index, index.indices(len(self)))
        return super().__getitem__(index)


class StatsListWithItemGetterSetterDeleter(StatsListEager):
    "class uses __getitem__, __setitem__ and __delitem__; those involve slices"

    @overload # using this to provide propper type hints for `obj[int]`
    def __setitem__(self, index: int, value: float) -> None:
        ...

    @overload # using this to provide propper type hints for `obj[int:int:int]`
    def __setitem__(self, index: slice, value: Iterable[float]) -> None:
        ...

    def __setitem__(self, index, value) -> None:
        """condition on whether the indices are provided as an it or as a slice"""
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self)) # read out indices from slice object
            olds = [self[i] for i in range(start, stop, step)]
            # run superclass method to keep old behaviour (we only want to change the dynamic calculation of _rmv and _new):
            super().__setitem__(index, value)
            for x in olds:
                self._rmv(x)
            for x in value:
                self._new(x)
        else:
            old = self[index]
            # run superclass method to keep old behaviour (we only want to change the dynamic calculation of _rmv and _new):
            super().__setitem__(index, value)
            self._rmv(old)
            self._new(value)

    def __delitem__(self, index: Union[int, slice]) -> None: # just a different way to do the type hints
    # Index may be a single integer, or a slice
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            olds = [self[i] for i in range(start, stop, step)]
            super().__delitem__(index)
            for x in olds:
                self._rmv(x)
        else:
            old = self[index]
            super().__delitem__(index)
            self._rmv(old)


class StatsListWrappingList:
    """class that only uses some of the methods, list() implements,
    in this case only append and __getitem__"""

    def __init__(self) -> None:
        self._list: List[float] = list() # instantiate as empty list
        self.sum0 = 0  # len(self), sometimes called "N"
        self.sum1 = 0.  # sum(self)
        self.sum2 = 0.  # sum(x**2 for x in self)

    def append(self, value: float) -> None:
        self._list.append(value) # use the append() method from list object
        self.sum0 += 1
        self.sum1 += value
        self.sum2 += value * value

    # etc.

    def __getitem__(self, index: int) -> float:
        return self._list.__getitem__(index)

    @property
    def mean(self) -> float:
        return self.sum1 / self.sum0

    @property
    def stdev(self) -> float:
        return math.sqrt(self.sum0 * self.sum2 - self.sum1 * self.sum1) / self.sum0

    def __hash__(self):
        """because the object is mutable; otherwise the hash value would be a value,
        because we have inherited from object class"""
        return None


print("############### Try Out ###############")

# StatsListLazy
stats_list = StatsListLazy(iterable=[1,4,19999])
print(f"mean: {stats_list.mean}")
print(f"stdev: {stats_list.stdev}\n")

# StatsListEager
stats_list = StatsListEager(iterable=[1,4,3])
print(f"sum0: {stats_list.sum0}, sum1: {stats_list.sum1}, sum2: {stats_list.sum2}")
print(f"mean: {stats_list.mean}")
print(f"stdev: {stats_list.stdev} \n")

stats_list.append(0)
print(f"sum0: {stats_list.sum0}, sum1: {stats_list.sum1}, sum2: {stats_list.sum2}")
print(f"mean: {stats_list.mean}")
print(f"stdev: {stats_list.stdev} \n")

stats_list.pop()
print(f"sum0: {stats_list.sum0}, sum1: {stats_list.sum1}, sum2: {stats_list.sum2}")
print(f"mean: {stats_list.mean}")
print(f"stdev: {stats_list.stdev} \n")

# Explore
explore = Explore("abcdefg")
print(explore[:])
print(explore[:-1])
print(explore[::2], " \n")

# StatsListWithItemGetterSetterDeleter
stats_list = StatsListWithItemGetterSetterDeleter(iterable=[0, 0, 0, 2])
del stats_list[-2]
print(f"sum0: {stats_list.sum0}, sum1: {stats_list.sum1}, sum2: {stats_list.sum2}")
print(f"mean: {stats_list.mean}")
print(f"stdev: {stats_list.stdev} \n")

stats_list[2] = 3
print(f"sum0: {stats_list.sum0}, sum1: {stats_list.sum1}, sum2: {stats_list.sum2}")
print(f"mean: {stats_list.mean}")
print(f"stdev: {stats_list.stdev} \n")

# StatsListWrappingList
stats_list = StatsListWrappingList()
stats_list.append(-10)
stats_list.append(-20)
print(stats_list[1])
print(f"sum0: {stats_list.sum0}, sum1: {stats_list.sum1}, sum2: {stats_list.sum2}")
print(f"mean: {stats_list.mean}")
print(f"stdev: {stats_list.stdev} \n")

# this is possible, because __getitem__ makes __iter__ work:
for ele in stats_list:
    print(ele)

# this breaks, because we didn't implement __len__:
try:
    len(stats_list)
except TypeError as e:
    print(e)
