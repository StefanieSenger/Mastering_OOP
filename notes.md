## Special methods and how they are triggered

```python
class Class:
    __init__(self):
        pass

obj = Class()
```

```__init__``` - ```obj = Class(*args, **kwargs)```, init attributes can be type checked by mypy

```__getitem__``` - ```obj[index]```

```__bool__``` - ```if obj```

```__format__``` - ```f"{obj}", format(obj), {0}.format(obj)```

```__hash__``` - ```hash(obj)```, integer representation of object, either for faster search in collections or for cryptography; objects need a hash in order to be keys in a dict; default hash values compute directly from the id numbers, using modulo depending on architecture (they repeat); default hash values only exist, unless a ```__eq__``` is created, then the object becomes unhashable, until a ```__hash__``` is implemented as well

```__eq__``` - ```obj is other_obj```, default compares ids, set together with ```__hash__``` (include same attributes)

```__del__``` - cleanly disentangle object from memory resource; invoked on another thread at a time that is not easily to be predicted; executes automatically when reference count of CPython goes to 0, but due to circular references, it cannot always go back to 0

```__new__``` - extend an (otherwise) immutable parent class, so that we can have an ```__init__``` method, that defines mutability; or: create a metaclass that controls how a class definition is build

```__dir__``` - reveal attribute names (attributes and methods) of an object, often coupled with ```__getattr__``` to account for dynamically computed attributes

```__dict__``` - shows all the data an object contains in dict format, only real attributes, no methods; is itself not a method an attribute instead

```__setattr__``` - ```obj.attribute = "bla"```, by default simply create and set attributes; can have property-like behaviour, but is not as secure; when we are not able to set a new attribute or change an existing one, the object is immutable, we can make this happen by implementing a custom ```__setattr__``` (it is easier to extend to NamedTuple to archive this, though); custom implementation also used to detect changes in attribute values and to then derive a specific action whenever attributes are being set (for instance computing derived attributes); attention: we cannot re-set the same attribute within ``__setattr__``, except for as a ```super().__setattr__(value)``` argument because it would create an infinite recursion

```__getattr__``` - triggered when ```obj.attribute``` does not exist, by default raises `AttributeError`; used as part of a larger process when the name of an attribute is unknown; can be overwritten with providing a meaningful result instead; common use for an attribute that doesn't compute it's values until they are needed

```__delattr__``` - deletes attribute from object

```__slots__``` - replaces an object's ```__dict__```; makes it difficult to add new attributes; existing attributes remain mutable however; used to limit memory usage

```__post_init__``` - eagerly calculates attributes right after ```__init__``` is run, provided by classes decorated with the ```@dataclass``` decorator; it's an alternative to the ```@property``` decorator for properties

```__getattribute__``` - ```obj.attribute```, as a default implementation tries to locate attribute in the object's ```__dict__``` and returns it, if he attribute is not found calls ```__getattr__```; by overwriting, we can prevent access to attributes, or invent new attributes, or change how attributes or descriptors behave

```__call__``` - ```obj()```, object can be called as if it was a function; the advantage compared to a function (that is also a callable object) is that a class with ```__call__``` can be stateful: it can remember information that speeds up the calculations of the callable; but we can also decorate functions with `@lru_cache()` from `functools` to add a cache to a normal function

```__subclasshook__``` - invoked when a subclass of a parent class is build; used in abstract classes to check if the subclasses adhere to certain rules; the subclasses are only build if this method returns `True`

```__enter__``` - used in context managers to change global state or create a local context; used to store previous state in `self.something` and change state; return `self`

```__exit__``` - used in context managers to restore the previous state; takes `(self, exc_type, exc_value, traceback)` as arguments; all exceptions raised in `__enter__` are directed towards `__exit__` and can be raised here, depending whether `__exit__` returns `True` or `False`; if it returns `False` or any object with `bool(obj)==False`, then the exceptions will possibly raise; returning `True` or alike will silence the exceptions (for instance when they are already handled in the `__exit__` block)


## More general info
With setting and getting attributes, we cannot call the same method from within, as this would cause an infinite recursion. As a workaround, we can use a super-class' getting or setting methods.

`@dataclass` class decorator: can be used to implement additional default methods, this class gets another parent than `type`, because it has a different `metaclass` (probably deriving from `type` but being able to do more). The default `@dataclass` implements `__eq__`, `__gt__`, etc. for instance. There are also more specifications available, for instance `@dataclass(frozen=True)` makes the class immutable.

`abc`s (abstract base classes) fail to provide methods on purpose, so that the interpreter would raise, if inheriting classes don't implement them themselves. We have `abc`-decorators for classes intended to be collections in `collections`, but there are more `abc`-decorators, for instance in `numbers` for numeric types.


## Descriptors
Used to customize attribute access.

An instance of a descriptor class is a class attribute in an owner class. The descriptor class must implement any combination of the following methods.

```Descriptor.__get__(self, instance, owner)``` - `instance` is an instance of the owing class, `owner` is the owning class

```Descriptor.__set__(self, instance, value)``` - `instance` is an instance of the owing class, `value` is the new value the descriptor needs to be set to

```Descriptor.__delete__(self, instance)``` - for deleting the attribute's value

A non-data descriptor only implements `__get__`, a data descriptor implements `__get__` and `__set__` and maybe `__delete__`.
