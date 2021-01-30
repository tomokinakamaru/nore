from datastellar import datastellar


@datastellar.nocache
def plus1(x):
    return 1 + x


@datastellar
def plus2(x):
    return plus1(x) + 1


def main():
    assert plus2(1) == 3
