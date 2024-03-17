import json
import datetime
from pprint import pprint
from typing import List, Optional, Dict, Any, DefaultDict, Union, Type
from pathlib import Path

from mastering_oop.serialisation.persistent_classes import Post, Blog_x


# example Blog_x() object
travel_x = Blog_x("Travel")
travel_x.append(
    Post(
        date=datetime.datetime(2013, 11, 14, 17, 25),
        title="Hard Aground",
        rst_text="""Some embarrassing revelation. Including ☹ and ⚓""",
        tags=["#RedRanger", "#Whitby42", "#ICW"],
    )
)
travel_x.append(
    Post(
        date=datetime.datetime(2013, 11, 18, 15, 30),
        title="Anchor Follies",
        rst_text="""Some witty epigram. Including < & > characters.""",
        tags=["#RedRanger", "#Whitby42", "#Mistakes"],
    )
)

# Simple object dumping
# ---------------------
# json.dumps() doesn't write the object to a file, but to a string, so we can inspect
# if we want to write the object to a file, we need to use json.dump()
print("as_dict:")
print(json.dumps(travel_x.as_dict(), indent=4))
print('')
print("by_tag")
print(json.dumps(travel_x.by_tag(), indent=4))
print('')


# if we would load these objects the simple way, we would get dicts returned
# to re-create our custom Python objects from a json file, we need to use so called "object hooks";
# these are functions that create custom objects from dicts
# we use these functions for encoding and decoding

# JSON encoding with object hooks
# -------------------------------
def blogx_encode(object: Any) -> Dict[str, Any]:
    if isinstance(object, datetime.datetime):
        return dict(
            __class__="datetime.datetime",
            __args__=[],
            __kw__=dict(
                year=object.year,
                month=object.month,
                day=object.day,
                hour=object.hour,
                minute=object.minute,
                second=object.second,
            ),
        )
    elif isinstance(object, Post):
        return dict(
            __class__="Post",
            __args__=[],
            __kw__=dict(
                date=object.date,
                title=object.title,
                rst_text=object.rst_text,
                tags=object.tags,
            ),
        )
    elif isinstance(object, Blog_x):
        # Will get ignored...
        return dict(
            __class__="Blog_x",
            __args__=[],
            __kw__=dict(title=object.title, entries=tuple(object)),
        )
    else:
        return object

text = json.dumps(travel_x, indent=4, default=blogx_encode)
print(text)
print('')


# JSON decoding with object hooks
# -------------------------------
def blogx_decode(some_dict: Dict[str, Any]) -> Dict[str, Any]:
    if set(some_dict.keys()) == set(["__class__", "__args__", "__kw__"]):
        class_ = eval(some_dict["__class__"]) # eval reads Python code that is a string and executes it
        return class_(*some_dict["__args__"], **some_dict["__kw__"])
    else:
        return some_dict

# comes back as a list
copy = json.loads(text, object_hook=blogx_decode)
pprint(copy)


# Writing and loading from file
# -----------------------------

file_path = Path.cwd() / "mastering_oop" / "serialisation" / "ch10.json"

with file_path.open("w", encoding="UTF-8") as target:
    json.dump(text, target, separators=(",", ":"), default=blogx_encode)

with file_path.open("r", encoding="UTF-8") as source:
    objects = json.load(source, object_hook=blogx_decode)

print(objects)
print(type(objects)) # these are strings
