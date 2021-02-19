from nore import nore


@nore
def do_nothing():
    pass


def main():
    do_nothing()
    nore.gc()
    nore.lifetime = 0
    nore.gc()
    assert nore.lifetime == 0
