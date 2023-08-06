import functools
import inspect
import logging
import logging.config
from datetime import datetime
from pathlib import Path
from typing import Union

PATH_SRC = Path(__file__).resolve().parent


def fun(func):
    """
    Log a callable

    Args:
        func (callable): Callable to be logged

    Returns:
        Callable: Callable outputs

    References:
        [1] https://dev.to/aldo/implementing-logging-in-python-via-decorators-1gje
        [2] https://stackoverflow.com/questions/6810999/how-to-determine-file-function-and-line-number
    """
    logger = logging.getLogger()

    # Filename where the function is called from
    func_filename = inspect.currentframe().f_back.f_code.co_filename

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        callerframerecord = inspect.stack()[1]
        frame = callerframerecord[0]
        info = inspect.getframeinfo(frame)

        # Line where the function is called from
        func_lineno = info.lineno

        entering_time = datetime.now()
        logger.info(
            f"{Path(func_filename).name} || {func.__module__} || {func_lineno} || Enter || {func.__name__}")

        try:
            return func(*args, **kwargs)

        except Exception as e:
            error_msg = f"In {func.__name__}"
            logger.exception(error_msg, exc_info=True)
            raise e

        finally:
            leaving_time = datetime.now()
            logger.info(
                f"{Path(func_filename).name} || {func.__module__} || {func_lineno} || Leave || {func.__name__} || Elapsed: {leaving_time - entering_time}")

    return wrapper


def make_path(path: Path=PATH_SRC/"logs") -> Path:
    """
    Create logs directory if it doesn't exist

    Args:
        path (Path, optional): Path where the log file is saved. Defaults to PROJECT_ROOT/logs/.
        test (bool): Return filename

    Returns:
        (Path): Path to logs directory

    Example:
        >>> _ = make_path()
    """
    path.mkdir(parents=True, exist_ok=True)

    return path


def config_logger(log_config_file: Path=PATH_SRC/"conf"/"logging.conf") -> logging.getLogger:
    """
    Configure logger object

    Args:
        log_config_file (Path, optional): Path where the log config file is. Defaults to PROJECT_ROOT / "cartorio" / "conf" / "logging.conf".

    Returns:
        (logging.getLogger): Logger object

    Example:
        >>> _ = config_logger()
    """

    logging.config.fileConfig(str(log_config_file),
                              disable_existing_loggers=False)

    return logging.getLogger()


def set_handler(filename: str, log_format: str, logs_path: Path) -> logging.FileHandler:
    """
    Set file handler for logger object

    Args:
        filename (str): File to be logged
        log_format (str): Log format
        logs_path (Path): Path where the log is saved.
    
    Raises:
        IOError: If folder doesn't exist

    Returns:
        (logging.FileHandler): File handler object

    Example:
        >>> format_filename = f"{Path(__file__).stem}.log"
        >>> log_format = logging.Formatter('%(asctime)-16s || %(name)s || %(process)d || %(levelname)s || %(message)s')
        >>> logs_path = Path(__file__).resolve().parent
        >>> _ = set_handler(__file__, log_format, logs_path=logs_path)
    """
    if not logs_path.is_dir():
        msg = f"Expected dir {logs_path} to exist."
        raise IOError(msg)

    fh = logging.FileHandler(str(logs_path / f'{filename}'))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(log_format)

    return fh


def log(filename: Union[str, Path], logs_path: Path
        ,log_config_file=PATH_SRC/"conf"/"logging.conf"):
    """
    Instantiate logger object

    Args:
        filename (str, Path): Log file
        logs_path (Path): Path where the log file is saved
        log_config_file (Path, optional): Path contaning the log config file. Defaults to PROJECT_ROOT / "conf" / "logging.conf"

    Returns:
        (logging.getLogger()): Logging object

    Example:
        >>> logs_path = Path(__file__).resolve().parent
        >>> logger = log("test.log", logs_path)

    References:
        [1] https://realpython.com/python-logging/
    """
    # 1. Create logs directory if it doesn't exist
    _ = make_path(logs_path)

    # 2. Instantiate logger object
    logger = config_logger(log_config_file=log_config_file)

    # 3. Create log file
    format_filename = f"{Path(filename).stem}_{datetime.now().date()}_{datetime.now().time()}.log"
    log_format = logging.Formatter(
        '%(asctime)-16s || %(name)s || %(process)d || %(levelname)s || %(message)s')

    fh = set_handler(format_filename, log_format, logs_path)

    logger.addHandler(fh)

    return logger


if __name__ == "__main__":
    logs_path = Path(__file__).resolve().parent
    logger = log(__file__, logs_path)
