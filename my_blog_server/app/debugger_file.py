import logging
def set_up_logger(file_name):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    # write logs to a file
    file_handler = logging.FileHandler(f'{file_name}')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # write logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

