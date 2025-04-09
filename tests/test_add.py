import sys
import pytest
from .src.add import add

def test_addition(self):
    assert add(1, 2) == 3

if __name__ == "__main__":
    pytest.main([__file__])
