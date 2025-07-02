import pytest

from main import k_add


@pytest.mark.parametrize(
    "first_int, second_int, expected",
    [
        (1, 2, 3),
        (2, 1, 3),
        (1, 1, 2),
        (2, 2, 4),
        (1, 3, 4),
        (3, 2, 5),
        (4, 2, 6),
        (3, 4, 7),
        (4, 4, 8),
        (3, 6, 9),
        (0, 0, 0),
        (-1, 2, 1),
        (1, -2, -1),
    ],
)
def test_k_add(first_int: int, second_int: int, expected: int) -> None:
    """Test the k_add function with various integer inputs."""
    result = k_add(first_int, second_int)
    assert result == expected, (
        f"Expected {expected} but got {result} for inputs {first_int} and {second_int}"
    )
