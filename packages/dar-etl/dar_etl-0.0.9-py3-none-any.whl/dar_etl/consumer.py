import logging
from pathlib import Path
import sys
from typing import Iterable

from confluent_kafka import Consumer

from dar_etl.config import Config


class NewDarFileNotificationConsumer:
    def __init__(self, config: Config) -> None:
        host = config.kafka.host
        port = config.kafka.port

        self.input_dir = config.app.input_directory
        self.consumer = Consumer(
            {
                "bootstrap.servers": f"{host}:{port}",
                "group.id": "dar-etl-notification-consumer",
                "auto.offset.reset": "earliest",
                "max.poll.interval.ms": sys.maxsize,
            },
        )
        self.consumer.subscribe([config.kafka.topic])

    def consume(self) -> Iterable[Path]:
        try:
            while True:  # noqa: WPS457
                yield from self._consume()
        except KeyboardInterrupt:
            logging.info("Consumer was interrupted by user")

    def _consume(self) -> Iterable[Path]:
        for message in self.consumer.consume(timeout=10):
            error = message.error()
            if error:
                logging.error(error)
                continue
            filename: str = message.value().decode("utf-8")
            logging.info(f"[CONSUMED] {filename}")
            yield self.input_dir.joinpath(filename)
