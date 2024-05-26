import uuid

class Config:
    SECRET_KEY = uuid.uuid4().hex

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "hd_tu_08"
    MYSQL_DB = "logins"

config = {
    'development': DevelopmentConfig
}