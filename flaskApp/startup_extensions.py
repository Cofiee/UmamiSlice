from configparser import ConfigParser
from flask import Flask

def startup(app: Flask, config_path: str) -> None:
    config_object = ConfigParser()
    config_object.read(config_path)

    app.config.update(
        SECRET_KEY='aaaa',
        REDIS_URL='redis://redis:6379/0',
        MINIO_URL=config_object['MINIO']['url'],
        MINIO_ACCESS_KEY=config_object['MINIO']['access_key'],
        MINIO_SECRET_KEY=config_object['MINIO']['secret_key'],
        MINIO_BUCKET_NAME=config_object['MINIO']['bucket']
    )
