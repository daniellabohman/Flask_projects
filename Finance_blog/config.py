import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_default_secret_key_here'  # Update this line
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Risengr0d1@localhost/flaskapp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    
