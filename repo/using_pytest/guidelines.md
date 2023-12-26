# Pytest documentation
https://docs.pytest.org/en/7.4.x/index.html

## Anatomy of a test
https://docs.pytest.org/en/7.4.x/explanation/anatomy.html#test-anatomy
**Arrange - Act - Assert - Cleanup**
`Arrange` is where we prepare everything for our test. This means pretty much everything except for `act`. It’s lining up the dominoes so that the act can do its thing in one, state-changing step. This can mean preparing objects, starting/killing services, entering records into a database, or even things like defining a URL to query, generating some credentials for a user that doesn’t exist yet, or just waiting for some process to finish.


`Act` is the singular, state-changing action that kicks off the behavior we want to test. This behavior is what carries out the changing of the state of the system under test (SUT), and it’s the resulting changed state that we can look at to make a judgement about the behavior. This typically takes the form of a function/method call.


`Assert` is where we look at that resulting state and check if it looks how we’d expect after the dust has settled. It’s where we gather evidence to say the behavior does or does not aligns with what we expect. The assert in our test is where we take that measurement/observation and apply our judgement to it. If something should be green, we’d say assert thing == "green".

`Cleanup` is where the test picks up after itself, so other tests aren’t being accidentally influenced by it.


## Basic pytest
Asserting with the assert statement
pytest allows you to use the standard Python assert for verifying expectations and values in Python tests. For example, you can write the following:
```python
# content of test_assert1.py
def f():
    return 3


def test_function():
    assert f() == 4
```
to assert that your function returns a certain value. If this assertion fails you will see the return value of the function call:
```python
$ pytest test_assert1.py
=========================== test session starts ============================
platform linux -- Python 3.x.y, pytest-7.x.y, pluggy-1.x.y
rootdir: /home/sweet/project
collected 1 item

test_assert1.py F                                                    [100%]

================================= FAILURES =================================
______________________________ test_function _______________________________

    def test_function():
>       assert f() == 4
E       assert 3 == 4
E        +  where 3 = f()

test_assert1.py:6: AssertionError
========================= short test summary info ==========================
FAILED test_assert1.py::test_function - assert 3 == 4
============================ 1 failed in 0.12s =============================
```
- https://www.youtube.com/watch?v=YbpKMIUjvK8

## Fixtures

In testing, a fixture provides a **defined, reliable and consistent context** for the tests. \
This could include: 
 - environment (for example a database configured with known parameters) 
 - or content (such as a dataset).

Fixtures define the steps and data that constitute the *arrange phase* of a test. \
In pytest, they are functions you define that serve this purpose. 

They can also be used to define a test’s **act phase**; this is a powerful technique for designing more complex tests. \

The services, state, or other operating environments set up by fixtures are accessed by test functions through arguments. 

*For each fixture used by a test function there is typically a parameter (named after the fixture) in the test function’s definition.*

We can tell pytest that a particular function is a fixture by decorating it with `@pytest.fixture`. Here’s a simple example of what a fixture in pytest might look like:

```python
import pytest


class Fruit:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name


@pytest.fixture
def my_fruit():
    return Fruit("apple")


@pytest.fixture
def fruit_basket(my_fruit):
    return [Fruit("banana"), my_fruit]


def test_my_fruit_in_basket(my_fruit, fruit_basket):
    assert my_fruit in fruit_basket
```

- https://docs.pytest.org/en/7.4.x/explanation/fixtures.html#about-fixtures
- https://www.youtube.com/watch?v=ScEQRKwUePI


### Fixture scopes
Fixtures are created when first requested by a test, and are destroyed based on their scope:
- `function`: the default scope, the fixture is destroyed at the end of the test.
- `class`: the fixture is destroyed during teardown of the last test in the class.
- `module`: the fixture is destroyed during teardown of the last test in the module.
- `package`: the fixture is destroyed during teardown of the last test in the package.
- `session`: the fixture is destroyed at the end of the test session.

