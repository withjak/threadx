from threadx import thread, x, stop
from functools import reduce
import operator as op

def test_thread_first_argument():
    """passing as first argument to next function"""
    assert '10' == thread([1, 2, 3, 4], 
                          (sum), 
                          (str))
    
    assert '10' == thread([1, 2, 3, 4], 
                          sum, 
                          str)

def test_thread_nth_argument():
    """place `x` at the last position"""
    assert '11' == thread([1, 2, 3, 4],
                          (reduce, op.add, x),
                          (op.add, 1),
                          (str, x))
    
def test_thread_debugging():
    """place `x` to return early."""
    assert 10 == thread([1, 2, 3, 4], 
                         sum,
                         stop,
                         str)
    
    assert [1, 2, 3, 4] == thread([1, 2, 3, 4],
                                  stop,
                                  (reduce, op.add, x),
                                  str)

def test_thread_get_attribute_value():
    assert 4 == thread([1, 2, 3, 4],
                       x.__len__)

def test_thread_call_method():
    assert 3 == thread([1, 2, 3, 2, 2, 4], 
                       (x.count, 2))    
    
def test_thread_unpack_args():
    assert range(10) == thread([0, 10],
                               (range, *x))
