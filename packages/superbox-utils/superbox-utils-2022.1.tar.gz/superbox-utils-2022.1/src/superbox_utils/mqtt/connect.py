import asyncio
import logging
import sys
from contextlib import AsyncExitStack
from typing import Callable
from typing import Final
from typing import Optional

from asyncio_mqtt import Client
from asyncio_mqtt import MqttError

from superbox_utils.mqtt.config import MqttConfig


class LogPrefix:
    MQTT: Final[str] = "[MQTT]"


async def mqtt_connect(mqtt_config: MqttConfig, logger: logging.Logger, mqtt_client_id: str, callback: Callable):
    logger.info("%s Client ID: %s", LogPrefix.MQTT, mqtt_client_id)

    reconnect_interval: int = mqtt_config.reconnect_interval
    retry_limit: Optional[int] = mqtt_config.retry_limit
    retry_reconnect: int = 0

    while True:
        try:
            logger.info("%s Connecting to broker ...", LogPrefix.MQTT)

            async with AsyncExitStack() as stack:
                mqtt_client: Client = Client(
                    mqtt_config.host,
                    mqtt_config.port,
                    client_id=mqtt_client_id,
                    keepalive=mqtt_config.keepalive,
                )

                await stack.enter_async_context(mqtt_client)
                retry_reconnect = 0

                logger.info("%s Connected to broker at '%s:%s'", LogPrefix.MQTT, mqtt_config.host, mqtt_config.port)

                await callback(stack=stack, mqtt_client=mqtt_client)
        except MqttError as error:
            logger.error(
                "%s Error '%s'. Connecting attempt #%s. Reconnecting in %s seconds.",
                LogPrefix.MQTT,
                error,
                retry_reconnect + 1,
                reconnect_interval,
            )
        finally:
            if retry_limit and retry_reconnect > retry_limit:
                sys.exit(1)

            retry_reconnect += 1

            await asyncio.sleep(reconnect_interval)
