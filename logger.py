import logging
from global_config import LOG_FILE_PATH

formatter = logging.Formatter('%(asctime)s~%(levelname)s~%(message)s~module:%(module)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(handler)