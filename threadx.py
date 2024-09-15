def unpack_args():
    pass

def stop(): 
    pass

# Not implementing unpack_kwargs i.e (..., **x, ...) because, 
# In a tuple (1, **{'a', 1}) is an invalid syntax.
# its valid syntax only in a function call. print("something", **{'end': '\n\n'})
# also you cant do somefn("something", **{'end': "abc"}, "hello"), as positional arguments cannot come after keyword arguments

# Instead something like below can be implemented
# (..., *_x, ...) but then you have 2 different symbols: x and _x. Which i dont want to do

def capture_attr(name):
    def call_me(obj, *args):
        thing = getattr(obj, name)
        if callable(thing):
            return thing(*args)     
        else:
            # if args not empty then raise exception / log warning saying syntax error. thing is not callable.
            return thing
    return call_me

def capture_key(name):
    def call_me(obj, *args):
        return obj[name]
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
            raise Exception(f'x cannot be the first thing in the tuple. Got {t!r}')
        elif callable(f):
            prev = handle_f(f, prev, rest)
        else:
            raise Exception(f'First thing in tuple needs to be a callable. Got {type(f)}:{f}')
    return prev
