"""Module to provide consistent logging functions for application"""

import logging

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(
    logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
)

handlers = [logging.FileHandler(filename='app.log', mode='a'), console]
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=handlers
)

logger = logging.getLogger(__name__)

def info(*args):
    if len(args) > 1:
        logger.info('>>>')

    for arg in args:
        logger.info(arg)

    if len(args) > 1:
        logger.info('<<<')

def debug(*args):
    if len(args) > 1:
        logger.info('>>>')

    for arg in args:
        logger.debug(arg)

    if len(args) > 1:
        logger.info('<<<')


def error(*args):
    if len(args) > 1:
        logger.error('>>>>>>>>')

    for arg in args:
        logger.error(arg)

    if len(args) > 1:
        logger.error('<<<<<<<<')
