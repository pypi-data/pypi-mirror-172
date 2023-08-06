import logging

from confluent_kafka import KafkaError
from confluent_kafka import Message
from confluent_kafka import Producer

from ftp_receiver.config import Config


class KafkaPublisher:
    def __init__(self, config: Config) -> None:
        self.topic = "ftp-downloader"
        self.key = config.ftp.host.encode("utf-8")
        host = config.kafka.host
        port = config.kafka.port
        self.producer = Producer({"bootstrap.servers": f"{host}:{port}"})

    def publish(self, filename: str) -> None:
        self.producer.poll(0)
        self.producer.produce(
            topic=self.topic,
            key=self.key,
            value=filename.encode("utf-8"),
            on_delivery=self._on_delivery,
        )
        self.producer.flush()

    def _on_delivery(self, error: KafkaError, message: Message) -> None:
        if error:
            logging.error("Failed to publish.")
        else:
            logging.debug("Published %s successfully", message.key())
