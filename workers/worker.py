#!/usr/bin/env python
from os import getenv
from redis import Redis
from rq import Worker

# Preload libraries
from model.background_remover import process_image


def remove_background(image_name):
    process_image(image_name)


# Provide the worker with the list of queues (str) to listen to.
redis_url = "redis://redis:6379"
w = Worker(['default'], connection=Redis.from_url(redis_url))
w.work()