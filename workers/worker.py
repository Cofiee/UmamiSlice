#!/usr/bin/env python
from os import getenv
from redis import Redis
from rq import Worker

# Preload libraries
import model.model_mock

# Provide the worker with the list of queues (str) to listen to.
redis_url = "redis://redis:6379"
w = Worker(['default'], connection=Redis.from_url(redis_url))
w.work()