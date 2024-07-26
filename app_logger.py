import logging

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(
    logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
)

handlers = [logging.FileHandler(filename='app.log', mode='a'), console]
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', handlers=handlers)
logger = logging.getLogger(__name__)

def info(*args):
    logger.info('>>>') if len(args) > 1 else None
    for arg in args:
        logger.info(arg)

    logger.info('<<<') if len(args) > 1 else None

def debug(*args):
    logger.debug('>>>') if len(args) > 1 else None
    for arg in args:
        logger.debug(arg)

    logger.debug('<<<') if len(args) > 1 else None

def error(*args):
    logger.error('>>>>>>>>') if len(args) > 1 else None
    for arg in args:
        logger.error(arg)

    logger.error('<<<<<<<<') if len(args) > 1 else None

