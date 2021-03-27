---
id: Coding-Standards
title: Coding Standards
---
These are some of the standards we choose to follow in this project. These might change if we agree on standards for python development within the community.

### Docstrings

We follow the Comments and Docstrings guidelines from [this style guide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).

### Type Hints

We use [type hints (PEP 484)](https://www.python.org/dev/peps/pep-0484/) which came with Python 3.5 to ease development experience and understand the function's signature better. For reference, this started with [PR #354](https://github.com/anitab-org/mentorship-backend/pull/354).

### String interpolation

We use f-strings as referred in [PEP 498 -- Literal String Interpolation](https://www.python.org/dev/peps/pep-0498/).

Example:
```python
my_name = "Jane Doe"
greetings = f"My name is {my_name}!"
```

### HTTP Status codes

Instead of using HTTP status codes hardcoded in literal format, we use [HTTPStatus module](https://docs.python.org/3/library/http.html) codes.

Example:
```python
from http import HTTPStatus

def ok_status_code:
    return HTTPStatus.OK #200
```
