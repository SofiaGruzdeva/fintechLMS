import os

from lms import create_app


ENV__NAME = os.getenv('FLASK_ENV')
APP = create_app(ENV__NAME)

if __name__ == '__main__':
    APP.run()
