import logging
import logging.config

logging.config.fileConfig('simple_loggin.ini')

logger = logging.getLogger('best_root')

logger.info('Olá fileConfig')
