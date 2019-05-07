'''
Configuration class, contains settings for running the app
'''


secret_key = b'your_secret_key'


class BaseConfig:
	'''
	Base config class
	'''
	DEBUG = True
	TESTING = False
	AVAILABLE_LANGUAGES = ['en', 'ru']


class ProductionConfig(BaseConfig):
	'''
	Production config
	'''
	DEBUG = False


class DevelopmentConfig(BaseConfig):
	'''
	Development config
	'''
	DEBUG = True
	TESTING = True