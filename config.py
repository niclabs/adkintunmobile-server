class DefaultConfig(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "this-really-needs-to-be-changed"
    USER = "this-really-needs-to-be-changed"
    SQLALCHEMY_DATABASE_URI = "postgresql://" + USER + ":" + SECRET_KEY + "@localhost/this-really-needs-to-be-changed"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(DefaultConfig):
    SQLALCHEMY_DATABASE_URI = "postgresql://felipe:niclabs.13@127.0.0.1:8080/test_db"
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    TESTING = True
    DEBUG = True


class AppTokens:
    tokens = {
        # random string, size 50 : name of the token
        "token-for-app-mobile": "app_mobile",
    }


class AdminUser:
    first_name = "this-really-needs-to-be-changed"
    last_name = "this-really-needs-to-be-changed"
    login = "this-really-needs-to-be-changed"
    email = "this-really-needs-to-be-changed"
    password = "this-really-needs-to-be-changed"


class OpenCellIdToken:
    """
    Open CellId Key token used in the antenna geolocalization process
    """
    token = "this-really-needs-to-be-changed"

class Urls:
    BASE_URL_OPENCELLID = "http://url.opencellid"

class Files:
    LOGS_FOLDER = "tmp"
    GEOLOCALIZATION_LOG_FILE = "geolocalization.log"
    PRINCIPAL_LOG_FILE = "adkintun-debug.log"
    REPORT_GENERATOR_LOG_FILE = "reports.log"
    STATIC_FILES_FOLDER = "app/static"
    FILES_FOLDER = "speedtest_files"
    REPORTS_FOLDER = STATIC_FILES_FOLDER + "/" + "reports"
