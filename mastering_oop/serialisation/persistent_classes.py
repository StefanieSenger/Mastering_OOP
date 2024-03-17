from typing import List, Optional, Dict, Any, DefaultDict, Union, Type
from pathlib import Path
import datetime
from dataclasses import dataclass
from collections import defaultdict
import json

# @dataclass decorator automatically generates special methods such as
# __init__, __repr__, __eq__, __ne__, and __hash__, based on the class attributes.
@dataclass
class Post:
    """Simple dataclass, that can be serialised into a dict."""
    date: datetime.datetime
    title: str
    rst_text: str
    tags: List[str]

    def as_dict(self) -> Dict[str, Any]: # type hint represents JSON standards
        return dict(
            date=str(self.date),
            title=self.title,
            underline="-" * len(self.title), # result will be in reST format
            rst_text=self.rst_text,
            tag_text=" ".join(self.tags),
        )


class Blog_x(list):
    """Collection class that extends a list.
    Apart from holding a list of Post() objects, it also has its own title."""

    def __init__(self, title: str, posts: Optional[List[Post]]=None) -> None:
        self.title = title
        super().__init__(posts if posts is not None else [])

    def by_tag(self) -> DefaultDict[str, List[Dict[str, Any]]]:
        tag_index: DefaultDict[str, List[Dict[str, Any]]] = defaultdict(list)
        for post in self:
            for tag in post.tags:
                tag_index[tag].append(post.as_dict())
        return tag_index

    def as_dict(self) -> Dict[str, Any]:
        return dict(
            title=self.title,
            entries=[p.as_dict() for p in self]
        )


# An example blog
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


'''print("############### Try Out ###############")
print(travel_x)
print('')
print(travel_x.as_dict())
print('')
print(travel_x.by_tag())'''
