import io
import uuid
from DAL import filesRepository
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect
from flask_rq2 import RQ
from forms import ImageForm
from model.model_mock import process_image_model
from services import ImageProcessingService

# APP #####################
app = Flask(__name__)
app.secret_key = 'aaaa'
bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)

app.config['RQ_REDIS_URL'] = 'redis://redis:6379/0'
rq = RQ(app)
default_queue = rq.get_queue()


# SERVICES ################
image_processing_service = ImageProcessingService(rq)


# CONTROLERS ##############
@app.route('/', methods=['GET', 'POST'])
def index():
    form = ImageForm()
    if request.method == 'GET':
        return render_template("index.html", form=form)
    elif request.method == 'POST' and form.validate_on_submit():
        image_repository = filesRepository.ImagesMINIORepository()
        new_file_name = uuid.uuid4().hex
        img_byte_array = request.files[form.image.name].read()
        image = io.BytesIO(img_byte_array)
        image_repository.insert_image(image, new_file_name)
        job_id = image_processing_service.register_ml_job(new_file_name)
        response = {
            "imageSize": len(image.getvalue()),
            "jobId": job_id,
            "image_guid": new_file_name,
            "image_name": form.image.name
        }
        return response

    return render_template("index.html", form=form)


@app.route('/start/task')
def start_task():
    job = default_queue.enqueue(process_image_model, "guid")
    return f"Task (ID: {job.id}) added to queue at {job.enqueued_at}"


@app.route('/results/<job_id>')
def get_results(job_id):
    job = default_queue.fetch_job(job_id)
    if job.is_finished:
        return f"The result is: {job.return_value()}", 200
    else:
        return "Still processing. Please refresh!", 202


if __name__ == '__main__':
    app.run(host='0.0.0.0')
