import os


class BaseConfig(object):
    APP_NAME = 'withpano'
    # SERVER_NAME = os.getenv('SERVER_NAME', 'localhost:8023')
    APP_HOST_NAME = os.getenv('APP_HOST_NAME')
    SECRET_KEY = os.getenv('SECRET_KEY', '4aa592fc8883f87ff6d2360983d82529aed2346cfc612f30')
    ENC_PWD = os.getenv('ENC_PWD', 'pan123')
    WTF_CSRF_ENABLED = False
    # MONGODB_SETTINGS = {
    #     "host": f"mongodb://{os.getenv('MONGO_USER', 'admin')}:{os.getenv('MONGO_PWD', 'admin')}@{os.getenv('MONGO_HOSTS', '3.110.192.4:27017')}/{os.getenv('MONGO_DB_NAME', 'withpano_crm_1_0')}?replicaSet={os.getenv('MONGO_REPLICA_SET', 'rs0')}&authSource={os.getenv('MONGO_AUTH_SOURCE', 'admin')}",
    #     "connect": True,
    # }
    APP_URL_PREFIX = os.getenv('APP_URL_PREFIX', '/')
    URL_SCHEME = os.getenv('URL_SCHEME', 'http')
    STATIC_PATH = os.getenv('STATIC_PATH', 'templates/build')
