from datastellar import datastellar


@datastellar
def do_nothing():
    pass


def main():
    do_nothing()
    datastellar.gc()
    datastellar.lifetime = 0
    datastellar.gc()
    assert datastellar.lifetime == 0
