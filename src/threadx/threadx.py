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
                  '__ge__': op.ge, 
                  # the other way around 
                  '__radd__': lambda a, b: b + a,
                  '__rsub__': lambda a, b: b - a, 
                  '__rmul__': lambda a, b: b * a,
                  '__rmatmul__': lambda a, b: b @ a,
                  '__rtruediv__': lambda a, b: b / a,
                  '__rfloordiv__': lambda a, b: b // a,
                  '__rmod__': lambda a, b: b % a,
                  '__rlshift__': lambda a, b: b << a,
                  '__rrshift__': lambda a, b: a >> b,
                  '__rpow__': lambda a, b: b ** a,
                  '__rand__': lambda a, b: b & a,
                  '__rxor__': lambda a, b: b ^ a,
                  '__ror__': lambda a, b: b | a}

symbols_map = {op.add: '+',
               op.sub: '-',
               op.mul: '*',
               op.matmul: '@',
               op.truediv: '/',
               op.floordiv: '//',
               op.mod: '%',
               op.lshift: '>>',
               op.rshift: '<<',
               op.pow: '**',
               op.and_: '&',
               op.xor: '^',
               op.or_: '|',
               op.lt: '<',
               op.le: '<=',
               op.eq: '==',
               op.ne: '!=',
               op.gt: '>',
               op.ge: '>='}

class _LazyLookup:
    """Remembers the item/attribute names and operations. 
    When called with data, lookup those items and attributes in the data and perform any needed operations.

    data = {'a': ["hello", "world"]}

    _LazyLookup()['a'][1](data)              # => "world"
    (_LazyLookup()['a'][1] == "world")(data) # => True
    """
    
    def __init__(self):
        self._call = False
        self.args = None
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
        self.key_names.append(('getitem', name))
        return self

    def __getattr__(self, name):
        "Warning: object is modified once we try to get an attr"
        self.key_names.append(('getattr', name))
        return self

    def _get_item_and_attr(self, data_obj):
        obj = data_obj
        for typ, name in self.key_names:
            if typ == 'getitem':
                obj = obj[name]
            elif typ == 'getattr': 
                obj = getattr(obj, name)
        return obj
    
    def __call__(self, *data_obj_or_args, call=False):
        if (self._call == True) or (call == True):
            data_obj = data_obj_or_args[0]
            
            obj = self._get_item_and_attr(data_obj) 

            if callable(obj) and (self.args is not None):
                args = [arg(data_obj, call=True) if isinstance(arg, self.__class__) else arg
                        for arg in self.args]
                obj = obj(*args) 

            for operation, other in self.operations:
                if isinstance(other, self.__class__): 
                    other = other(data_obj, call=True)     
                obj = operation(obj, other)
            return obj
        
        else:   
            self.args = data_obj_or_args
            return self

    @staticmethod
    def _lookup_str(typ, name):
        return f"[{name}]" if typ == 'getitem' else f".{name}" 

    @staticmethod 
    def _operations_str(op, other): 
        symbol = symbols_map.get(op, op)
        return f" {symbol} {other}"
        
    def __repr__(self):
        lookup = [self._lookup_str(typ, name) for typ, name in self.key_names]
        operations = [self._operations_str(op, other) for op, other in self.operations]
        
        return '_LazyLookup()' + str.join('', lookup) + str.join('', operations) 
 
class _ShapeShifter:
    """I am `_ShapeShifter` (`x`).
    When you try to:
    1. iterate me (`*x`) i become `_unpack_args`
    2. access a method/attribute (`x.name`) i become `_LazyLookup`
    3. do item lookup (`x[name]`) or slicing (`x[:]`) i `become _LazyLookup`
    4. apply an operator (`x > 1`) i become `_LazyLookup`

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
        return getattr(_LazyLookup(), name)
    
    def __repr__(self):
        return '_ShapeShifter()'

x = _ShapeShifter()

def _call_f(f, prev, args, default_first=True):
    """
    Builds up arguments list by subtituting:
    - `unpack_args` with *prev, or
    - `x` with `prev`.

    Calls function `f` with these new arguments.
    """
    if isinstance(f, _LazyLookup):
        f._call = True
        return f(prev)

    else:
        for arg in args: 
            if isinstance(arg, _LazyLookup):
                arg._call = True
            
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
        elif default_first == True: # unpack == None
            return f(prev, *args) 
        else: 
            return f(*args, prev)

def xf(data, *steps, default_first=True):
    """Threads result of a step to next, i.e. passes output of one a function to the next function.
    Ex.
    xf(10, 
       (range, 0, x, 2), 
       sum)
    Check tests/readme for all possible options.
    """
    prev = data
    for step in steps:
        if not isinstance(step, tuple):
            step = (step, )
        
        f, *rest = step
        if f is x:
            raise ValueError(f'x cannot be the first thing.')
        elif f is _unpack_args:
            raise ValueError(f'*x cannot be the first thing.')
        elif callable(f):
            prev = _call_f(f, prev, rest, default_first)
        else:
            raise TypeError(f'First thing in tuple needs to be a callable. Got {type(f)}:{f}')
    return prev

def xl(data, *steps):
    return xf(data, *steps, default_first=False)
