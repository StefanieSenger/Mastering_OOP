import logging

from typing import Iterable, Any, Union, Type, Tuple, Dict, cast


class LoggedMeta(type):
    """metaclass that extends the build in `type` metaclass with their own version of __new__;
    it adds attributes to all classes deriving from the abc class that inherits from it
    """

    def __new__(
        cls: Type, name: str, bases: Tuple[Type, ...], namespace: Dict[str, Any]
    ) -> "Logged":
        result = cast("Logged", super().__new__(cls, name, bases, namespace))
        result.logger = logging.getLogger(name)
        return result


# that's an abstract class, whose metaclass is not precisely `type` anymore
class Logged(metaclass=LoggedMeta):
    logger: logging.Logger  # odd syntax.... but `logging.Logger` is the mypy type hint


class SomeApplicationClass(Logged):

    def __init__(self, v1: int, v2: int) -> None:
        self.logger.info("v1=%r, v2=%r", v1, v2)
        self.v1 = v1
        self.v2 = v2
        self.v3 = v1 * v2
        self.logger.info("product=%r", self.v3)


print("############### Try Out ###############")
print(type(LoggedMeta))  # of type `type`
print(type(Logged))  # of type `LoggedMeta`
print(type(SomeApplicationClass))  # of type `LoggedMeta`

app = SomeApplicationClass(1, 2)
app.logger.info("This can now be logged: {self.v3}")
