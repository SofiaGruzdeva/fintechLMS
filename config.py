class Development:

    DEBUG = True
    TESTING = False
    JWT_SECRET_KEY = 'hhgaghhgsdhdhdd'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///C:\\Users\\admin\\Fintech\\LMS1\\db.db'


class Production:

    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///C:\\Users\\admin\\Documents\\GitHub\\LMS\\db.db'
    JWT_SECRET_KEY = 'hhgaghhgsdhdhdd'


app_config = {
    'development': Development,
    'production': Production,
}
