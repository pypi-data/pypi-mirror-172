import logging
from pathlib import Path
import re
import sys
import time

from ftp_receiver.config import Config
from ftp_receiver.consumer import ExistingFilesKafkaConsumer
from ftp_receiver.ftp_client import FTPClient
from ftp_receiver.publisher import KafkaPublisher


def main() -> None:
    config = Config()
    try:
        run_until_cancelled(config=config, publisher=KafkaPublisher(config=config))
    except KeyboardInterrupt:
        logging.info("Interrupted by keyboard")


def run_until_cancelled(config: Config, publisher: KafkaPublisher) -> None:
    logging.basicConfig(stream=sys.stdout, level=config.log.level)

    interval = config.download.interval_seconds
    while True:  # noqa: WPS457 infinite-while-loop
        logging.info(f"Running FTP Receiver v{config.version}")
        run(config=config, publisher=publisher)
        logging.info(f"Run completed, sleeping for {interval} seconds")
        time.sleep(interval)


def run(config: Config, publisher: KafkaPublisher) -> None:
    client = FTPClient(config=config)
    downloaded = filenames(output=config.download.directory)
    for missing in missing_files(config=config):
        publisher.publish(filename=missing)

    for filename in sorted(client.list()):
        if filename in downloaded:
            continue
        if re.match(config.download.match_pattern, filename):
            client.download(filename=filename)
            publisher.publish(filename=filename)
    client.quit()


def missing_files(config: Config) -> list[str]:
    published_filenames_consumer = ExistingFilesKafkaConsumer(config=config)
    missing = filenames(output=config.download.directory)
    for published_filename in published_filenames_consumer.consume():
        if published_filename in missing:
            missing.remove(published_filename)
    logging.info("missing files added: %d", len(missing))
    return sorted(missing)


def filenames(output: Path) -> set[str]:
    return {filepath.name for filepath in output.iterdir()}


if __name__ == "__main__":
    main()
