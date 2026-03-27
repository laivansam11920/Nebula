import logging
import os
import sys
from logging.handlers import RotatingFileHandler

try:
    import colorlog
except ImportError:
    pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_dir = os.path.join(BASE_DIR, "logs")

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

file_format = logging.Formatter(
    "%(asctime)s - [%(filename)s:%(lineno)d] - %(levelname)s - %(message)s"
)

if "colorlog" in sys.modules:
    console_format = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - [%(filename)s:%(lineno)d] - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
    )
else:
    console_format = logging.Formatter(
        "%(asctime)s - [%(filename)s:%(lineno)d] - %(levelname)s - %(message)s"
    )


# 3. Tạo Logger
def setup_logger():
    logger = logging.getLogger("App_Logger")
    logger.setLevel(logging.DEBUG)

    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "app.log"),
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setFormatter(file_format)
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_format)
    console_handler.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Khởi tạo một lần dùng mãi mãi
logger = setup_logger()
