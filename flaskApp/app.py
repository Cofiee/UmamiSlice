import io
import uuid
from DAL import filesRepository
from flask import Flask, flash, jsonify, redirect, render_template, request, send_file
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect
from flask_rq2 import RQ
from forms import ImageForm
from services import BackgroundRemoverServiceProxy

# APP #####################
app = Flask(__name__)
app.secret_key = 'aaaa'
bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)

app.config['RQ_REDIS_URL'] = 'redis://redis:6379/0'
rq = RQ(app)
default_queue = rq.get_queue()


# SERVICES ################
image_repository = filesRepository.ImagesMINIORepository()
image_processing_service = BackgroundRemoverServiceProxy(rq, image_repository)


# CONTROLLERS ##############
@app.route('/', methods=['GET', 'POST'])
def index():
    form = ImageForm()
    return render_template("index.html", form=form)


@app.route('/api/remove-background', methods=['POST'])
def remove_background():
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


@app.route('/api/removed-background/<image_guid>', methods=['GET'])
def get_image_no_background(image_guid):
    image = image_processing_service.fetch_image(image_guid)
    return send_file(image, mimetype='image/jpg')


@app.route('/api/status/<job_id>', methods=['GET'])
def get_job_status(job_id):
    status = image_processing_service.get_job_status(job_id)
    return {"status": status}


if __name__ == '__main__':
    app.run(host='0.0.0.0')
