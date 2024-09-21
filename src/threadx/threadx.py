# Copyright 2024 Akshay Patel
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import operator as op

def _unpack_args():
    """Used as a symbol for comparision"""
    pass

def stop(): 
    """Used as a symbol for comparision"""
    pass

def _capture_attr(name):
    def call_me(obj, *args):
        thing = getattr(obj, name)
        if callable(thing):
            return thing(*args)     
        else:
            # if args not empty then raise exception / log warning saying syntax error. thing is not callable.
            return thing
    return call_me

operations_map = {'__add__': op.add,
                  '__sub__': op.sub,
                  '__mul__': op.mul,
                  '__matmul__': op.matmul,
                  '__truediv__': op.truediv,
                  '__floordiv__': op.floordiv,
                  '__mod__': op.mod,
                  '__lshift__': op.lshift,
                  '__rshift__': op.rshift,
                  '__pow__': op.pow,
                  '__and__': op.and_,
                  '__xor__': op.xor,
                  '__or__': op.or_, 
                  '__lt__': op.lt, 
                  '__le__': op.le, 
                  '__eq__': op.eq, 
                  '__ne__': op.ne, 
                  '__gt__': op.gt,
                  '__ge__': op.ge}

class _LazyLookup:
    """Remembers the item names and operations. 
    When called with data, lookup those items in the data and perform any needed operations.

    data = {'a': ["hello", "world"]}

    _LazyLookup()['a'][1](data)              # => "world"
    (_LazyLookup()['a'][1] == "world")(data) # => True
    """
    
    def __init__(self):
        self.key_names = []
        
        self.operations = []
        def binary_operation(op):
            def special_method(self, other):
                self.operations.append((op, other))
                return self
            return special_method
        
        for method_name, operation in operations_map.items(): 
            setattr(self.__class__, method_name, binary_operation(operation))
    
    def __getitem__(self, name):
        "Warning: object is modified once we try to get an item"
        self.key_names.append(name)
        return self
    
    def __call__(self, data_obj):
        obj = data_obj
        for name in self.key_names:
            obj = obj[name]

        for operation, other in self.operations:
            if isinstance(other, self.__class__): 
                other = other(data_obj)     
            obj = operation(obj, other)
        return obj
    
    def __repr__(self):
        return '_LazyLookup()' + str.join('', [f"[{_!r}]" for _ in self.key_names]) + ' ' + str(self.operations) 

class _ShapeShifter:
    """I am `_ShapeShifter` (`x`).
    When you try to:
    1. iterate me (`*x`) i become `_unpack_args`
    2. access a method/attribute (`x.name`) i become `_capture_attr`
    3. do item lookup (`x[name]`) or slicing (`x[:]`) i become _LazyLookup
    4. apply an operator (`x > 1`) i become _LazyLookup

    You can not compare me using `==`, but I allow you to verify my identity using `is`
    """
    def __init__(self):
        def binary_operation(method_name):
            def special_method(self, other):
                return getattr(_LazyLookup(), method_name)(other)
            return special_method
            
        for method_name in operations_map.keys(): 
            setattr(self.__class__, 
                    method_name, 
                    binary_operation(method_name))
    
    def __iter__(self):
        return iter([_unpack_args])

    def __getitem__(self, name):
        return _LazyLookup()[name]
        
    def __getattr__(self, name):
        return _capture_attr(name)
    
    def __repr__(self):
        return '_ShapeShifter()'

x = _ShapeShifter()

def _call_f(f, prev, args):
    """
    Builds up arguments list by subtituting:
    - `unpack_args` with *prev, or
    - `x` with `prev`.

    Calls function `f` with these new arguments.
    """

    # list.index makes comparision using == 
    # this wont work for us as soon as we check for equality x (i.e. _X()) will be converted to _KeyChain().
    # Also not choosing comparing hash as this might be expensive depending on the object.
    # so settling on id which is a contant time operation.
    # also id comparision is much faster compared to == 
    
    x_id = id(x)
    u_id = id(_unpack_args)
    index = None 
    unpack = None

    # doing this loop manually as this previous implementation took 550ns while this implementation takes 300ns
    for i, arg in enumerate(args): 
        arg_id = id(arg)
        if arg_id == x_id: 
            index = i 
            unpack = False
            break
        elif arg_id == u_id: 
            index = i
            unpack = True
            break

    if unpack == True: 
        return f(*args[:index], *prev, *args[index+1:])
    elif unpack == False: 
        return f(*args[:index], prev, *args[index+1:])
    else: # unpack == None
        return f(prev, *args)   

def thread(data, *steps):
    """Threads result of a step to next, i.e. passes output of one a function to the next function.
    Ex.
    thread(10, 
           (range, 0, x, 2), 
           sum)
    Check tests/readme for all possible options.
    """
    prev = data
    for step in steps:
        if not isinstance(step, tuple):
            step = (step, )
        
        f, *rest = step
        if f is stop:
            return prev
        elif f is x:
            raise ValueError(f'x cannot be the first thing.')
        elif f is _unpack_args:
            raise ValueError(f'*x cannot be the first thing.')
        elif callable(f):
            prev = _call_f(f, prev, rest)
        else:
            raise TypeError(f'First thing in tuple needs to be a callable. Got {type(f)}:{f}')
    return prev

