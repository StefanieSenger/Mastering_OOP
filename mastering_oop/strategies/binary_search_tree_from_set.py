from abc import ABCMeta, abstractmethod
from collections.abc import MutableSet
from typing import Iterable, Any, Iterator, Optional, cast
import weakref

# Here, we create a binary search tree that uses the MutableSet class from collections.abc as a base class.
# Python documentation tells us which method our class needs to implement (those MutableSet provides as abstract methods)
# and which methods are also provided which we might want to overwrite:
# https://docs.python.org/3.12/library/collections.abc.html#collections-abstract-base-classes


class Comparable(metaclass=ABCMeta):
    """used for the type hint to restrain the type of values our knots and leaves can contain;
    those  two methods fulfill the minimal requirements, from where ABCMeta can deduce all the others
    (unlike the object class that needs everything)"""

    def __lt__(self, other: Any) -> bool:
        pass

    def __ge__(self, other: Any) -> bool:
        pass

class Tree(MutableSet):
    """Facade class that will contain TreeNode() objects;
    abstract superclass provides a default implementation of remove() and many other features"""

    def __init__(self, source: Iterable[Comparable] = None) -> None:
        self.root = TreeNode(None)
        self.size = 0
        if source:
            for item in source: #source is iterable
                self.root.add(item)
                self.size += 1

    def add(self, item: Comparable) -> None:
        """delegates adding to the TreeNode object at the root of their tree,
        and keeps track of the Tree's size"""
        self.root.add(item)
        self.size += 1

    def discard(self, item: Comparable) -> None:
        """delegates deleting to the TreeNode object at the root of their tree,
        and keeps track of the Tree's size; MutableSets require this method, because they have it implemented as an abstract class
        see: https://docs.python.org/3.12/library/collections.abc.html#collections-abstract-base-classes"""
        if self.root.more:
            try:
                self.root.more.remove(item)
                self.size -= 1
            except KeyError:
                pass
        else:
            pass

    def __contains__(self, item: Any) -> bool:
        if self.root.more:
            self.root.more.find(cast(Comparable, item))
            return True
        else:
            return False

    def __iter__(self) -> Iterator[Comparable]:
        """generator function that delegates the real work into the recursive iterator in the TreeNode class"""
        if self.root.more:
            for item in iter(self.root.more):
                yield item
        # Otherwise, the tree is empty.

    def __len__(self) -> int:
        return self.size


class TreeNode:
    """bla
    """

    def __init__(
        self,
        item: Optional[Comparable],
        less: Optional["TreeNode"] = None,
        more: Optional["TreeNode"] = None,
        parent: Optional["TreeNode"] = None,
    ) -> None:
        self.item = item
        self.less = less
        self.more = more
        if parent:
            # Can't create a weakref to a None value. Only set if there's a value
            self.parent = parent

    @property
    # the property getter and setter are used to make sure that the parent is actually a weakref but appears as a strong reference
    def parent(self) -> Optional["TreeNode"]:
        return self.parent_ref()

    @parent.setter
    def parent(self, value: "TreeNode") -> None:
        """weakref, a reference that does not increase the reference count of the referenced object
        and allows it to be garbage collected; returns the referenced object if it is still alive,
        otherwise None if the object has been garbage collected.
        In general, we use weakrefs here, because the circular references would it make difficult
        to remove TreeNode objects otherwise."""
        self.parent_ref = weakref.ref(value)

    def __repr__(self) -> str:
        return f"TreeNode({self.item!r}, {self.less!r}, {self.more!r})"

    def find(self, item: Comparable) -> "TreeNode":
        if self.item is None:  # Root
            if self.more:
                return self.more.find(item) # recursion
        elif self.item == item:
            return self
        elif self.item > item and self.less:
            return self.less.find(item) # recursion
        elif self.item < item and self.more:
            return self.more.find(item) # recursion
        raise KeyError

    def __iter__(self) -> Iterator[Comparable]:
        """using a generator function that yields recursively"""
        if self.less:
            yield from self.less
        if self.item:
            yield self.item
        if self.more:
            yield from self.more

    def add(self, item: Comparable) -> None:
        if self.item is None:  # Root Special Case
            if self.more:
                self.more.add(item)
            else:
                self.more = TreeNode(item, parent=self)
        elif self.item >= item:
            if self.less:
                self.less.add(item)
            else:
                self.less = TreeNode(item, parent=self)
        elif self.item < item:
            if self.more:
                self.more.add(item)
            else:
                self.more = TreeNode(item, parent=self)

    def remove(self, item: Comparable) -> None:
        # Recursive search for node; since the nodes link weakly to each other, memory space can be recovered by garbage collector
        if self.item is None or item > self.item:
            if self.more:
                self.more.remove(item)
            else:
                raise KeyError
        elif item < self.item:
            if self.less:
                self.less.remove(item)
            else:
                raise KeyError
        else:  # self.item == item
            if self.less and self.more:  # Two children are present
                successor = self.more._least()
                self.item = successor.item
                if successor.item:
                    successor.remove(successor.item)
            elif self.less:  # One child on less
                self._replace(self.less)
            elif self.more:  # One child on more
                self._replace(self.more)
            else:  # Zero children
                self._replace(None)

    def _least(self) -> "TreeNode":
        if self.less is None:
            return self
        return self.less._least()

    def _replace(self, new: Optional["TreeNode"] = None) -> None:
        if self.parent:
            if self == self.parent.less:
                self.parent.less = new
            else:
                self.parent.more = new
        if new is not None:
            new.parent = self.parent


print("############### Try Out ###############")

bt = Tree()

# test add()
bt.add("Number 1")
print(list(iter(bt)))
bt.add("Number 3")
print(list(iter(bt)))
bt.add("Number 2")
print(list(iter(bt)))

# print repr()
print(repr(bt.root))

# test __contains__
print("Number 2" in bt)

# test __len__
print(len(bt))

# test remove()
bt.remove("Number 3")
print(list(iter(bt)))

# not sure what this does
bt.discard("Number 3")  # Should be silent

# add same value
bt.add("Number 1")
print(list(iter(bt))) # strange that this adds the new value and doesn't skip it
# I think add() should be implemented in another way, because this is not set-like

bt2 = Tree(["item",  "some other item", "yet another"])

# union operator works since __ior__ is implemented in any Set type: https://docs.python.org/3.12/library/collections.abc.html#collections-abstract-base-classes
union = bt | bt2
print(list(union))
