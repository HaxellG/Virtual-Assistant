import logging

def setup_logger(name, log_file, level=logging.INFO, fmt='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p'):
    """
    Function to setup a logger instance.
    
    Args:
        name (str): Name for the logger instance.
        log_file (str): The name and location of the log file.
        level (int, optional): Level of logging. Defaults to logging.INFO.
        fmt (str, optional): The format in which logs will be written in the log file. Defaults to '%(asctime)s %(levelname)s %(message)s'.
        datefmt (str, optional): The format of date to be included in logs. Defaults to '%m/%d/%Y %I:%M:%S %p'.
    
    Returns:
        logger instance with specified configurations.
    """

    # Define the formatter based on the provided format and date format
    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)

    # Add the formatter to the handler
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

logger = setup_logger('first_logger', 'first_logfile.log')
logger.info('This is just info message')