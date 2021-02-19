from nore import nore, Thread


@nore
def foo():
    pass


@nore
def bar():
    t = Thread(target=foo)
    t.start()
    t.join()


def main():
    bar()
