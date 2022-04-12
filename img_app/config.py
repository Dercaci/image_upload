from distutils.debug import DEBUG
import os


class Configuration(object):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')


    