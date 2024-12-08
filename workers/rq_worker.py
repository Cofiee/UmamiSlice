#!/usr/bin/env python
from os import getenv
from redis import Redis
from rq import Worker

# Preload libraries
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


def remove_background(image_name):
    process_image(image_name)


# Provide the worker with the list of queues (str) to listen to.
redis_url = "redis://redis:6379"
w = Worker(['default'], connection=Redis.from_url(redis_url))
w.work()