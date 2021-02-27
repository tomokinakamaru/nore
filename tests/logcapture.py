from io import StringIO
from logging import getLogger
from logging import DEBUG
from logging import Formatter
from logging import StreamHandler


class LogCapture(object):
    def __enter__(self):
        self.renew_handler()
        return self

    def __exit__(self, typ, val, tb):
        logger.removeHandler(self.handler)

    def read(self):
        val = self.handler.stream.getvalue().strip()
        self.renew_handler()
        return val

    def renew_handler(self):
        self.handler = StreamHandler(StringIO())
        self.handler.setFormatter(Formatter('%(levelname)s %(message)s'))
        logger.addHandler(self.handler)


logger = getLogger('nore')

logger.setLevel(DEBUG)

logcapture = LogCapture()
