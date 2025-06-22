import logging

logger = logging.getLogger("kerbian")
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.handlers = []  # Remove any default handlers
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def debug(msg):
    logger.debug(msg)

def info(msg):
    logger.info(msg)

def warn(msg):
    logger.warning(msg)

def error(msg):
    logger.error(msg)