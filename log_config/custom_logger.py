import logging
from logging.config import fileConfig

fileConfig(u'./logging_config.ini')
logger = logging.getLogger()
