import json
from abc import ABC
from pathlib import Path
from typing import Dict, Iterable, Union

from pydantic import BaseModel, Extra, create_model

Child = Union[str, "Element"]


class Element(ABC, BaseModel, extra=Extra.forbid):

    children: Union[Child, Iterable[Child]] = None
    aria_: Dict[str, str] = {}
    data_: Dict[str, str] = {}

    def __str__(self):
        tag = self.__class__.__name__.lower()  # get the html tag name

        # generate all the html attributes
        attrs = self.dict()
        attrs.pop("children")  # this field is dealt with specially
        attrs["class"] = attrs.pop("classes")  # renamed since it's a reserved keyword
        for k, v in attrs.pop("aria_").items():  # flatten nested aria-* attributes
            attrs[f"aria-{k}"] = v
        for k, v in attrs.pop("data_").items():  # flatten nested data-* attributes
            attrs[f"data-{k}"] = v
        attrs = {k: v for k, v in attrs.items() if v is not None}  # discard None values
        attrs = {k.replace("_", "-"): v for k, v in attrs.items()}  # convert snake_case

        # None children should produce empty html elements
        if self.children is None:
            children = ""
        # strings are passed through without conversion
        elif isinstance(self.children, str):
            children = self.children
        # individual Elements are recursively converted to strings
        elif isinstance(self.children, self.__class__.__bases__):
            children = str(self.children)
        # the only valid case remaining is an iterable of Elements, also recursively converted
        else:
            children = "\n".join(str(child) for child in self.children)

        # write out the html tag
        attr_str = " ".join(f"{key}='{value}'" for key, value in attrs.items())
        html_str = f"<{tag} {attr_str}>\n{children}\n</{tag}>"
        return html_str


# read in the saved attributes
thisdir = Path(__file__).parent
with open(thisdir / "classes.json") as f:
    classes = json.load(f)

# create a model for each element and make it importable by name from the module's namespace
__all__ = []
for element, attrs in classes.items():
    name = element.title()
    field_definitions = {attr: (str, None) for attr in attrs}
    globals()[name] = create_model(name, **field_definitions, __base__=Element)
    __all__.append(name)
