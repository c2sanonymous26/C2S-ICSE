import logging
from typing import Any
from pathlib import Path

from rich.logging import RichHandler
from rich.text import Text
from typing import cast

INVT_LOGGER_NAME = "invention"
INST_LOGGER_NAME = "instantiation"
CHCK_LOGGER_NAME = "check"

# Define custom styles for log sources
LOG_STYLES = {
    "debug": "magenta",
    "info": "steel_blue1"
}

class ColoredRichHandler(RichHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_level_text(self, record: logging.LogRecord) -> Text:
        # If message is empty, return empty Text
        if not record.msg:
            return Text("")

        level_name = record.levelname.lower()
        if level_name in LOG_STYLES:
            color = LOG_STYLES[level_name]
            return Text(record.levelname, style=color)

        return super().get_level_text(record)

class CminerLogger(logging.Logger):
    def __init__(self, name: str, level: int = logging.NOTSET):
        super().__init__(name, level)

    def debug(self, msg: str, center: bool = False, symbol: str = "*", newlines: int = 0, *args, **kwargs):
        if center:
            msg = center_header(str(msg), symbol)
        
        # Add newlines
        if newlines > 0:
            msg = msg + "\n" * newlines
            
        super().debug(msg, *args, **kwargs)

    def info(self, msg: str, center: bool = False, symbol: str = "*", newlines: int = 0, *args, **kwargs):
        if center:
            msg = center_header(str(msg), symbol)
        
        # Add newlines
        if newlines > 0:
            msg = msg + "\n" * newlines
            
        super().info(msg, *args, **kwargs)
        
    def warning(self, msg: str, newlines: int = 0, *args, **kwargs):
        # Add newlines
        if newlines > 0:
            msg = msg + "\n" * newlines
            
        super().warning(msg, *args, **kwargs)
        
    def error(self, msg: str, newlines: int = 0, *args, **kwargs):
        # Add newlines
        if newlines > 0:
            msg = msg + "\n" * newlines
            
        super().error(msg, *args, **kwargs)
        
    def exception(self, msg: str, newlines: int = 0, *args, **kwargs):
        # Add newlines
        if newlines > 0:
            msg = msg + "\n" * newlines
            
        super().exception(msg, *args, **kwargs)

def build_logger(logger_name: str) -> Any:
    # Set custom logger class as default class for this logger
    logging.setLoggerClass(CminerLogger)

    # Create logger using custom class
    _logger = logging.getLogger(logger_name)

    # Reset logger class to default to avoid affecting other loggers
    logging.setLoggerClass(logging.Logger)

    # Create Rich handler
    rich_handler = ColoredRichHandler(
        show_time=False,
        rich_tracebacks=False,
        show_path=False,
        tracebacks_show_locals=False,
    )
    rich_handler.setFormatter(
        logging.Formatter(
            fmt="%(message)s",
            datefmt="[%X]",
        )
    )
    rich_handler.setLevel(logging.INFO)
    
    _logger.setLevel(logging.DEBUG)
    _logger.addHandler(rich_handler)
    _logger.propagate = False
    return _logger


# Create loggers
invt_logger: CminerLogger = build_logger(INVT_LOGGER_NAME)
inst_logger: CminerLogger = build_logger(INST_LOGGER_NAME)
chck_logger: CminerLogger = build_logger(CHCK_LOGGER_NAME)

def set_log_file_handler(logger_name: str, log_file_path: Path, file_level: int = logging.INFO):
    if logger_name == INVT_LOGGER_NAME:
        pass
    else:
        _logger = logging.getLogger(logger_name)
        
        clean_log_file_handler(logger_name)
        
        # Add new file handler
        file_handler = logging.FileHandler(log_file_path, mode='w')
        file_handler.setLevel(file_level)
        file_handler.setFormatter(logging.Formatter('%(message)s'))
        _logger.addHandler(file_handler)

def clean_log_file_handler(logger_name: str):
    if logger_name == INVT_LOGGER_NAME:
        pass
    else:
        _logger = logging.getLogger(logger_name)
        for handler in _logger.handlers[:]:
            if isinstance(handler, logging.FileHandler):
                _logger.removeHandler(handler)
                handler.close()

def center_header(message: str, symbol: str = "*") -> str:
    """
    Center display the message and fill both sides with specified symbols.
    
    Args:
        message: Message to display
        symbol: Symbol for padding
        
    Returns:
        Formatted message string
    """
    try:
        import shutil
        terminal_width = shutil.get_terminal_size().columns
    except Exception:
        terminal_width = 80  # Default width

    header = f" {message} "
    return f"{header.center(terminal_width - 20, symbol)}"

def log_debug(logger_name: str, msg: str, center: bool = False, symbol: str = "*", newlines: int = 0, *args, **kwargs):
    if logger_name in [INVT_LOGGER_NAME, INST_LOGGER_NAME, CHCK_LOGGER_NAME]:
        _logger = logging.getLogger(logger_name)
        _logger = cast(CminerLogger, _logger)  # Ensure correct type
        _logger.debug(msg, center=center, symbol=symbol, newlines=newlines, *args, **kwargs)

def log_info(logger_name: str, msg: str, center: bool = False, symbol: str = "*", newlines: int = 0, *args, **kwargs):
    if logger_name in [INVT_LOGGER_NAME, INST_LOGGER_NAME, CHCK_LOGGER_NAME]:
        _logger = logging.getLogger(logger_name)
        _logger = cast(CminerLogger, _logger)
        _logger.info(msg, center=center, symbol=symbol, newlines=newlines, *args, **kwargs)


def log_warning(logger_name: str, msg: str, newlines: int = 0, *args, **kwargs):
    if logger_name in [INVT_LOGGER_NAME, INST_LOGGER_NAME, CHCK_LOGGER_NAME]:
        _logger = logging.getLogger(logger_name)
        _logger = cast(CminerLogger, _logger)
        _logger.warning(msg, newlines=newlines, *args, **kwargs)
        
def log_error(logger_name: str, msg: str, newlines: int = 0, *args, **kwargs):
    if logger_name in [INVT_LOGGER_NAME, INST_LOGGER_NAME, CHCK_LOGGER_NAME]:
        _logger = logging.getLogger(logger_name)
        _logger = cast(CminerLogger, _logger)
        _logger.error(msg, newlines=newlines, *args, **kwargs)
        
def log_exception(logger_name: str, msg: str, newlines: int = 0, *args, **kwargs):
    if logger_name in [INVT_LOGGER_NAME, INST_LOGGER_NAME, CHCK_LOGGER_NAME]:
        _logger = logging.getLogger(logger_name)
        _logger = cast(CminerLogger, _logger)
        _logger.exception(msg, newlines=newlines, *args, **kwargs)
