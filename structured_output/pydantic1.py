# 2nd way to get structured output is to use a Pydantic model with data validation
from pydantic import BaseModel, EmailStr
class Person(BaseModel):
    name: str
    age: int
    email: EmailStr

new_person = Person(name="Sharad", age="30", email="sharad@gmail.com")
print(new_person)