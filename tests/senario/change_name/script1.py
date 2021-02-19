from nore import nore


@nore
def plus1(x):
    return x + 1


def main():
    assert plus1(1) == 2
