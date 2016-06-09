class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    USER = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = 'postgresql://' + USER + ':' + SECRET_KEY + '@localhost/adkintun'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://user_test:password_test@localhost/adkintun_test'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    TESTING = True
    DEBUG = True

class AppTokens():
    tokens = {
        # tokens generados aleatoriamente, de largo 50
        "token-for-app-mobile": "app_mobile",
    }


class AdminUser():
    first_name = "Cambiar Usuario"
    last_name = "Cambiar Usuario"
    login = "Cambiar login"
    email = "Crear correo"
    password = "Cambiar pass"


class Visualization():
    real_time_info= False