from nore import nore


@nore
def plus1(x):
    return 1 + x


def main():
    assert plus1(1) == 2
