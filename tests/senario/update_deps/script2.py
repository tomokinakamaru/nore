from datastellar import datastellar


@datastellar
def plus1(x):
    return 1 + x


@datastellar
def plus1_and_mult2(x):
    return plus1(x) * 2


def main():
    assert plus1_and_mult2(1) == 4
