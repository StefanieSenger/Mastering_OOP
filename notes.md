## Special methods and how they are triggered

```python
class Class:
    __init__(self):
        pass

obj = Class()
```

```__init__``` - ```obj = Class(*args, **kwargs)```, init attributes can me type checked by mypy

```__getitem__``` - ```obj[index]```

```__bool__``` - ```if obj```

```__format__``` - ```f"{obj}", format(obj), {0}.format(obj)```

```__hash__``` - ```hash(obj)```, integer prepresentation of object, either for faster search in collections or for cryptography; objects need a hash in order to be keys in a dict; default hash values compute directly from the id numbers, using modulo depending on architecture (they repeat); default hash values only exist, unless a ```__eq__``` is created, then the object becomes unhashable, until a ```__hash__``` is implemented as well

```__eq__``` - ```obj is other_obj```, default compares ids, set together with ```__hash__``` (include same attributes)

```__del__``` - cleanly disentangle object from memory resource; invoked on another thread at a time that is not easily to be predicted; executes automatically when reference count of CPython goes to 0, but due to circular references, it cannot always go back to 0

```__new__``` - extend an (otherwise) immutable parent class, so that we can have an ```__init__``` method, that defines mutability; or: create a metaclass that controlls how a class definition is build
