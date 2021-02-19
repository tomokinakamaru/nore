from nore import nore
from inspect import isgenerator


@nore
def generator():
    yield 1
    yield 2
    yield 3


def main():
    for _ in range(2):
        g = generator()
        assert isgenerator(g)
        assert list(g) == [1, 2, 3]
