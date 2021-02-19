from nore import nore


@nore.nocache
def plus1(x):
    return x + 1


@nore
def plus2(x):
    return plus1(x) + 1


def main():
    assert plus2(1) == 3
    assert plus2(1) == 3
    assert plus1(1) == 2
