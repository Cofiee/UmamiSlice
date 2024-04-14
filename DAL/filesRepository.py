import io
from abc import ABCMeta, abstractmethod
from minio import Minio
from PIL import Image


class IImagesRepository(metaclass=ABCMeta):

    @abstractmethod
    def insert_pil_image(self, image: Image, image_name: str) -> str:
        pass

    @abstractmethod
    def get_pil_image(self, image_name: str):
        pass

    @abstractmethod
    def insert_image(self, img_byte_array: io.BytesIO, image_name: str) -> str:
        pass

    @abstractmethod
    def get_image(self, image_name: str) -> io.BytesIO:
        pass


class ImagesMINIORepository(IImagesRepository):
    def __init__(self):
        self.__bucket_name = 'mybucket'
        self.__client = Minio('umamislice-minio-1:9000',
               access_key='minio_access_key',
               secret_key='minio_secret_key',
               secure=False)
        # Make a bucket
        if not self.__client.bucket_exists(self.__bucket_name):
            self.__client.make_bucket(self.__bucket_name)

    def insert_pil_image(self, image: Image, image_name: str) -> str:
        tmp = io.BytesIO()
        image.save(tmp, format='PNG')
        img_byte_array = io.BytesIO(tmp.getbuffer())
        self.__client.put_object(self.__bucket_name, image_name, img_byte_array, len(img_byte_array.getvalue()))
        return 'OK'

    def get_pil_image(self, image_name: str) -> Image:
        try:
            response = self.__client.get_object(self.__bucket_name, image_name)
            img_byte_array = response.read()
            return Image.open(io.BytesIO(img_byte_array))
        finally:
            response.close()
            response.release_conn()

    def insert_image(self, img_byte_array: io.BytesIO, image_name: str) -> str:
        self.__client.put_object(self.__bucket_name, image_name, img_byte_array, len(img_byte_array.getvalue()))
        return 'OK'

    def get_image(self, image_name: str) -> io.BytesIO:
        try:
            response = self.__client.get_object(self.__bucket_name, image_name)
            img_byte_array = response.read()
            return io.BytesIO(img_byte_array)
        finally:
            response.close()
            response.release_conn()
