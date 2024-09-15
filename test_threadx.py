from threadx import thread, x, stop
from functools import reduce
import operator as op
import pytest

"""
Test cases
- implicity passed as first argument
- explicity pass as nth argument
- spread using *
- first thing is required to be a callable
    - a function
    - a method
    - a class
    - a callable class object
- x cannot be the first thing
- method call 
- attribute access 
- key lookup and chained key lookup 
- usage with higher order functions like map
- usage in lambda function
- stop and return early
"""

def return_args(*args):
    return args

def test_thread_implicit_first_argument():
    """Previous result is passed as first argument by default"""
    assert (1, ) == thread(1, 
                           (return_args))
    
    assert (1, ) == thread(1, 
                           return_args)
    
def test_thread_explicit_first_argument():
    """x represents the results from previous step."""
    assert (1, ) == thread(1,
                          (return_args, x))

def test_thread_pass_x_as_nth_argument():
    """place `x` as argument at different position"""
    assert ('here', 1, 2, 4) == thread('here',
                                       (return_args, x, 1, 2, 4))
    
    assert (1, 'here', 2, 4) == thread('here',
                                       (return_args, 1, x, 2, 4))
    
    assert (1, 2, 'here', 4) == thread('here',
                                       (return_args, 1, 2, x, 4))
    
    assert (1, 2, 4, 'here') == thread('here',
                                       (return_args, 1, 2, 4, x))

def test_thread_unpack():
    assert (1, 2, 3, 4, 5) == thread([2, 3], 
                                     (return_args, 1, *x, 4, 5))
    
    assert range(10) == thread([0, 10],
                               (range, *x))

def test_thread_first_thing_should_be_callable():
    with pytest.raises(TypeError, match="First thing in tuple needs to be a callable. Got <class 'str'>:i_am_not_callable"):
        thread(1, 
               'i_am_not_callable')
    
    with pytest.raises(TypeError, match="First thing in tuple needs to be a callable. Got <class 'str'>:i_am_not_callable"):
        thread(1, 
               ('i_am_not_callable', ))
        
def test_thread_first_thing_cannot_be_x():
    with pytest.raises(ValueError, match="x cannot be the first thing."):
        thread(1, 
               x)
    
    with pytest.raises(ValueError, match="x cannot be the first thing."):
        thread(1, 
               (x, ))

class Foo:
    class_attribute = 'class_attribute'

    def __init__(self, a):
        self.instance_attribute = a

    def return_args(self, *args):
        return args

def test_thread_method_call():
    assert (1, 2, 3, 4) == thread(Foo('o'), 
                                  (x.return_args, 1, 2, 3, 4))
    
    assert 4 == thread([1, 2, 3, 4],
                       x.__len__)
    
    assert 3 == thread([1, 2, 3, 4],
                       (x.index, 4))

def test_thread_attribute_access():
    assert 'o' == thread(Foo('o'),
                         x.instance_attribute)
    
    assert 'class_attribute' == thread(Foo('o'), 
                                       x.class_attribute)

def test_thread_key_lookup():
    data = {'a': {'b': [10, 12]}}
    assert {'b': [10, 12]} == thread(data, 
                                     x['a'])
    
    assert [10, 12] == thread(data, 
                               x['a']['b'])
    
    assert 10 == thread(data, 
                        x['a']['b'][0])

def test_thread_higher_order_functions():
    data = {'a': {'b': [10, 12]}}
    assert [{'b': [10, 12]}, {'b': [10, 12]}] == thread([data, data],
                                                        (map, x['a'], x), 
                                                        list)
    
    assert [[10, 12], [10, 12]] == thread([data, data],
                                          (map, x['a']['b'], x), 
                                          list)
    
    assert [12, 12] == thread([data, data],
                              (map, x['a']['b'][1], x), 
                              list)

def test_thread_lambda():
    data = {'a': {'b': [10, 12]}}
    assert [10, 10] == thread([data, data],
                              (map, lambda i: i['a']['b'][0], x),
                              list)
    
    assert [10, 10] == thread([data, data],
                              (map, lambda i: i['a']['b'][0], x),
                              list)
    
def test_thread_stop_and_return():
    """place `stop` to return early."""
    assert 10 == thread([1, 2, 3, 4], 
                         sum,
                         stop,
                         str)
    
    assert [1, 2, 3, 4] == thread([1, 2, 3, 4],
                                  stop,
                                  str)

