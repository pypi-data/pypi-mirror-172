import logging
from collections import OrderedDict
from typing import Dict
from typing import Final
from typing import Optional

DEFAULT_LOG_FORMAT: Final[str] = "%(levelname)s | %(message)s"

LOG_LEVEL: Final[Dict[str, int]] = OrderedDict(
    {
        "error": logging.ERROR,
        "warning": logging.WARNING,
        "info": logging.INFO,
        "debug": logging.DEBUG,
    }
)

stream_handler: logging.StreamHandler = logging.StreamHandler()


def init_logger(name: str, level: str, handlers: list, fmt: Optional[str] = None) -> logging.Logger:
    logger: logging.Logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL[level.lower()])

    if not fmt:
        fmt = DEFAULT_LOG_FORMAT

    for handler in handlers:
        handler.setFormatter(logging.Formatter(fmt))
        handler.setLevel(LOG_LEVEL[level.lower()])
        logger.addHandler(handler)

    return logger
