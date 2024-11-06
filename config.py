import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")  
    SQLALCHEMY_TRACK_MODIFICATIONS = False       

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db' 

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

# Dictionary to easily access configurations by name
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
