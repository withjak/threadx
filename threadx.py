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

def unpack_args():
    pass

def stop(): 
    pass

def capture_attr(name):
    def call_me(obj, *args):
        thing = getattr(obj, name)
        if callable(thing):
            return thing(*args)     
        else:
            # if args not empty then raise exception / log warning saying syntax error. thing is not callable.
            return thing
    return call_me

class Key_chain:
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

class Special:
    "I do not say no to anything."
    def __iter__(self):
        return iter([unpack_args])

    def __getitem__(self, name):
        return Key_chain()[name]
        
    def __getattribute__(self, name):
        return capture_attr(name)
    
    def __repr__(self):
        return 'Special()'

x = Special()

def handle_f(f, prev, args):
    try:
        i = args.index(unpack_args)
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

def thread(prev, *tuples):
    for t in tuples:
        if not isinstance(t, tuple):
            t = (t, )
            
        f, *rest = t
        if f == stop:
            return prev
        elif f == x:
            raise ValueError(f'x cannot be the first thing.')
        elif callable(f):
            prev = handle_f(f, prev, rest)
        else:
            raise TypeError(f'First thing in tuple needs to be a callable. Got {type(f)}:{f}')
    return prev
