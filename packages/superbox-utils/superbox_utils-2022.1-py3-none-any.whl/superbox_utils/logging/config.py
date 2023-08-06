import dataclasses
import logging
from dataclasses import dataclass
from dataclasses import field
from typing import List

from superbox_utils.config.exception import ConfigException
from superbox_utils.config.loader import ConfigLoaderMixin
from superbox_utils.logging import LOG_LEVEL


@dataclass
class LoggingConfig(ConfigLoaderMixin):
    level: str = field(default="error")

    @property
    def verbose(self):
        return list(LOG_LEVEL).index(self.level)

    def update_level(self, name: str, verbose: int = 0):
        logger = logging.getLogger(name)

        levels: List[int] = list(LOG_LEVEL.values())
        level: int = levels[min(max(verbose, self.verbose), len(levels) - 1)]

        logger.setLevel(level)

    def _validate_level(self, value: str, _field: dataclasses.Field) -> str:
        if (value := value.lower()) not in LOG_LEVEL.keys():
            raise ConfigException(
                f"[{self.__class__.__name__.replace('Config', '').upper()}] Invalid log level '{self.level}'. The following log levels are allowed: {' '.join(LOG_LEVEL.keys())}."
            )

        return value
