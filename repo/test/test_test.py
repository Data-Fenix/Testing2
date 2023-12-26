import numpy as np

# this should pass
def test_numpy():
    assert np.array([1, 2, 3]).sum() == 6
    
# this should fail
def test_numpy_2():
    assert np.array([1, 2, 4]).sum() == 7    
    