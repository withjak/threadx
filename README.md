**threadx** - Create elegant data transformation pipelines.
It brings the elegance of Clojure's threading macros to Python. 
It lets you thread values through a sequence of operations with a sense of clarity and simplicity that feels natural. And it all revolves around two key elements:
- **thread**: Passes the result of each step as the input to the next.
- **x**: A smart placeholder that knows exactly where to inject the previous result, whether in a method call, item lookup, or even unpacking.

Here’s what it looks like in action:
```python
from threadx import thread, x

thread('./data.log', 
       read_file, 
       x.splitlines, 
       (map, x.strip, x), 
       (map, json.loads, x), 
       (map, x['time'], x), 
       sum)
```

What’s happening here? The file content is being read, split, stripped, converted to JSON, and the execution-time summed—all in a linear and readable way. No intermediary variables, no nesting, just the data flowing from one step to the next. <br>


*data.log* might look like:
```json
{"time": 12000, "fn": "foo", ...}
{"time": 12345, "fn": "bar", ...}
```

What Makes threadx Interesting?
- **Readable Flow**: Instead of diving into layers of nested calls, you write each transformation as a clear, sequential step. 
- **The `x` Factor**: `x` acts as a placeholder for where the output of the previous step goes. It’s surprisingly flexible, supporting method calls, attribute/item lookups, and more.
- **No Extra Variables**: Avoid the noise of intermediate variables or lambda functions. Your transformations stay clean and minimal.

# Table of Contents
- [Install](#Install)
- [Usage](#Usage)
    - [Pass result as first argument](#Pass-result-as-first-argument)
    - [Pass x as nth argument](#Pass-x-as-nth-argument)
    - [Unpacking arguments](#Unpacking-arguments)
    - [Rule for the First thing](#Rule-for-the-First-thing)
    - [Method call](#Method-call)
    - [Attribute lookup](#Attribute-lookup)
    - [Getting Item And Slicing](#Getting-Item-And-Slicing)
    - [Debugging](#Debugging)
    - [Fewer lambdas](#Fewer-lambdas)
    - [Build data transformation pipeline](#Build-data-transformation-pipeline)
- [TODO](#TODO)

## Install 
TODO

## Usage

### Import
```python
from threadx import thread, x, stop
```

### Pass result as first argument
`thread` allows you to pass the result of the previous step automatically as the first argument in each new function:
```python
thread([1, 2, 3],  # => [1, 2, 3]
       sum,        # => 6
       str)        # => '6'
```

Or, be explicit about it:
```python
thread([1, 2, 3],
       (sum, x),
       (str, x))
```

### Pass x as nth argument
Want to pass the result into a different argument position? No problem:
```python
thread(10, 
       (range, x, 20, 3),  # same as (range, 20, 3)
       list)               # => [10, 13, 16, 19]

thread(20, 
       (range, 10, x, 3),
       list)               # => [10, 13, 16, 19]

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

### Method call
Use `x.method_name` for method calls, just like magic.
```python
thread(['a', 'b'], 
       (x.index, 'a'))      # => 0

thread(['a', 'b'], 
       (x.count, 'b'))      # => 1
```

### Attribute lookup
Use `x.attribute_name` to lookup class and instance attributes. 
```python 
thread({'a': 1, 'b': 2},
       x.keys, 
       list)                # => ['a', 'b']

```

### Getting Item And Slicing
```python
data = {'a': {'b': [1, 2, 3, 4]}}

thread(data, 
       x['a'], 
       x['b'][0])                   # => 1

thread(data, 
       x['a']['b'][:2])             # => [1, 2]

```

### Debugging 
Easily inspect intermediate results using `stop`. Usefull for debugging.
```python
thread(data, 
       x['a'], 
       x['b'], 
       stop,                    # => [1, 2, 3, 4], Stop and return for inspection
       sum,                     # This won’t be executed
       str)

```

### Fewer lambdas
Remove verbose lambdas in the **simple case** where there is only one iterable provided to the `map`/`filter`/`reduce` or any other similar function.
```python 
# Normal way:
thread([data, data], 
       (map, lambda i: i['a']['b'][0], x), 
       list)                                # => [10, 10]

# threadx way:
thread([data, data], 
       (map, x['a']['b'][0], x), 
       list)                                # => [10, 10]

```
What just happened?
- Last `x` is the output from previous step.
- "x" in `x[...][...]` assumes the value of data1 and then data2 as map supplies them one by one.

### Build data transformation pipeline
```python
# make a tuple or list
pipeline = (read_file, 
            x.splitlines, 
            (map, x.strip, x), 
            (map, json.loads, x), 
            (map, x['time'], x), 
            sum)

thread('./data.log', *pipeline)  # works jsut as any other function.
```

## Why I Built This
After spending a few years working with Clojure, I found myself missing its threading macros when I returned to Python (for a side project). Sure, Python has some tools for chaining operations, but nothing quite as elegant or powerful as what I was used to.

## TODO
- Benchmarking code for performance both time and memory (if possible).
- Publish it on pypi
