"""A clean Python module."""


def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


def main() -> None:
    """Main entry point."""
    result = add(1, 2)
    print(result)


if __name__ == "__main__":
    main()
