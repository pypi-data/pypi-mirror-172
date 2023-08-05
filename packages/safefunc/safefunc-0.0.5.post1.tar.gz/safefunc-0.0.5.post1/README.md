safefunc
========

**Important**
> You may want to use the newer library
> [fnsafe](https://pypi.org/project/fnsafe/).

Make sudden erros not stop your program


Installation
------------

`pip install safefunc`

```python
from safefunc import makesafe
```


Basic Example
-------------

```python
@makesafe()
def divide(a, b):
    return a / b

print("Let's calculate!")
result = divide(1, 0)
print(f"{result = }")
```

Output:

```
Let's calculate!
Ignoring exception in divide
Traceback (most recent call last):
  File "<string>", line 40, in safe
  File "<string>", line 75, in divide
ZeroDivisionError: division by zero
result = None
```

As you can see, the exception gets printed but
the program continues.


More Examples
-------------

Let's try the same thing with `divide(1, 1)`:

Output:

```
Let's calculate!
result = 1
```

Now everything worked fine.

Some functions may return `None`. If an error
happens, it would also return `None`. Luckily
we can differate between success and failure
with the `return_entire_result` paramter:

```python
@makesafe(return_entire_result = True)
def divide(a, b):
    return a / b

print("Let's calculate!")
result = divide(1, 0)
if result: # or result.success
    print(result()) # or result.result
```

In this case our function returns a `Result`
object which allows us to check wether the
function succeeded or not. The `result`
attribute (which also can be accessed by
calling the object) returns depending on the
success, the function return value or the
exception.

Let's expect, we call `divide("1", 1)`. Because
the first argument is not supported for
division, it would raise an error. If we only want
to ignore `ZeroDivisionError`s, we can make use of
the `ignore` parameter. You can interpret this as
a whitelist:

```python
@makesafe(return_entire_result = True, ignore = [ZeroDivisionError])
def divide(a, b):
    return a / b

print("Let's calculate!")
result = divide("1", 1)
if result:
    print(result())
```

This will raise any error that occures except
`ZeroDivisionError`.

We can also reverse the situation and ignore
any exception except `ZeroDivisionError` by
setting the `raise_when` parameter. You can
understand this as a blacklist:

```python
@makesafe(return_entire_result = True, raise_when = [ZeroDivisionError])
def divide(a, b):
    return a / b

print("Let's calculate!")
result = divide("1", 1)
if result:
    print(result())
```

<b>Keep in mind that you can not set both
`ignore` and `raise_when`. If you do
so, a TypeError gets raised.</b>


Other Parameters
----------------

quiet

> refrains displaying the exception

> type: bool

> default: False

title

> text that gets displayed above the exception

> type: str

> default: "Ignoring exception in {function.\_\_name\_\_}"

colored

> displays the exception in a darker color;
> may not work on every device / console;
> should not be used when using a file for the output

> type: bool

> default: False

file

> a file or file-like object where the ouput gets written to

> type: typing.TextIO

> default: sys.stderr


*[inspired by discord.py](https://github.com/Rapptz/discord.py/blob/master/discord/client.py#L405-L415)*


Tips
----

In case you want to just *run* a function safely
instead of directly *making* it safe, you can
include this function:

```python
from safefunc import makesafe

def runsafe(function, *args, **kwargs):
    return makesafe(*args, **kwargs)(function)
```
