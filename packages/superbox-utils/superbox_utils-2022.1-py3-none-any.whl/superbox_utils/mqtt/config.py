from dataclasses import dataclass
from dataclasses import field

from superbox_utils.config.loader import ConfigLoaderMixin


@dataclass
class MqttConfig(ConfigLoaderMixin):
    host: str = field(default="localhost")
    port: int = field(default=1883)
    keepalive: int = field(default=15)
    retry_limit: int = field(default=30)
    reconnect_interval: int = field(default=10)
