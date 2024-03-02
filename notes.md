## Special methods

This table tries to define special methods by answering the following questions:
- what base classes have this method implemented and what is the default implementation
- when is the special method triggered
- what is it useful for

```python
class Class:
    __init__(self):
        pass

obj = Class()
```

```__init__``` - ```obj = Class(*args, **kwargs)```, init attributes can be type checked by mypy

```__bool__``` - ```if obj```

```__format__``` - ```f"{obj}", format(obj), {0}.format(obj)```

```__hash__``` - ```hash(obj)```, integer representation of object, either for faster search in collections (searching otherwise has quite a bad time complexity) or for cryptography; makes the object immutable, objects need a hash in order to be keys in a dict or elements in a set; default hash values compute directly from the id numbers, using modulo depending on architecture (they repeat); default hash values only exist, unless a ```__eq__``` is created, then the object becomes unhashable, until ```__hash__``` inherited from the `object` class is overwritten; set types use hash tables to perform adding or removing an element in  $O(1)$ compared to $O(n)$ in lists types, mappings also use hashing

```__eq__``` - ```obj is other_obj```, default inherited from `object` compares ids, set together with ```__hash__``` (include same attributes); equality tests involving floats should never be written with `==` (because of imprecisions), but rather with `abs(a-b)/a <= eps`, with `eps` being a small value that we define

```__del__``` - cleanly disentangle object from memory resource; invoked on another thread at a time that is not easily to be predicted; executes automatically when reference count of CPython goes to 0, but due to circular references, it cannot always go back to 0

```__new__``` - extend an (otherwise) immutable parent class, so that we can have an ```__init__``` method, that defines mutability; or: create a metaclass that controls how a class definition is build

```__dir__``` - reveal attribute names (attributes and methods) of an object, often coupled with ```__getattr__``` to account for dynamically computed attributes

```__dict__``` - shows all the data an object contains in dict format, only real attributes, no methods; is itself not a method an attribute instead

```__setattr__``` - ```obj.attribute = "bla"```, by default simply create and set attributes; can have property-like behaviour, but is not as secure; when we are not able to set a new attribute or change an existing one, the object is immutable, we can make this happen by implementing a custom ```__setattr__``` (it is easier to extend to NamedTuple to archive this, though); custom implementation also used to detect changes in attribute values and to then derive a specific action whenever attributes are being set (for instance computing derived attributes); attention: we cannot re-set the same attribute within ``__setattr__``, except for as a ```super().__setattr__(value)``` argument because it would create an infinite recursion

```__getattr__``` - triggered when ```obj.attribute``` does not exist, by default raises `AttributeError`; used as part of a larger process when the name of an attribute is unknown; can be overwritten with providing a meaningful result instead; common use for an attribute that doesn't compute it's values until they are needed; setting and getting attributes, we cannot call the same method from within, as this would cause an infinite recursion; as a workaround, we can use a super-class' getting or setting methods

```__delattr__``` - deletes attribute from object

```__slots__``` - replaces an object's ```__dict__```; makes it difficult to add new attributes; existing attributes remain mutable however; used to limit memory usage

```__post_init__``` - eagerly calculates attributes right after ```__init__``` is run, provided by classes decorated with the ```@dataclass``` decorator; it's an alternative to the ```@property``` decorator for properties

```__getattribute__``` - ```obj.attribute```, as a default implementation tries to locate attribute in the object's ```__dict__``` and returns it, if he attribute is not found calls ```__getattr__```; by overwriting, we can prevent access to attributes, or invent new attributes, or change how attributes or descriptors behave

```__call__``` - ```obj()```, object can be called as if it was a function; the advantage compared to a function (that is also a callable object) is that a class with ```__call__``` can be stateful: it can remember information that speeds up the calculations of the callable; but we can also decorate functions with `@lru_cache()` from `functools` to add a cache to a normal function

```__subclasshook__``` - invoked when a subclass of a parent class is build; used in abstract classes to check if the subclasses adhere to certain rules; the subclasses are only build if this method returns `True`

```__enter__``` - used in context managers to change global state or create a local context; used to store previous state in `self.something` and change state; return `self`

```__exit__``` - used in context managers to restore the previous state; takes `(self, exc_type, exc_value, traceback)` as arguments; all exceptions raised in `__enter__` are directed towards `__exit__` and can be raised here, depending whether `__exit__` returns `True` or `False`; if it returns `False` or any object with `bool(obj)==False`, then the exceptions will possibly raise; returning `True` or alike will silence the exceptions (for instance when they are already handled in the `__exit__` block)

```__contains__``` - `a in obj`, implements `in` operator in collections

```__iter__``` - `for i in obj` or `iter(obj)`, iteration in collection classes; can return an Iterator object or be a generator function

```__len__``` - `len(obj)`, for collection classes

```__getitem__``` - ```obj[index]```, uses slicing to get member of a `Sequence` type, $O(1)$

