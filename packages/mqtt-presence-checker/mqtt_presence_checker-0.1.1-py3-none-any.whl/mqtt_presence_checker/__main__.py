import toml
import asyncio
from asyncio_mqtt import Client
from loguru import logger
from jsonargparse import CLI, set_docstring_parse_options
from docstring_parser import DocstringStyle
from dotwiz import DotWiz

from . import ping
from .minuterie import Minuterie
from .mqtt import mqtt_source, mqtt_sink, MQTTTopic

set_docstring_parse_options(style=DocstringStyle.REST)


def parse_mqtt_sensors(config, mqtt):
    try:
        return [
            mqtt_source(mqtt, sensor.topic, eval(sensor.predicate))
            for name, sensor in config.mqtt.sensor.items() if 'sensor' in config.mqtt
        ]
    except SyntaxError as e:
        logger.error(f'There is an error in your sensor configuration! {config.mqtt.sensor}')
        raise e


async def async_main(config):
    async with Client(
            config.mqtt.host,
            username=config.mqtt.username,
            password=config.mqtt.password,
            logger=logger) as mqtt:
        mqtt_sensors = parse_mqtt_sensors(config, mqtt)
        logger.debug(mqtt_sensors)

        async with Minuterie(
                sources=[
                            ping.availability_loop(host)
                            for host in config.ping.hosts
                        ] + mqtt_sensors,
                sinks=[
                    mqtt_sink(mqtt, config.mqtt.topic)
                ],
                cooldown=config.main.cooldown
        ) as presence:
            while True:
                await asyncio.sleep(1)


def main(conf_path: str = './config.toml'):
    config = toml.load(conf_path)
    logger.debug(config)

    asyncio.run(async_main(DotWiz(config)))


if __name__ == '__main__':
    try:
        CLI(main)
    except KeyboardInterrupt:
        ...
