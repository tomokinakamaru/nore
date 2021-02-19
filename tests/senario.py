from nore import nore
from nore import functions
from importlib import import_module
from importlib import reload
from io import StringIO
from logging import DEBUG
from logging import Formatter
from logging import StreamHandler
from os import getcwd
from os import listdir
from os import makedirs
from os.path import dirname
from os.path import relpath
from os.path import join
from shutil import rmtree


class Senario(object):
    @staticmethod
    def find():
        return listdir(senario_root)

    def __init__(self, name):
        self.path = join(senario_root, name)
        self.workspace = Workspace(name)
        self.stream = None
        self.handler = None

    def run(self):
        self.workspace.create()

        nore.cache_path = self.workspace.cache_path
        for path in sorted(self.script_files()):
            functions.functions._funcs.clear()
            self.workspace.update_script(path).main()

        self.workspace.delete()

    def caputure_log(self):
        self.stream = StringIO()
        self.handler = StreamHandler(self.stream)
        self.handler.setFormatter(Formatter(log_format))
        nore.logger.addHandler(self.handler)
        nore.logger.setLevel(DEBUG)

    def get_captured_log(self):
        nore.logger.removeHandler(self.handler)
        return self.stream.getvalue().strip()

    def script_files(self):
        for name in listdir(self.path):
            if name.endswith('.py'):
                yield join(self.path, name)

    def read_expected_log(self):
        return read_file(join(self.path, log_file_name))


class Workspace(object):
    def __init__(self, name):
        self.name = workspace_name_format.format(name)
        self.path = join(workspace_root, self.name)
        self.cache_path = join(self.path, cache_dir_name)
        self.script_module = None

    def create(self):
        rmtree(self.path, ignore_errors=True)
        makedirs(self.path)

    def delete(self):
        rmtree(self.path)

    def update_script(self, src):
        write_file(join(self.path, script_file_name), read_file(src))
        self.script_module = self.reload_script_module()
        return self.script_module

    def reload_script_module(self):
        if self.script_module:
            return reload(self.script_module)
        return import_module(f'{self.name}.{script_name}')


def read_file(path):
    with open(path) as f:
        return f.read().strip()


def write_file(path, text):
    with open(path, 'w') as f:
        f.write(text)


tests_path = relpath(dirname(__file__), getcwd())

senario_dir_name = 'senario'

senario_root = join(tests_path, senario_dir_name)

workspace_root = tests_path

workspace_name_format = '_{}'

cache_dir_name = '.cache'

script_name = 'script'

script_file_name = f'{script_name}.py'

log_format = '%(levelname)s %(message)s'

log_file_name = 'log.txt'
