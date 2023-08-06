import logging
from pathlib import Path
import sys
from zipfile import ZipFile

from dar_etl.config import Config
from dar_etl.consumer import NewDarFileNotificationConsumer
from dar_etl.parsing.parser import DarParser
from dar_etl.publisher import DarEntryPublisher


class DarEtl:
    def __init__(self, config: Config) -> None:
        self.publisher = DarEntryPublisher(config=config)
        self.consumer = NewDarFileNotificationConsumer(config=config)
        self.json_directory = config.app.json_directory
        self.parser = DarParser()

    def run(self) -> None:
        for filepath in self.consumer.consume():
            json_file = self._unzip(filepath=filepath)
            for entry in self.parser.parse(filepath=json_file):
                self.publisher.publish(metadata=entry)

    def _unzip(self, filepath: Path) -> Path:
        logging.info(f"[EXTRACTING] {filepath.name}")
        member = filepath.name.replace(".zip", ".json")
        json_file = self.json_directory.joinpath(member)
        if json_file.exists():
            logging.info(f"[EXTRACTED] {filepath.name}")
            return json_file
        with ZipFile(file=filepath, mode="r") as dar_zip_file:
            dar_zip_file.extract(member=member, path=self.json_directory)
        logging.info(f"[EXTRACTED] {filepath.name}")
        return json_file


def main() -> None:
    config = Config()
    logging.basicConfig(stream=sys.stdout, level=config.log.level)
    dar_etl = DarEtl(config=config)
    dar_etl.run()


if __name__ == "__main__":
    main()
