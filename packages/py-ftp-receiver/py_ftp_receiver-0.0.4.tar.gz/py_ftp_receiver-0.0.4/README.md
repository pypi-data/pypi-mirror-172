# Ftp Receiver

1. Checks existing files in output directory.
2. List files in root directory on FTP server.
3. Downloads all files which filename is not present in the output directory.
4. After each file download, publish an event to Kafka with the name of the downloaded file.

## Configuration

The application is configured via environment variables. See `example.env`.

## Development

For help getting started developing check [DEVELOPMENT.md](DEVELOPMENT.md)
