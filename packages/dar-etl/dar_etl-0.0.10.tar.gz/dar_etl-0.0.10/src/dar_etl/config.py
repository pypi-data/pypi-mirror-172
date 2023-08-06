from pathlib import Path

from pydantic import BaseSettings

from dar_etl.version import __version__


class BaseConfig(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class KafkaConfig(BaseConfig):
    host: str
    port: int
    topic: str

    class Config:
        env_prefix = "kafka_"


class LogConfig(BaseConfig):
    level: str = "INFO"

    class Config:
        env_prefix = "log_"


class AppConfig(BaseConfig):
    input_directory: Path
    json_directory: Path


class Config:
    def __init__(self) -> None:
        self.version: str = __version__
        self.kafka = KafkaConfig()
        self.app = AppConfig()
        self.log = LogConfig()
