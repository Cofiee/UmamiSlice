import io
from abc import ABC, abstractmethod
from minio import Minio
from PIL import Image


class IImagesRepository(metaclass=ABC):

    @abstractmethod
    def insert_image(self, image_no_background: Image,  image_name: str) -> str:
        pass

    @abstractmethod
    def get_image(self, image_name: str):
        pass


class ImagesMINIORepository(metaclass=IImagesRepository):
    def __init__(self):
        self.__bucket_name = 'mybucket'
        self.__client = Minio('localhost:9000',
               access_key='minio_access_key',
               secret_key='minio_secret_key',
               secure=False)
        # Make a bucket
        self.__client.make_bucket(self.__bucket_name)

    def insert_image(self, image: Image, image_name: str) -> str:
        img_byte_array = io.BytesIO()
        image.save(img_byte_array, format='PNG')
        self.__client.put_object(self.__bucket_name, image_name, img_byte_array, len(img_byte_array))

    def get_image(self, image_name: str) -> Image:
        try:
            response = self.__client.get_object(self.__bucket_name, image_name)
            img_byte_array = response.readlines()
            return Image.open(img_byte_array)
        finally:
            response.close()
            response.release_conn()
