from nore.stack import stack


def test_empty():
    stack.push(1)
    assert not stack.empty()

    stack.pop()
    assert stack.empty()


def test_peak():
    stack.push(1)
    assert stack.peak() == 1

    stack.pop()
    assert stack.peak() is None
