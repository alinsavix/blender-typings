# Random typing notes

## Subtype

### Rules

`T` is a subtype of `U` if:

- Every value from `T` is also in the set of values of `U` type

  AND

- Every function of type `U` is also in the set of functions of type `T`

### Thus

- variables of type `T` can always pretend to be type `U`
- The set of values becomes smaller with subtyping
- The set of functions becomes larger

### Examples

`bool` is a subtype of `int`

`Dog` is subtype of `Animal`; The set of `Dog` is smaller than the set of `Animal` AND `Dog` has more functions (e.g. can `bark()`) in addition to anything `Animal` can do

### Formal Syntax

```math
  SubType <: SuperType
```

## Invariant

### Rules

Generic type `GenType[T, ...]` is invariant in type variable `T` if `GenType` is neither covariant in type variable `T` nor contravariant in type variable `T`

### Thus

- mutable containers are usually invariant
- e.g. these are invariant: `List`, `Dict`, `Set`
- You can't use `List[T]` as a drop-in replacement for `List[U]` even if `T <: U`, because something might append something of type `U` to the list, which makes it no longer `List[T]`

### Examples

- Dict[A, B] won't accept Dict[A, C], even if C is a subtype of B

```python
def append_kangaroo(animals: List[Animal]) -> None:
    animal = Kangaroo()
    # it's okay, since `Kangaroo <: Animal`
    animals.append(animal)

dogs: List[Dog] = []

lassie = Dog()
dogs.append(lassie)

append_kangaroo(dogs)

dogs[0].eat()  # fine...
# Om nom nom!

dogs[0].bark()  # fine...
# Woof woof!

dogs[1].eat()  # also fine...
# Om nom nom!

dogs[1].bark()  # oops!
# AttributeError: 'Kangaroo' object has no attribute 'bark'
```

## Covariant

### Rules

`GenType[SubType, ...] <: GenType[SuperType, ...]` for `SubType <: SuperType`

and

`GenType[SubType1, SubType2] <: GenType[SuperType1, SuperType]` for `SubType1 <: SuperType1` *and* `SubType2 <: SuperType2`

### Thus

- immutable containers are usually covariant
- e.g. these are covariant: `Tuple`, `FrozenSet`, `Union[]` types

- callables are covariant in return type
- `Callable[[], SubType] <: Callable[[], SuperType]` for `SubType <: SuperType`


### Examples

- `Tuple[Dog]` could be assigned where `Tuple[Animal]` is needed.
- `Tuple[bool]` is subtype of `Tuple[int]` because bool is subtype of int
- `Mapping[A, B]` will accept `Dict[A, C]` if `C <: B`
- `Union[Animal, Food]` will accept `Union[Dog, Meat]`

- `some_animal: Animal = get_animal()` can be replaced with `some_animal: Animal = get_dog()`

```python
from typing import Tuple

class Animal: ...
class Dog(Animal): ...

an_animal: Animal = Animal()
lassie: Dog = Dog()
snoopy: Dog = Dog()

animals: Tuple[Animal, ...] = (an_animal, lassie)
dogs: Tuple[Dog, ...] = (lassie, snoopy)

dogs = animals  # mypy error:
# Incompatible types in assignment (expression has type
#   "Tuple[Animal, ...]", variable has type "Tuple[Dog, ...]")
```

## Contravariant

### Rules

`GenType[SuperType, ...] <: GenType[SubType, ...]` for `SubType <: SuperType`

`GenType[[SuperType1, SuperType2], ...] <: GenType[[SubType1, SubType2], ...]` for `SubType1 <: SuperType1` *and* `SubType2 <: SuperType2`

Callable is contravariant in argument type.


### Thus

Things accepting a `Callable` can accept something with a more permissive type, but not a more restrictive one


### Examples

- Something taking an argument of `Callable[[Dog], ...]` can accept `Callable[[Animal], ...]`
- But `Callable[[Animal], ...]` can **not** accept `Callable[[Dog], ...]`

```python
class Animal: ...
class Dog(Animal): ...
class Kangaroo(Animal): ...

def animal_run(animal: Animal) -> None:
    # its type is `Callable[[Animal], None]`
    print('An animal is running!')

def dog_run(dog: Dog) -> None:
    # its type is `Callable[[Dog], None]`
    print('A dog is running!')

def make_animal_run(
    an_animal: Animal,
    run_function: Callable[[Animal], None],
) -> None:
    run_function(an_animal)

bob_a_kangaroo: Kangaroo = Kangaroo()

make_animal_run(bob_a_kangaroo, dog_run)  # mypy error:
# Argument 2 to "make_animal_run" has incompatible type
#   "Callable[[Dog], None]"; expected "Callable[[Animal], None]"
```


## NewType

Type-checked type aliases, e.g.:

```python

from typing import NewType

SafeStr = NewType('SafeStr', str)

safe_code = SafeStr('2 + 2')
user_provided_code = 'import sys; sys.melt_cpu()'

def exec_code(string: SafeStr):
    exec(string)

exec_code(safe_code)
exec_code(user_provided_code)  # error:
# Argument 1 to "exec_code" has incompatible type "str"; expected "SafeStr"
```


## TypeVar

Dynamically constrain types, e.g.:

```python
# choose.py

import random
from typing import Sequence, TypeVar

Choosable = TypeVar("Choosable", str, float)

def choose(items: Sequence[Choosable]) -> Choosable:
    return random.choice(items)

reveal_type(choose(["Guido", "Jukka", "Ivan"]))  # builtins.str*
reveal_type(choose([1, 2, 3]))  # builtins.float*
reveal_type(choose([True, 42, 3.14]))  # builtins.float*
reveal_type(choose(["Python", 3, 7]))  # builtins.object*
# error: Value of type variable "Choosable" of "choose" cannot be "object"

bob: str = choose([42, 3.14])
# error: Incompatible types in assignment (expression has type "float", variable has type "str")
```
