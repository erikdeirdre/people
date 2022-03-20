from os import (path, environ)

basedir = path.abspath(path.dirname(__file__))
DATABASE_DIR = environ.get('DATABASE_DIR') or basedir

APP_NAME = 'people'

SQLALCHEMY_URI = environ.get("SQLALCHEMY_URI")
SQLALCHEMY_DATABASE_URI = SQLALCHEMY_URI

SECRET_KEY = environ.get('SECRET_KEY', 'my_secret')
SECRET_TIMEOUT = int(environ.get('SECRET_TIMEOUT', '900'))
DEBUG = environ.get('DEBUG', False)
TESTING = environ.get('TESTING', False)
BCRYPT_LOG_ROUNDS = 13

# Flask-security settings
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_PASSWORD_SALT = environ.get('PASSWORD_SALT') or 'mySalt'
SECURITY_TOKEN_AUTHENTICATION_KEY = 'auth_token'
SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
SECURITY_TOKEN_MAX_AGE = 1800
SECURITY_TRACKABLE = True
SECURITY_RECOVERABLE = True
SECURITY_CONFIRMABLE = False
SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = False
SECURITY_USER_IDENTITY_ATTRIBUTES = 'email'
SECURITY_LOGIN_URL = '/login'
WTF_CSRF_ENABLED = False

# Email
MAIL_SERVER = environ.get('MAIL_SERVER', 'smtp.sendgrid.net')
MAIL_PORT = int(environ.get('MAIL_PORT', '587'))
MAIL_USE_TLS = environ.get('MAIL_USE_TLS', True)
MAIL_USE_SSL = environ.get('MAIL_USE_SSL', False)
MAIL_USERNAME = environ.get('MAIL_USERNAME')
MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = environ.get('MAIL_DEFAULT_SENDER')

# Admin account
ADMIN_PASSWORD = environ.get('ADMIN_PASSWORD', 'password123#')
ADMIN_EMAIL = environ.get('ADMIN_EMAIL', 'admin@example.com')
EMAIL_SUBJECT_PREFIX = f"[{APP_NAME}]"
EMAIL_SENDER = f"{APP_NAME} Admin <{MAIL_USERNAME}>"

SOCIAL_GOOGLE = {
    'consumer_key': "cute.apps.googleusercontent.com",
    'consumer_secret': "password"
}

GRAPHIQL = environ.get('GRAPHIQL', False)

USPS_URL = environ.get('USPS_URL',
                       "https://secure.shippingapis.com/ShippingAPI.dll")
USPS_USERID = environ.get('USPS_USERID')
