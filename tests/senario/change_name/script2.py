from datastellar import datastellar


@datastellar
def add1(x):
    return x + 1


def main():
    assert add1(1) == 2
