import logging

logger = logging.getLogger('OPEN_LISA_SDK')
logger.setLevel(logging.DEBUG)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logging.Formatter('[%(name)s] %(asctime)s %(levelname)-8s %(message)s'))
logger.addHandler(consoleHandler)

def set_level(level):
  logger.setLevel(level)

def debug(msg):
  logger.debug(msg)

def info(msg):
  logger.info(msg)

def warn(msg):
  logger.warn(msg)

def warning(msg):
  logger.warning(msg)

def error(msg):
  logger.error(msg)