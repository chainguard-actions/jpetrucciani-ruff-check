"""A clean Python module with no linting issues."""


def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


def subtract(a: int, b: int) -> int:
    """Subtract b from a."""
    return a - b


def main() -> None:
    """Main entry point."""
    result = add(1, 2)
    print(result)
