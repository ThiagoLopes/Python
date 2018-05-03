from functools import wraps
import logging


log_format = '%(asctime)s:%(levelname)s:%(filename)s:%(lineno)s:%(message)s'

logging.basicConfig(
    filename='decorator.log',  # arquivo de saida
    filemode='w',  # a = append, w = write
    level=logging.DEBUG,
    format=log_format)  # add format in logging

logger = logging.getLogger('root')  # get the logging root


def log(func):
    @wraps(func)
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        l_sms = f'func:{func.__name__} args:{args} kwargs{kwargs} result:{result}'
        logger.debug(l_sms)
        return result
    return inner


@log
def test_decorator(*items):
    return '202 OK'


test_decorator(10, 20, 30, 'ok', True)
