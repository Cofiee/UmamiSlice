import json
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect

from di_container import Container
from views import index, remove_background, get_image_no_background, get_job_status

# CONTROLLERS ##############
def register_endpoints(app: Flask) -> None:
    app.add_url_rule('/', view_func=index, methods=['GET'])
    app.add_url_rule('/api/remove-background', view_func=remove_background, methods=['POST'])
    app.add_url_rule('/api/removed-background/<image_guid>', view_func=get_image_no_background, methods=['GET'])
    app.add_url_rule('/api/status/<job_id>', view_func=get_job_status, methods=['GET'])


# FACTORY #################
def create_app(config_filename: str) -> Flask:
    container = Container()

    app = Flask(__name__)
    app.container = container

    if config_filename:
        app.config.from_file(config_filename, load=json.load)
        container.config.from_dict(app.config)

    Bootstrap5(app)
    CSRFProtect(app)
    container.redis_queue().init_app(app)
    container.wire(modules=["views"])

    register_endpoints(app)

    return app


#if __name__ == '__main__':
    #app.run(host='0.0.0.0')
