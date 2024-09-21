from threadx import thread, x, stop
import timeit
import pytest

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

def test_thread_nth_argument():
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

def test_x_binary_operations():
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

def test_x_binary_operations_and_item_lookup():
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


def test_thread_operations():
    assert 1 == thread([1], 
                       x[0] == 1)
    
    assert False == thread(1, 
                       x == 2)
    
    assert True == thread(1, 
                       x == 1)
    
    assert 16 == thread({'a': [0, 1, 2, 3, 4]}, 
                       x['a'][1] + x['a'][2] + x['a'][3] + 10)

    
def return_one(*args):
    return 1 

def test_thread_insane_time_with_x():
    calls_per_run = 100    
    total_runs = 1000

    # preparing best possible python code
    code = 'f = lambda i: '
    for _ in range(calls_per_run): 
        code += 'return_one(1, 2, 3, '
    code += 'i' + ')'*calls_per_run

    normal = timeit.timeit('f(1)',
                           setup=code,
                           globals=globals(), 
                           number=total_runs)
    
    # pipeline contains 100 fn calls. With x placed in worst position i.e. last position
    # pipeline is rerun 1000 time
    # so runtime overhead is between 0.08 / (100 * 1000) i.e.  between 600 to 800 nanoseconds 
    # practically speaking using this in a very large system wont even account for 1 second delay
    threadx = timeit.timeit('thread(1, *pipeline)', 
                            setup=f"pipeline = [(return_one, 1, 2, 3, x) for _ in range({calls_per_run})]", 
                            globals=globals(), 
                            number=total_runs)
    
    # 1 second overhead you can make 1/6e-7 => 1,666,667 function calls.
    assert 6e-7 > (threadx - normal) / (calls_per_run * total_runs)


def return_four(*args): 
    return args[:4]

def test_thread_insane_time_with_unpack_x():
    calls_per_run = 100    
    total_runs = 1000

    # preparing best possible python code
    code = 'f = lambda i: '
    for _ in range(calls_per_run): 
        code += 'return_four(1, 2, 3, *'
    code += 'i' + ')'*calls_per_run

    normal = timeit.timeit('f([1])',
                           setup=code,
                           globals=globals(), 
                           number=total_runs)
    
    threadx = timeit.timeit('thread([1], *pipeline)', 
                           setup=f"pipeline = [(return_four, 1, 2, 3, *x) for _ in range({calls_per_run})]", 
                           globals=globals(), 
                           number=total_runs)
    
    # 1 second overhead you can make 1/6e-7 => 1,666,667 function calls.
    assert 6e-7 > (threadx - normal) / (calls_per_run * total_runs)


def get_data(calls_per_run): 
    data = {'a': 'you finally found me'}
    for _ in range(100):
        data = {'a': [data]}
    return data

def get_pipeline(calls_per_run):
    return [x['a'][0] for _ in range(100)]

def test_thread_insane_time_with_item_lookup(): 
    calls_per_run = 100    
    total_runs = 1000

    code = 'lambda i: i'
    for _ in range(calls_per_run): 
        code += "['a'][0]"
    
    assert {'a': 'you finally found me'}  == eval(code)(get_data(calls_per_run))
    normal = timeit.timeit('f(data)', 
                          setup = f"f = {code}; data = get_data({calls_per_run})",
                          globals=globals(), 
                          number= total_runs)
    
    assert {'a': 'you finally found me'} == thread(get_data(calls_per_run), *get_pipeline(calls_per_run))
    threadx = timeit.timeit('thread(data, *pipeline)', 
                          setup = f"data = get_data({calls_per_run}); pipeline = get_pipeline({calls_per_run})",
                          globals=globals(), 
                          number= total_runs)
    
    assert 5e-7 > (threadx - normal) / (calls_per_run * total_runs)


def get_data_2(n):
    data = [1, 2]
    for _ in range(n): 
        data = [data, data]
    return data

def get_pipeline_2(n):
    return [x[0] + x[1] for _ in range(n)]

def get_pipeline_3():
    return [(lambda i: i[0] + i[1]) for _ in range(2)] 

def extract(d):
    return d[0] + d[1]

def test_thread_insane_time_with_op():
    calls_per_run = 100    
    total_runs = 1000

    code = "lambda i: "
    for _ in range(calls_per_run):
        code += 'extract('
    code += 'i' + ')'*calls_per_run

    assert [1, 2, 1, 2] == eval(code)(get_data_2(calls_per_run))
    assert [1, 2, 1, 2] == thread(get_data_2(calls_per_run), 
                                  *get_pipeline_2(calls_per_run))
    
    normal = timeit.timeit('f(data)', 
                          setup = f"f = {code}; data = get_data_2({calls_per_run})",
                          globals=globals(), 
                          number= total_runs)
    
    threadx = timeit.timeit('thread(data, *pipeline)', 
                          setup = f"data = get_data_2({calls_per_run}); pipeline = get_pipeline_2({calls_per_run})",
                          globals=globals(), 
                          number= total_runs)
    
    assert 7e-7 > (threadx - normal) / (calls_per_run * total_runs)
     
