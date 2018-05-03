"""
Exemplo 4.

Explicação de todas etapas do logger
"""
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formater = logging.Formatter(
    '%(asctime)s:%(levelname)s:%(filename)s:%(lineno)s:%(message)s'
)

# console Handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formater)

# file Handler
fh = logging.FileHandler('log.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formater)

logger.addHandler(ch)
logger.addHandler(fh)

logger.debug('Olá')
