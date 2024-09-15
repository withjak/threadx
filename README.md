**threadx** 


# Table of Contents
- [Install](#Install)
- [Motivation](#Add-dependency)
- [Usage](#Usage)
    - [Pass result as first argument](#Pass-result-as-first-argument)
    - [Pass x as nth argument](#Pass-x-as-nth-argument)
    - [Unpacking arguments](#Unpacking-arguments)
    - [Rules for First thing](#Rules-for-First-thing)
    - [Method call](#Method-call)
    - [Attribute lookup](#Attribute-lookup)
    - [Key access and slicing](#Key-access-and-slicing)
    - [Debugging](#Debugging)
    - [Fewer lambdas](#Fewer-lambdas)
- [Inner working](#Inner-working)

## Install 
TODO

## Motivation
TODO

## Usage

### Import
```python
from threadx import thread, x, stop
```

### Pass result as first argument
Passed result (i.e. `x`) of last step as first argument.
```python
thread([1, 2, 3],  # => [1, 2, 3]
       sum,        # => 6
       str)        # => '6'

# x represents the result of previous step.
# x is implictly passed as first argument in each step
# identical to above code
thread([1, 2, 3],
       (sum, x),
       (str, x))
```

### Pass x as nth argument
Pass `x` as nth argument <br>
`x` if present it the arguments, then it wont be passed as the first argument implicitly.
```python
thread(10, 
       (range, x, 20, 3),  # same as (range, 20, 3)
       list)               # => [10, 13, 16, 19]

# passed as second argument 
thread(20, 
       (range, 10, x, 3),
       list)               # => [10, 13, 16, 19]

# passed as third argument
thread(3, 
       (range, 10, 20, x),
       list)               # => [10, 13, 16, 19]
```

### Unpacking arguments 
```python 
# unpacking works as usual
thread([10, 20], 
       (range, *x, 3),     # unpack to (range, 10, 20, 3)
       list)               # => [10, 13, 16, 19]
```

### Rules for First thing
- First thing needs to be callable. As can be seen in above examples `sum` `str` `range` `list`.
- You cannot pass `x` as the first thing.

Their voilation will throw `TypeError` and `ValueError` respectively.
<br>

### Method call
- `x` is whatever was returned from evaluation of previous step.
- So naturally you can do all the things with it that you would do with them.

```python
thread(['a', 'b'], 
       (x.index, 'a'))      # => 0
# l = ['a', 'b']
# l.index('b')

thread(['a', 'b'], 
       (x.count, 'b'))      # => 1
```

### Attribute lookup
Lookup class and instance attributes.
```python 
thread({'a': 1, 'b': 2},
       x.keys, 
       list)                # => ['a', 'b']

```

### Key access and slicing
```python
thread({'a': {'b': [1, 2]}}, 
       x['a'], 
       x['b'][0])                   # => 1

thread({'a': {'b': [1, 2, 3, 4]}}, 
       x['a']['b'][:2])             # => [1, 2]

```

### Debugging 
Place `stop` to retun the result of previous step. Usefull for debugging.
```python
thread({'a': {'b': [1, 2]}}, 
       x['a'], 
       x['b'], 
       stop,                    # => [1, 2]
       sum,                     # this wont be executed
       str)                     # this wont either

```

### Fewer lambdas
```python 
data = {'a': {'b': [10, 12]}}

# lambdas
thread([data, data], 
       (map, lambda i: i['a']['b'], x), 
       list)                                # => [[10, 12], [10, 12]]

# See `Inner working` to undestand whats happening
# For now think of it like:
# last `x` is the output from previous step, i.e. [data1, data2]
# `x` in x[...][...] assumes the value of data1 and then data2.
thread([data, data], 
       (map, x['a']['b'], x), 
       list)                                # => [[10, 12], [10, 12]]

```

## Inner working
### x
`x` is Special, I mean literally.
```python
x = _Special()
```
`thread` finds it in arguments list and replaces it with return value from previous step.

### *x
`*x` is a function
```python
(*x, ) == (_unpack_args, )
```
If `thread` function sees it in argument list, it replaces it with, result (unpacked) of previous step.

### x[...]
- `x[...]` retuns a object of class `_KeyChain`. 
- This object remembers the key names that appear in brackets.

```python
data = [['a', 'b'], 'k']

# This happens
_KeyChain()[0][1](data) # => 'b'

# You wite is as
thread(data, 
       x[0][1])

# which is identical to
thread(data, 
       (x[0][1], x))

# or you can write it as
thread(data, 
       _KeyChain()[0][1])

```

### x.thing
`x.thing` works similar to `x[...]`, but instead of being an object, it is just a function with a closure on the name "thing".

```python
data = ['a', 'b']
_capture_attr('index')(data, 'a')  # => 0

thread(data, 
       (x.index, 'a'))

thread(data, 
       (_capture_attr('index'), 'a'))

thread(data, 
       (_capture_attr('index'), x, 'a'))
```






