import pytest
import importlib
Group17 = importlib.import_module("Onko-MiniProject")
from Group17 import add

def test_add():
    assert add(1, 2) == 3

if __name__ == "__main__":
    pytest.main()
