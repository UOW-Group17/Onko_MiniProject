import pytest
from src import add

def test_add():
    assert add(1, 2) == 3

# edge case testing
def test_add_edge_cases():
    # Test negative numbers
    assert add(-1, -2) == -3
    # Test addition involving zero
    assert add(0, 5) == 5
    # Test large numbers
    assert add(1000000000, 1) == 1000000001

if __name__ == "__main__":
    pytest.main()
