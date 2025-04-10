import pytest
from src import add

def test_add():
    assert add.add(1, 2) == 3

if __name__ == "__main__":
    pytest.main()
