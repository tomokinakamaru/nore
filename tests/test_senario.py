from re import sub
from senario import Senario


def test_nocache():
    s = run('nocache')
    assert s.get_captured_log() == s.read_expected_log()


def test_run_once():
    s = run('run_once')
    assert s.get_captured_log() == s.read_expected_log()


def test_change_code():
    s = run('change_code')
    assert s.get_captured_log() == s.read_expected_log()


def test_run_twice():
    s = run('run_twice')
    assert s.get_captured_log() == s.read_expected_log()


def test_update_deps():
    s = run('update_deps')
    assert s.get_captured_log() == s.read_expected_log()


def test_generator():
    s = run('generator')
    assert s.get_captured_log() == s.read_expected_log()


def test_gc():
    s = run('gc')
    log = s.get_captured_log()
    log = sub(r'touched at.+', 'touched at ...', log)
    assert log == s.read_expected_log()


def test_threading():
    s = run('threading')
    assert s.get_captured_log() == s.read_expected_log()


def test_change_name():
    s = run('change_name')
    assert s.get_captured_log() == s.read_expected_log()


def run(name):
    s = Senario(name)
    s.caputure_log()
    s.run()
    return s
