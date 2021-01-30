from datastellar import datastellar, Thread


@datastellar
def foo():
    pass


@datastellar
def bar():
    t = Thread(target=foo)
    t.start()
    t.join()


def main():
    bar()
