from typing import TypedDict


class Person(TypedDict):
    name: str
    age: int


new_person: Person = {"name": "john", "age": 35}
