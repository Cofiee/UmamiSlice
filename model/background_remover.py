from rembg import remove
from DAL import filesRepository
from PIL import Image


def process_image(image_name) -> str:
    image_repository = filesRepository.ImagesMINIORepository()
    image: Image = image_repository.get_pil_image(image_name)
    image_no_background: Image = remove(image)
    image_new_name = image_name + "_out"
    image_repository.insert_pil_image(image_no_background, image_new_name)
    return image_new_name
