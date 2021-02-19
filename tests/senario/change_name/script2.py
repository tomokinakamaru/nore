from nore import nore


@nore
def add1(x):
    return x + 1


def main():
    assert add1(1) == 2
