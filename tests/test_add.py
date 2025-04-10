import pytest
import src

def test_add():
    assert src.add(1, 2) == 3

if __name__ == "__main__":
    pytest.main()
