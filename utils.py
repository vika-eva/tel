import logging
import sys
from aiogram.types import BotCommand

def config_logger() -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

COMMANDS = [
    BotCommand(command='start', description='Starts dialog with Bot'),
]
