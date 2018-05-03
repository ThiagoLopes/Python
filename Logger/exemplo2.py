"""
Exemplo 2.

Como escrever o log em um arquivo
"""
import logging

logging.basicConfig(
    filename='exemplo2.log',  # arquivo de saida
    filemode='w',  # a = append, w = write
    level=logging.DEBUG)

logging.debug('DEBUG in file')
logging.info('INFO in file')
logging.warning('WARNING in file')
logging.log(30, 'Level debug with log')
