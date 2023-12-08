import logging
from config import LOG_FILE_PATH, DSL_LOG_PATH

formatter = logging.Formatter('%(asctime)s~%(levelname)s~%(message)s~module:%(module)s\n')

handler = logging.FileHandler(LOG_FILE_PATH)
handler.setFormatter(formatter)

handler_dsl = logging.FileHandler(DSL_LOG_PATH, mode='w')
handler.setFormatter(formatter)

logger = logging.getLogger('general')
logger.addHandler(handler)
logger.setLevel(logging.INFO)

dsl_logger = logging.getLogger('dsl')
dsl_logger.addHandler(handler_dsl)
dsl_logger.setLevel(logging.INFO)