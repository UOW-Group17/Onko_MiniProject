import pytest
from .. import src
from src import add
from add import add

def test_add():
    assert add(1, 2) == 3

if __name__ == "__main__":
    pytest.main()
