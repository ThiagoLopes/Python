"""
Exemplo 1.

Exemplificação do nível/level do log default
"""
import logging

logging.basicConfig(filename='exemplo.log',
                    level=logging.DEBUG)

logging.debug('debug')
logging.info('info')
logging.warning('warning')
