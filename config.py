class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'pass'
    USER = 'adkintun'
    SQLALCHEMY_DATABASE_URI = 'postgresql://' + USER + ':' + SECRET_KEY + '@localhost:5432/adkintun'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://joseto:pass@localhost/adkintun_test'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    TESTING = True
    DEBUG = True

class AdminUser():
    first_name = "Cambiar Usuario"
    last_name = "Cambiar Usuario"
    login = "Cambiar login"
    email = "Crear correo"
    password = "Cambiar pass"
