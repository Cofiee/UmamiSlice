import io

from flask_rq2 import RQ

from DAL.filesRepository import IImagesRepository
from forms import ImageForm
from model.model_mock import process_image_model


class ImageProcessingService:
    def __init__(self, rq: RQ, images_repository: IImagesRepository):
        self.__rq: RQ = rq
        self.__images_repository: IImagesRepository = images_repository

    def remove_background(self, image: io.BytesIO, image_name: str) -> str:
        self.__images_repository.insert_image(image, image_name)
        return self.__register_ml_job(image_name)

    def __register_ml_job(self, job_guid: str) -> str:
        queue = self.__rq.get_queue()
        job = queue.enqueue(process_image_model, job_guid)
        return job.id

