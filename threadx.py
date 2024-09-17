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

def _unpack_args():
    """Used as a symbol for comparision"""
    pass

def stop(): 
    """Used as a symbol for comparision"""
    pass

def _capture_attr(name):
    """Remebers `name`, which is supposed to be a attribute/method name of `obj`.
    Later it
    - returns the attributre value
    - or calls the method
    """
    def call_me(obj, *args):
        thing = getattr(obj, name)
        if callable(thing):
            return thing(*args)     
        else:
            # if args not empty then raise exception / log warning saying syntax error. thing is not callable.
            return thing
    return call_me

class _KeyChain:
    """Usage:
    data = [['a', 'b'], 1]
    
    _KeyChain()[0][1](data) # => 'b'
    """
    def __init__(self):
        self.key_names = []
    
    def __getitem__(self, name):
        "Warning: object is modified once we try to get an item"
        self.key_names.append(name)
        return self
    
    def __call__(self, obj):
        for name in self.key_names:
            obj = obj[name]
        return obj

class _X:
    "I do not say no to anything."
    def __iter__(self):
        return iter([_unpack_args])

    def __getitem__(self, name):
        return _KeyChain()[name]
        
    def __getattribute__(self, name):
        return _capture_attr(name)
    
    def __repr__(self):
        return '_Special()'

x = _X()

def _call_f(f, prev, args):
    """
    Builds up arguments list by subtituting:
    - `unpack_args` with *prev, or
    - `x` with `prev`.

    Calls function `f` with these new arguments.
    """
    try:
        i = args.index(_unpack_args)
    except ValueError:
        pass
    else:
        return f(*args[:i], *prev, *args[i+1:])
          
    try:
        i = args.index(x)
    except ValueError:
        return f(prev, *args)
    else:
        return f(*args[:i], prev, *args[i+1:])    

def thread(data, *pipeline):
    """Does Threading/Chaining of functions. Passes output of one a function to the next function.
    Ex.
    thread(10, 
           (range, 0, x, 2), 
           sum)
    Check tests for all possible options.
    """
    prev = data
    for step in pipeline:
        if not isinstance(step, tuple):
            step = (step, )
            
        f, *rest = step
        if f == stop:
            return prev
        elif f == x:
            raise ValueError(f'x cannot be the first thing.')
        elif f == _unpack_args:
            raise ValueError(f'*x cannot be the first thing.')
        elif callable(f):
            prev = _call_f(f, prev, rest)
        else:
            raise TypeError(f'First thing in tuple needs to be a callable. Got {type(f)}:{f}')
    return prev



