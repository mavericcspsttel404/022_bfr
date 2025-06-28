import pytest

from settings import TEST_IMPORTS, TEST_IMPORTS_INT, TEST_IMPORTS_TEXT


@pytest.mark.parametrize(
    "key_name, expected_value",
    [
        (TEST_IMPORTS, "True"),
        (TEST_IMPORTS_TEXT, "kgk"),
        (TEST_IMPORTS_INT, "9"),
    ],
)
def test_k_imports(key_name: str, expected_value: str) -> None:
    """Test the k_add function with various integer inputs."""
    assert key_name == expected_value, f"Expected {expected_value} but got {key_name}"
