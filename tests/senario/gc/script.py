from nore import nore


@nore
def do_nothing():
    pass


def main():
    do_nothing()
    nore.gc(10)
    nore.gc(0)
