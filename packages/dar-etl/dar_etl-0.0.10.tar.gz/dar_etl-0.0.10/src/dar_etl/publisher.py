import logging

from confluent_kafka import KafkaError
from confluent_kafka import Message
from confluent_kafka import Producer

from dar_etl.config import Config
from dar_etl.parsing.parser import Metadata


class DarEntryPublisher:
    def __init__(self, config: Config) -> None:
        host = config.kafka.host
        port = config.kafka.port
        self.producer = Producer({"bootstrap.servers": f"{host}:{port}"})

    def publish(self, metadata: Metadata) -> None:
        self.producer.poll(0)
        self.producer.produce(
            topic=metadata.root.value,
            key=metadata.filename.encode("utf-8"),
            value=metadata.dar_model.json().encode("utf-8"),
            on_delivery=self._on_delivery,
        )

    def flush(self) -> None:
        self.producer.flush()

    def _on_delivery(self, error: KafkaError, message: Message) -> None:
        if error:
            logging.error("Failed to publish.")
        else:
            logging.debug("Published %s successfully", message.key())
