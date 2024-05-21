import logging
import sys

from typing import Iterable, Any, Union, Type, Tuple, Dict, cast


class LoggedMeta(type):
    """metaclass that extends the build in `type` metaclass with their own version of __new__;
    it adds attributes to all classes deriving from the abc class that inherits from it
    """

    def __new__(
        cls: Type, name: str, bases: Tuple[Type, ...], namespace: Dict[str, Any]
    ) -> "Logged":
        """__new__ interferes with class creation process of type class. `Name` is the
        name of the new class being created; `bases` is a tuple of base classes from
        which the new class inherits; `namespace` is a dictionary containing the
        attributes and methods defined within the class body"""
        result = cast("Logged", super().__new__(cls, name, bases, namespace))
        result.logger = logging.getLogger(name) # sets a logger attribute on the class object
        return result # result is the new class object


# that's an abstract class, whose metaclass is not precisely `type` anymore
class Logged(metaclass=LoggedMeta):
    logger: logging.Logger  # odd syntax.... but `logging.Logger` is the mypy type hint
    # as a class attribute, logger is set for any instance of any child class


class SomeApplicationClass(Logged):
    """class derived from LoggedMeta: `name` is the name of this class
    (SomeApplicationClass), `bases` are the base classes of this class (Logged), and
    `namespace` dictionary includes information about the attributes and methods defined
    within SomeApplicationClass, for instance {'logger': <type 'logging.Logger'>}"""

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

app = SomeApplicationClass(4, 2)

# we need to change the logging configuration to see an output:
# logging.basicConfig defines the configuration for the root logger, but we can also build a hierarchy if we want
# stream=sys.stderr defines the standard error as a handler within this process (usually the console)
# level=logging.DEBUG defines the severity level to send a logging message to the handler
# it's best to do the configuration only once (on the top level of an application)
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
app.logger.info(f"This can now be logged: {app.v3}")

# flushes the in-build buffering; often used in a finally() block on the top level of an application
logging.shutdown()