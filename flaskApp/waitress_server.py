from app_factory import create_app
from waitress import serve

if __name__ == '__main__':
    serve(create_app("../config.json"), host='0.0.0.0', port=5000)
