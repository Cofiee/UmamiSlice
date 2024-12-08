import io
from abc import ABCMeta, abstractmethod

import pika
from dependency_injector.wiring import inject
from flask_rq2 import RQ
from sympy import false

from DAL.filesRepository import IImagesRepository

class IBackgroundRemover(metaclass=ABCMeta):
    @abstractmethod
    def schedule_remove_background(self, image: io.BytesIO, image_guid: str) -> str:
        ...

    @abstractmethod
    def fetch_image(self, image_guid: str) -> io.BytesIO:
        ...

    @abstractmethod
    def get_job_status(self, job_id: str) -> str:
        ...


class BackgroundRemoverService(IBackgroundRemover):
    def __init__(self, rq: RQ, images_repository: IImagesRepository):
        self.__rq: RQ = rq
        self.__images_repository: IImagesRepository = images_repository

    def schedule_remove_background(self, image: io.BytesIO, image_guid: str) -> str:
        self.__images_repository.insert_image(image, image_guid)
        return self.__register_ml_job(image_guid)

    def fetch_image(self, image_guid: str) -> io.BytesIO:
        return self.__images_repository.get_image(image_guid)

    def get_job_status(self, job_id: str) -> str:
        queue = self.__rq.get_queue()
        job = queue.fetch_job(job_id)
        return job.get_status()

    def __register_ml_job(self, image_guid: str) -> str:
        queue = self.__rq.get_queue()
        job = queue.enqueue('worker.remove_background', image_guid)
        return job.id


class BackgroundRemoverServiceRabbitMq(IBackgroundRemover):
    def __init__(self, images_repository: IImagesRepository):
        self.__connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost', port=10002)
        )
        self.__channel = self.__connection.channel()
        self.__channel.queue_declare(
            queue='remove_background_queue',
            durable=False
        )

        self.__images_repository: IImagesRepository = images_repository

    def schedule_remove_background(self, image: io.BytesIO, image_guid: str) -> str:
        self.__images_repository.insert_image(image, image_guid)
        return self.__register_ml_job(image_guid)

    def fetch_image(self, image_guid: str) -> io.BytesIO:
        return self.__images_repository.get_image(image_guid)

    def get_job_status(self, job_id: str) -> str:
        return "False"

    def __register_ml_job(self, image_guid: str) -> str:
        self.__channel.basic_publish(
            exchange='',
            routing_key='remove_background_queue',
            body=image_guid,
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            )
        )
        return image_guid