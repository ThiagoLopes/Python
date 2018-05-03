"""
Exemplo 3.

Como personalizar a msg do log
"""
import logging

log_format = '%(asctime)s:%(levelname)s:%(filename)s:%(lineno)s:%(message)s'

logging.basicConfig(
    filename='exemplo3.log',  # arquivo de saida
    filemode='w',  # a = append, w = write
    level=logging.DEBUG,
    format=log_format)  # add format in logging

logger = logging.getLogger('root')  # get the logging root


def add(x: int, y: int) -> int:
    """Função que efetura a soma de dois inteiro"""
    if isinstance(x, int) and isinstance(y, int):
        logger.info(f'x: {x} - y: {y}')
        return x + y
    logger.warning(
        f'x: {x} type: {type(x)} - y: {y} type: {type(y)}'
    )


add(7, 7)
add(7.4, 1.1)
