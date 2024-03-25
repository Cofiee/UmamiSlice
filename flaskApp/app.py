from flask import Flask, render_template
from flask_rq2 import RQ
from model.model_mock import process_image_model

app = Flask(__name__)
app.config['RQ_REDIS_URL'] = 'redis://redis:6379/0'
rq = RQ(app)
default_queue = rq.get_queue()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/start/task')
def start_task():
    from model import model_mock
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
