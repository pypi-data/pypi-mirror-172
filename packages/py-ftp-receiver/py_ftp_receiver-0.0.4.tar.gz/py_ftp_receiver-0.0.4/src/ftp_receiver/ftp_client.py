from ftplib import FTP  # noqa: S402
import logging

from ftp_receiver.config import Config


class FTPClient:
    def __init__(self, config: Config) -> None:
        ftp_config = config.ftp
        self.logger = logging.getLogger(ftp_config.host)
        self.ftp = FTP(  # noqa: S321
            host=ftp_config.host,
            user=ftp_config.username,
            passwd=ftp_config.password,
        )
        self.output_dir = config.download.directory

    def list(self) -> list[str]:
        return self.ftp.nlst()

    def download(self, filename: str) -> None:
        self.logger.info(f"Downloading {filename}")
        output_file = self.output_dir.joinpath(filename)
        with open(file=output_file, mode="wb") as fp:
            self.ftp.retrbinary(cmd=f"RETR {filename}", callback=fp.write)

    def quit(self) -> None:
        self.ftp.quit()
        self.logger.info("Quit")
