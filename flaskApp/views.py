import io
import uuid

from dependency_injector.wiring import inject, Provide
from flask import request, render_template, jsonify, send_file

from di_container import Container
from forms import ImageForm
from services import BackgroundRemoverService, BackgroundRemoverServiceRabbitMq


def index():
    form = ImageForm()
    return render_template("index.html", form=form)


@inject
def remove_background(
        image_processing_service: BackgroundRemoverServiceRabbitMq = Provide[Container.background_remover_service]
):
    if request.method == 'POST':
        form = ImageForm()
        new_file_name = uuid.uuid4().hex
        img_byte_array = request.files[form.image.name].read()
        image = io.BytesIO(img_byte_array)
        job_id = image_processing_service.schedule_remove_background(image, new_file_name)
        return jsonify({
            "imageSize": len(image.getvalue()),
            "job_id": job_id,
            "image_guid": new_file_name,
            "image_name": form.image.name
        })


@inject
def get_image_no_background(
    image_guid,
    image_processing_service: BackgroundRemoverServiceRabbitMq = Provide[Container.background_remover_service]
):
    image = image_processing_service.fetch_image(image_guid)
    return send_file(image, mimetype='image/jpg')


@inject
def get_job_status(
    job_id,
    image_processing_service: BackgroundRemoverServiceRabbitMq = Provide[Container.background_remover_service]
):
    status = image_processing_service.get_job_status(job_id)
    return {"status": status}