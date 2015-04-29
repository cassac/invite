import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = BASE_DIR + '/app/static/uploads'

class BaseConfig(object):
	'Base configuration class'
	DEBUG = False
	TESTING = False
	SECRET_KEY = open(BASE_DIR + '/' + 'opensesame.txt').read()[0]

	@staticmethod
	def init_app(app):
		pass

class ProductionConfig(BaseConfig):
	'Production specific configuration'
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = 'sqlite:///production.db'

class StagingConfig(BaseConfig):
	'Staging specific configuration'
	DEBUG = True
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///staging.db'

class DevelopmentConfig(BaseConfig):
	'Development environment specific configuration'
	DEBUG = True
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'

email_config = {
## EMAIL SETTINGS
	'MAIL_DEBUG': True,
	'MAIL_SERVER':'smtp.gmail.com',
	'MAIL_PORT':465,
	'MAIL_USE_SSL':True,
	'MAIL_USERNAME': open(BASE_DIR + '/' + 'opensesame.txt').read().splitlines()[1],
	'MAIL_PASSWORD': open(BASE_DIR + '/' + 'opensesame.txt').read().splitlines()[2],
	'MAIL_SUPPRESS_SEND':False,
	'TESTING': False
}

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

