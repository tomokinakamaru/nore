from logging import getLogger
from logging import DEBUG
from logging import INFO
from logging import WARNING
from .stack import stack


class CallLogger(object):
    def __init__(self):
        self._logger = getLogger('nore')

    def reading_cache(self, name, args, kwargs):
        self.log(INFO, f'Reading cache for {name}', args, kwargs)

    def found_no_cache(self, name, args, kwargs):
        self.log(DEBUG, f'Found no cache for {name}', args, kwargs)

    def found_broken_cache(self, name, args, kwargs):
        self.log(DEBUG, f'Found broken cache for {name}', args, kwargs)

    def failed_to_read_cache(self, name, args, kwargs):
        self.log(WARNING, f'Failed to read cache for {name}', args, kwargs)

    def running_func(self, name, args, kwargs):
        self.log(INFO, f'Running {name}', args, kwargs)

    def log(self, level, msg, args, kwargs):
        msg += f' with args={args} and kwargs={kwargs}'
        if not stack.empty():
            msg += f' (from {stack.peak().name})'
        self._logger.log(level, msg)


class ValidationLogger(object):
    def __init__(self):
        self._logger = getLogger('nore')

    def detected_deletion(self, name, parent):
        self.log(f'Detected deletion of {name}', parent)

    def detected_change(self, name, parent):
        self.log(f'Detected change of {name}', parent)

    def found_no_cache(self, name, parent):
        self.log(f'Found no cache for {name}', parent)

    def found_invalid_cache(self, name, parent):
        self.log(f'Found invalid cache for {name}', parent)

    def found_broken_deps(self, name, parent):
        self.log(f'Found broken deps file for {name}', parent)

    def found_invalid_cache_propagated(self, name, child, parent):
        self.log(
            f'Found invalid cache for {name}; propagation from {child}',
            parent
        )

    def log(self, msg, parent):
        if parent:
            msg += f' (dependency of {parent.name})'
        self._logger.debug(msg)


clogger = CallLogger()

vlogger = ValidationLogger()
