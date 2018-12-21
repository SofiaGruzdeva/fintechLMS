import os

if "TRAVIS_BUILD_DIR" in os.environ:
    db_dir = os.environ['TRAVIS_BUILD_DIR']
else:
    db_dir = '/C:/Users/admin/Documents/GitHub/LMS/'

class Development:

    DEBUG = True
    TESTING = False
    JWT_SECRET_KEY = 'hhgaghhgsdhdhdd'
    SQLALCHEMY_DATABASE_URI = 'sqlite://' + db_dir + 'db.db'


class Production:

    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://' + db_dir + 'db.db'
    JWT_SECRET_KEY = 'hhgaghhgsdhdhdd'


app_config = {
    'development': Development,
    'production': Production,
}
