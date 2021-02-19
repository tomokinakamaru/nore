from logging import getLogger


def debug(msg):
    logger.debug(msg)


def info(msg):
    logger.info(msg)


def warn(msg):
    logger.warning(msg, exc_info=True)


logger = getLogger(__name__.split('.')[0])
