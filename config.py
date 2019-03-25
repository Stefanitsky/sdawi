'''
Configuration class, contains settings for running the app
'''


class BaseConfig:
	'''
	Base config class
	'''
	DEBUG = True
	TESTING = False


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