import os

class Development(object):

    DEBUG = True
    TESTING = False
    JWT_SECRET_KEY = 'hhgaghhgsdhdhdd'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///C:\\Users\\admin\\Fintech\\LMS1\\db.db'

class Production(object):

    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///C:\\Users\\admin\\Documents\\GitHub\\LMS\\db.db'
    JWT_SECRET_KEY = 'hhgaghhgsdhdhdd'

app_config = {
    'development': Development,
    'production': Production,
}
