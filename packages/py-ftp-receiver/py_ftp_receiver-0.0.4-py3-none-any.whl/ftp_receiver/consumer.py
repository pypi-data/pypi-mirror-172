import logging
from typing import Iterable, Optional

from confluent_kafka import Consumer

from ftp_receiver.config import Config


class ExistingFilesKafkaConsumer:
    def __init__(self, config: Config) -> None:
        self.topic = "ftp-downloader"
        host = config.kafka.host
        port = config.kafka.port
        self.consumer = Consumer(
            {
                "bootstrap.servers": f"{host}:{port}",
                "group.id": "existing-files-consumer",
                "auto.offset.reset": "earliest",
                "enable.auto.commit": "false",
            },
        )
        self.consumer.subscribe([self.topic])

    def consume(self) -> Iterable[str]:
        logging.info("Consume existing")
        count = 0
        while True:
            new_file = self.consume_one()
            if new_file:
                count += 1
                yield new_file
            else:
                break
        logging.info("Finished consuming %d exisiting files.", count)
        self.consumer.close()

    def consume_one(self) -> Optional[str]:
        for message in self.consumer.consume(timeout=10):
            error = message.error()
            if error:
                logging.error(error)
                return None
            return message.value().decode("utf-8")
        return None
