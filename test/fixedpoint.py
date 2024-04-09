from fxpmath import Fxp
from math import isclose
def test_multiplication():
    DTYPE = "fxp-u16/16"
    # Fxp as operands
    x1 = Fxp(0.5, signed=False, dtype=DTYPE)
    x2 = Fxp(0.7, signed=False, dtype=DTYPE)

    # Define the type of the new variable first
    y = Fxp(None, signed=False, dtype=DTYPE)
    # Set the value of the new variable with equal
    y.equal(x1*x2)

    assert (y.dtype == x1.dtype and y.dtype == x2.dtype)

def test_addition():
    DTYPE = "fxp-u16/16"
    # Fxp as operands
    x1 = Fxp(0.2, signed=False, dtype=DTYPE)
    x2 = Fxp(0.3, signed=False, dtype=DTYPE)
    # Define the type of the new variable first
    y = Fxp(None, signed=False, dtype=DTYPE)
    # Set the value of the new variable with equal
    y.equal(x1 + x2)

    assert (y.dtype == x1.dtype and y.dtype == x2.dtype)
    assert isclose(0.5, y, rel_tol=0.05)
