from pathlib import Path

from pydantic import BaseSettings

from ftp_receiver.version import __version__


class BaseConfig(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class DownloadConfig(BaseConfig):
    directory: Path
    interval_seconds: int = 300
    match_pattern: str = ""

    class Config:
        env_prefix = "download_"


class KafkaConfig(BaseConfig):
    host: str
    port: int

    class Config:
        env_prefix = "kafka_"


class LogConfig(BaseConfig):
    level: str = "INFO"

    class Config:
        env_prefix = "log_"


class FTPConfig(BaseConfig):
    username: str
    password: str
    host: str
    port: int = 21

    class Config:
        env_prefix = "ftp_"


class Config:
    def __init__(self) -> None:
        self.version = __version__
        self.ftp = FTPConfig()
        self.kafka = KafkaConfig()
        self.download = DownloadConfig()
        self.log = LogConfig()
