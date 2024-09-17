**threadx** 


# Table of Contents
- [Install](#Install)
- [Motivation](#Add-dependency)
- [Usage](#Usage)
    - [Pass result as first argument](#Pass-result-as-first-argument)
    - [Pass x as nth argument](#Pass-x-as-nth-argument)
    - [Unpacking arguments](#Unpacking-arguments)
    - [Rule for the First thing](#Rule-for-the-First-thing)
    - [Method call](#Method-call)
    - [Attribute lookup](#Attribute-lookup)
    - [Key access and slicing](#Key-access-and-slicing)
    - [Debugging](#Debugging)
    - [Fewer lambdas](#Fewer-lambdas)
- [Inner working](#Inner-working)
- [TODO](#TODO)

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
Pass result (i.e. `x`) of previous step as first argument.
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
`x` if present it the arguments, then it won't be passed as the first argument implicitly.
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

Unpacking works as usual

```python 
thread([10, 20], 
       (range, *x, 3),     # unpack to (range, 10, 20, 3)
       list)               # => [10, 13, 16, 19]
```

### Rule for the First thing
`thread` function:
- signature `thread(data, *pipeline)`
  - pipeline is a sequence of steps
  - each step can be:
       - a tuple like `(function, arg_1, arg_2, ...)`.
       - or, just a `function` in case if it only takes one argument.
  - `thread` calls the function in each step with appropiate arguments (including the result from previous step)

So, the first thing i.e. the function in each step, well it does not need be a function. But it needs to be a `callable`.
- `TypeError` will be thrown if its not a callable.

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
Below code demonstrates how we can get rid of `lambda` in the **simplest case** where there is only one iterable provided to the map function.
```python 
data = {'a': {'b': [10, 12]}}

# lambdas
thread([data, data], 
       (map, lambda i: i['a']['b'][0], x), 
       list)                                # => [10, 10]

thread([data, data], 
       (map, x['a']['b'][0], x), 
       list)                                # => [10, 10]

```
What just happened?
- last `x` is the output from previous step, i.e. [data1, data2]
- "x" in `x[...][...]` assumes the value of data1 and then data2.
See `Inner working` to undestand whats happening

## Inner working
### x
`thread` sees `x` in arguments list and replaces it with return value from previous step. 
```python
x = _X()
```

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

## TODO
- Complete readme.
- Few exmaple showing best written python code and then comparing it with threadx implementation, for:
 - redability
 - performance impact
- Benchmarking code for performance both time and memory (if possible).
- Publish it on pypi
