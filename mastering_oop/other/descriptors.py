from pathlib import Path
from typing import Type


# non-data descriptor


class PersistentState:
    """Abstract superclass to use a StateManager object; meant to be used as a
    base class for other classes that need to manage a persistent state"""

    # `_saved` will hold the path to the saved state file
    _saved: Path


class StateManager:
    """This class' objects are non-data descriptors; they set `_saved` in the instances of PersistentClass()."""

    def __init__(self, base: Path) -> None:
        # `base` specifies base directory where state files will be saved
        self.base = base

    def __get__(self, instance: PersistentState, owner: Type) -> Path:
        """This method is called, when `PersistentClass().state_path` is accessed.
        It only creates a file in a defined file path, saves the path in
        the instance's `_saved` and returns it."""
        if not hasattr(instance, "_saved"):
            class_path = self.base / owner.__name__  # add sub-directory to path
            class_path.mkdir(exist_ok=True, parents=True)
            # the essence of descriptors: sets (!) attribute in PersistentClass() instance:
            instance._saved = class_path / str(
                id(instance)
            )  # add file with name of instance-id
        return instance._saved  # also gets attribute


class PersistentClass(PersistentState):
    """The inheriting class sets `state_path` to an instantiated descriptor object with a path given."""

    # by inheritance, also has `_saved` as a class attribute, but it might still be empty

    # pass base path and get instance._saved from descriptor
    state_path = StateManager(
        Path.cwd() / "mastering_oop" / "other" / "state"
    )  # <-- this object is the descriptor

    def __init__(self, a: int, b: float) -> None:
        self.a = a
        self.b = b
        self.c: Optional[float] = None
        self.state_path.write_text(repr(vars(self)))

    def calculate(self, c: float) -> float:
        self.c = c
        self.state_path.write_text(repr(vars(self)))
        return self.a * self.b + self.c

    def __str__(self) -> str:
        return self.state_path.read_text()


# data descriptor

# this super short and overly complex part of the book is too complicated to understand
# without referring to additional material and practice


"""print("############### Try Out ###############")
from pprint import pprint

# create file and write init-state to `_saved` attribute of PersistentClass() instance
persistent = PersistentClass(a=1, b=2)
file_content = open(persistent._saved).read()
pprint(str(file_content))

# re-calculate and write state to `_saved` attribute of PersistentClass() instance
persistent.calculate(c=3)
file_content = open(persistent._saved).read()
pprint(str(file_content))"""
