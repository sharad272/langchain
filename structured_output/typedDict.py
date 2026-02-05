# 1st way to get structured output is to use a TypedDict no data validation
from typing import TypedDict
class Person(TypedDict):
    name: str
    age: int


new_person = Person(name="John Doe", age=30)
print(new_person)