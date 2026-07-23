"""A clean Python module."""


def greet(name: str) -> str:
    """Return a greeting string."""
    return f"Hello, {name}!"


if __name__ == "__main__":
    print(greet("world"))
