from attr.validators import instance_of
from dependency_injector import containers, providers
from flask_rq2 import RQ

from DAL.filesRepository import IImagesRepository, ImagesMINIORepository
from services import BackgroundRemoverService


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    images_repository = providers.Dependency(
        instance_of=IImagesRepository, default=providers.Factory(
            ImagesMINIORepository,
            bucket_name=config.MINIO_BUCKET,
            url=config.MINIO_URL,
            access_key=config.MINIO_ACCESS_KEY,
            secret_key=config.MINIO_SECRET_KEY
        ))

    redis_queue = providers.Singleton(RQ)

    background_remover_service = providers.Dependency(
        instance_of=BackgroundRemoverService, default=providers.Factory(
            BackgroundRemoverService,
            rq=redis_queue,
            images_repository=images_repository,
        ))

