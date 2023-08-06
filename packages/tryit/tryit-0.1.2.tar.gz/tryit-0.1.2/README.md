# Tryit

## Description

Just a decorator to handle exceptions. It maps Python Exceptions to specific callbacks.


## Usage
```python
from tryit import tryit, ExceptionTarget

@tryit(exceptions=[
  ExceptionTarget(ZeroDivisionError, callback=lambda err: float("nan"))
])
def divide(a: int, b: int) -> float:
  return a/b



```