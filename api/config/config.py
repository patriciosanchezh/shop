import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    SQLALCHEMY_ECHO = False
    JWT_SECRET_KEY = 'JWT-SECRET'
    SECRET_KEY = 'SECRET-KEY'
    SECURITY_PASSWORD_SALT = 'SECRET-KEY-PASSWORD'
    MAIL_DEFAULT_SENDER= '<mail_sender>'
    MAIL_SERVER= '<mail_smtp_host>'
    MAIL_PORT= '<mail_port>'
    MAIL_USERNAME= '<mail_username>'
    MAIL_PASSWORD= '<mail_password>'
    MAIL_USE_TLS= False
    MAIL_USE_SSL= True
    UPLOAD_FOLDER= 'images'


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    SQLALCHEMY_ECHO = False
    JWT_SECRET_KEY = 'JWT-SECRET'
    SECRET_KEY = 'SECRET-KEY'
    SECURITY_PASSWORD_SALT = 'SECRET-KEY-PASSWORD'
    MAIL_DEFAULT_SENDER= '<mail_sender>'
    MAIL_SERVER= '<mail_smtp_host>'
    MAIL_PORT= '<mail_port>'
    MAIL_USERNAME= '<mail_username>'
    MAIL_PASSWORD= '<mail_password>'
    MAIL_USE_TLS= False
    MAIL_USE_SSL= True
    UPLOAD_FOLDER= 'images'
    

    
    
class TestingConfig(Config): 
    TESTING = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/db.sqlite.db'
    SQLALCHEMY_ECHO = False
    JWT_SECRET_KEY = 'JWT-SECRET'
    SECRET_KEY= 'SECRET-KEY'
    SECURITY_PASSWORD_SALT= 'SECRET-KEY-PASSWORD'
    MAIL_DEFAULT_SENDER= '<mail_sender>'
    MAIL_SERVER= '<mail_smtp_host>'
    MAIL_PORT= '<mail_port>'
    MAIL_USERNAME= '<mail_username>'
    MAIL_PASSWORD= '<mail_password>'
    MAIL_USE_TLS= False
    MAIL_USE_SSL= True
    UPLOAD_FOLDER= 'images'
    