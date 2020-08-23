import logging, sys
LOG_LEVEL = logging.DEBUG




def init_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(LOG_LEVEL)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(LOG_LEVEL)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger



logger = init_logger()