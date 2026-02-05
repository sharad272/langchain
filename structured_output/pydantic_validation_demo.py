# Demonstrating Pydantic validation behavior
from pydantic import BaseModel, ValidationError

class Person(BaseModel):
    name: str
    age: int

print("=" * 60)
print("SUCCESSFUL CASES (with type coercion):")
print("=" * 60)

# Case 1: Exact types - works
person1 = Person(name="Alice", age=30)
print(f"1. name='Alice', age=30 -> {person1}")

# Case 2: String that looks like number - works (it's already a string!)
person2 = Person(name="32", age=30)
print(f"2. name='32', age=30 -> {person2}")

# Case 3: Integer as name - COERCED to string
person3 = Person(name=32, age=30)
print(f"3. name=32, age=30 -> {person3}")
print(f"   Type of name: {type(person3.name)}")

# Case 4: String as age - COERCED to integer
person4 = Person(name="Bob", age="25")
print(f"4. name='Bob', age='25' -> {person4}")
print(f"   Type of age: {type(person4.age)}")

print("\n" + "=" * 60)
print("VALIDATION ERROR CASES:")
print("=" * 60)

# Case 5: Can't convert string to int - FAILS
try:
    person5 = Person(name="Charlie", age="not_a_number")
except ValidationError as e:
    print(f"5. name='Charlie', age='not_a_number' -> ERROR!")
    print(f"   {e.errors()[0]['msg']}")

# Case 6: Float for age - might work or fail depending on version
try:
    person6 = Person(name="Diana", age=25.5)
    print(f"6. name='Diana', age=25.5 -> {person6} (converted to int)")
except ValidationError as e:
    print(f"6. name='Diana', age=25.5 -> ERROR!")
    print(f"   {e.errors()[0]['msg']}")

# Case 7: List as name - might get coerced to string
try:
    person7 = Person(name=["Eve"], age=30)
    print(f"7. name=['Eve'], age=30 -> {person7}")
except ValidationError as e:
    print(f"7. name=['Eve'], age=30 -> ERROR!")
    print(f"   {e.errors()[0]['msg']}")

print("\n" + "=" * 60)
print("KEY TAKEAWAY:")
print("=" * 60)
print("Pydantic performs TYPE COERCION before validation.")
print("It will try to convert compatible types automatically.")
print("Validation errors only occur when conversion is impossible.")
