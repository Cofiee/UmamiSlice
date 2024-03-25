from abc import ABC, abstractmethod
from rembg import remove
from DAL import filesRepository
from PIL import Image


class IBackgroundRemover(metaclass=ABC):
    @abstractmethod
    def remove_background(self, image_name):
        pass


class RembgBackgroundRemover(IBackgroundRemover):
    def __init__(self):
        self.image_repository: filesRepository.IImagesRepository = filesRepository.ImagesMINIORepository()

    def remove_background(self, image_name) -> str:
        image: Image = self.image_repository.get_image(image_name)
        image_no_background: Image = remove(image)
        self.image_repository.insert_image(image_no_background, image_name)
        return image_name + "_out"
