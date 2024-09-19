from threadx import thread, x, stop
import timeit
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
    
def test_thread_stop_and_return():
    """place `stop` to return early."""
    assert 10 == thread([1, 2, 3, 4], 
                         sum,
                         stop,
                         str)
    
    assert [1, 2, 3, 4] == thread([1, 2, 3, 4],
                                  stop,
                                  str)

"""Insane tests
operations on x 
operation on x.thing
operations on x[]
"""

def test_thread_insane_ops_on_x():
    a = 3
    b = 2
    assert a + b == (x + b)(a)
    assert a - b  == (x - b)(a)
    assert a * b == (x * b)(a)
    # assert a @ b == (x @ b)(a)
    assert a / b == (x / b)(a)
    assert a // b == (x // b)(a)
    assert a % b == (x % b)(a)
    assert a ** b == (x ** b)(a)
    assert a >> b == (x >> b)(a)
    assert a << b == (x << b)(a)
    assert a & b == (x & b)(a)
    assert a ^ b == (x ^ b)(a)
    assert a | b == (x | b)(a)
    assert (a < b) == (x < b)(a)
    assert (a <= b) == (x <= b)(a)
    assert (a == b) == (x == b)(a)
    assert (a != b) == (x != b)(a)
    assert (a > b) == (x > b)(a)
    assert (a >= b) == (x >= b)(a)

def test_thread_insane_ops_on_x_item():
    a = [3, 2]
    assert a[0] + a[1] == (x[0] + x[1])(a)
    assert a[0] - a[1]  == (x[0] - x[1])(a)
    assert a[0] * a[1] == (x[0] * x[1])(a)
    # assert a[0] @ a[1] == (x[0] @ x[1])(a)
    assert a[0] / a[1] == (x[0] / x[1])(a)
    assert a[0] // a[1] == (x[0] // x[1])(a)
    assert a[0] % a[1] == (x[0] % x[1])(a)
    assert a[0] ** a[1] == (x[0] ** x[1])(a)
    assert a[0] >> a[1] == (x[0] >> x[1])(a)
    assert a[0] << a[1] == (x[0] << x[1])(a)
    assert a[0] & a[1] == (x[0] & x[1])(a)
    assert a[0] ^ a[1] == (x[0] ^ x[1])(a)
    assert a[0] | a[1] == (x[0] | x[1])(a)
    assert (a[0] < a[1]) == (x[0] < x[1])(a)
    assert (a[0] <= a[1]) == (x[0] <= x[1])(a)
    assert (a[0] == a[1]) == (x[0] == x[1])(a)
    assert (a[0] != a[1]) == (x[0] != x[1])(a)
    assert (a[0] > a[1]) == (x[0] > x[1])(a)
    assert (a[0] >= a[1]) == (x[0] >= x[1])(a)



def test_thread_insane_ops_on_x_getitem():
    assert 1 == thread([1], 
                       x[0] == 1)
    
    assert False == thread(1, 
                       x == 2)
    
    assert True == thread(1, 
                       x == 1)
    
    assert 16 == thread({'a': [0, 1, 2, 3, 4]}, 
                       x['a'][1] + x['a'][2] + x['a'][3] + 10)

def test_thread_insane_time_with_x():
    # pipeline contains 100 fn calls. With x placed in worst position i.e. last position
    # pipeline is rerun 1000 time
    # so runtime overhead is between 0.08 / (100 * 1000) i.e.  between 600 to 800 nanoseconds 
    # practically speaking using this in a very large system wont even account for 1 second delay
    assert (0.08 > 
            timeit.timeit('thread(1, *pipeline)', 
                              setup="pipeline = [(return_args, 1, 2, 3, x) for _ in range(100)]", 
                              globals=globals(), 
                              number=1000)
            > 0.06)

def test_thread_insane_time_with_unpack_x():
    # takes little more time, probably due to unking and not due to thread fn itself.
    # also we are unpacking 1, 1 + 4, 1 + 4*2, ..., 1 + 4*100 args. which would be at best rare in real world.
    # anyway its still only 0.1 sec for 100k calls. per call its like 0.1/100k
    assert (0.2 > 
            timeit.timeit('thread([1], *pipeline)', 
                           setup="pipeline = [(return_args, 1, 2, 3, *x) for _ in range(100)]", 
                           globals=globals(), 
                           number=1000)
            > 0.1)


def get_data(): 
    data = {'a': 'you finally found me'}
    for _ in range(100):
        data = {'a': [data]}
    return data

def get_pipeline():
    return [x['a'][0] for _ in range(100)]

def test_thread_insane_time_with_item_lookup():    
    
    assert {'a': 'you finally found me'} == thread(get_data(), *get_pipeline())

    assert (0.08 > 
            timeit.timeit('thread(data, *pipeline)', 
                          setup = "data = get_data(); pipeline = get_pipeline()",
                          globals=globals(), 
                          number= 1000)
            > 0.07)

def get_data_2():
    data = [1, 2]
    for _ in range(2): 
        data = [data, data]
    return data

def get_pipeline_2():
    return [x[0] + x[1] for _ in range(2)]

def get_pipeline_3():
    return [(lambda i: i[0] + i[1]) for _ in range(2)]

def test_thread_insane_time_with_op():

     assert [1, 2, 1, 2] == thread(get_data_2(), *get_pipeline_2())

     assert (0.003 > 
            timeit.timeit('thread(data, *pipeline)', 
                          setup = "data = get_data_2(); pipeline = get_pipeline_2()",
                          globals=globals(), 
                          number= 1000)
            > 0.001)
     
     assert (0.003 > 
            timeit.timeit('thread(data, *pipeline)', 
                          setup = "data = get_data_2(); pipeline = get_pipeline_3()",
                          globals=globals(), 
                          number= 1000)
            > 0.001)