```__setitem__``` - ```obj[index] = value```, uses slicing to set member of a `MutableSequence` type, $O(1)$

```__delitem__``` - ```del obj[index]```, uses slicing to delete member of a `MutableSequence` type, $O(1)$

```__add__``` and other operants - left hand side object's operant will by tried first, except if the right hand side object's class is a subclass of the left one: then the right hand side object's reflected operant will by tried first

```__rsub__``` - reflected subtraction: reverts the order of both objects; used if the left hand object doesn't implement the required special method (like ```__sub__``) or if the right hand object's class is a subclass of the left hand side's object


## Descriptors
Used to customize attribute access.

An instance of a descriptor class is a class attribute in an owner class. The descriptor class must implement any combination of the following methods.

```Descriptor.__get__(self, instance, owner)``` - `instance` is an instance of the owing class, `owner` is the owning class

```Descriptor.__set__(self, instance, value)``` - `instance` is an instance of the owing class, `value` is the new value the descriptor needs to be set to

```Descriptor.__delete__(self, instance)``` - for deleting the attribute's value

A non-data descriptor only implements `__get__`, a data descriptor implements `__get__` and `__set__` and maybe `__delete__`.


## Build-in classes and creating custom classes
- classes to inherit from can be found in the `typing` module or in the several `abc` modules of the different build-in class types (for instance `collections.abc`) or in other places
-`abc`s (abstract base classes) fail to provide methods on purpose, so that the interpreter would raise, if inheriting classes don't implement them themselves. We have `abc`-decorators for classes intended to be collections in `collections`, but there are more `abc`-decorators, for instance in `numbers` for numeric types.
- the `abc`'s source code also shows what methods need to be implemented, as does the documentation, see: [Collections Abstract Base Classes](https://docs.python.org/3.12/library/collections.abc.html#collections-abstract-base-classes)
- when we build new classes, we need to know what methods come inherited with creating the class (those might have to be overwritten), and what methods we need to add, so that the required behaviour integrates nicely into the rest of the programme, for instance, when we want to build our own `MutableSequence` class (`list` also is one), then we need to implement or overwrite all its methods
- there are three ways to make up our own class:
  - extend: add functionality to existing collection class: `class NewClass(list)`
    - re-use or overwrite existing methods
  - wrap: surround an existing collection class: `class NewClass: #some method uses a list`
    - some methods will have to be delegated to the underlying container
  - self design: build new class from scratch


`deque` - double ended queue; in distinction with a list, it does not provide uniform performance for any element, but favours performance in the beginning and in the end of the collection; has a `pop()` method that is very efficient

`stack` - single ended queue (not sure if this is build into Python in fact)

`ChainMap` - chain of mappings; uses Python's principle to look for local keys first, then global ones

`defaultdict` - dict subclass that provides a factory method to create/calculate missing keys; unlike an ordinary dict, doesn't raise an exception for missing keys, but inserts a default value for any new key we give it, for instance `defaultdict(list)` will create an empty list by default for any key, that we request using `defaultdict(list)["nonexisting_key"]`; commonly used to create indices for objects

`Counter` - dict subclass used for counting objects; represents multiple occurrences of a value with an integer count; relies on the data structure `bag` (also called `multiset`); used as a frequency table; also implements set-like comparison operators like union or intersection

`NamedTuple` - tuple subclass with named attributes that contain immutable objects; expects a number of class level attributes (typically with type hints); it has a `__setattr__` method that prevents attributes from being set; a subclass can't add any new attributes, but it can add methods (not so sure how it differs with `Enum`)

`Enum` - used to build a unique set of constant values; values can be iterated over and compared for equality; useful working with a fixed set of choices; expects a number of class level attributes (not so sure how it differs with `NamedTuple`)

`OrderedDict` - mapping that keeps the original key order (all dicts do that, since Python 3.7, so this class now is redundant)


## Python in-build decorators
### class decorators
- are used as an alternative to a mixin class
- can implement both methods and attributes, but should be used for attributes only to avoid confusion (also, methods added by decorators cannot be overwritten or extended within the class or in a classes' subclass)
- are applied to the class after the mro (method resolution order) has been done when building the class

- `@dataclass`: can be used to implement additional default methods, this class gets another parent than `type`, because it has a different `metaclass` (probably deriving from `type` but being able to do more). The default `@dataclass` implements `__eq__`, `__gt__`, etc. for instance. There are also more specifications available, for instance `@dataclass(frozen=True)` makes the class immutable.
- `@functools.total_ordering`: creates the missing comparison methods after only implementing two of them: `__eq__` and any method evaluating to <, >, <=, >=; the other methods will automatically be generated and will be available

### method decorators
- `@property`: transforms a method into a descriptor (changes the method into an attribute of the object); also creates `@{method_name}.setter` and `@{method_name}.deleter`

- `@classmethod`: transforms a method into class-level function, that operates in the class space

- `@staticmethod`: transforms a method into class-level function, that syntactically belongs to the class, but is in the global space
