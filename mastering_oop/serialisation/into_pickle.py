import pickle
from pathlib import Path
import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

from mastering_oop.serialisation.persistent_classes import Post, Blog_x

# pickle is explicitly written for serialising Python objects and its easy to
# retrieve Python objects from it

# pickle however is no data-interchange format that can be easily read by other languages


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


file_path = Path.cwd() / "mastering_oop" / "serialisation" / "ch10.pickle"

# dump pickle
with file_path.open("wb") as target:
    pickle.dump(travel_x, target)

# load pickle
with file_path.open("rb") as source: # file must be opened in "rb" mode, because we need to read binaries
    copy = pickle.load(source)

print(copy)
print(type(copy)) # it's a Blog_x() object!!!
