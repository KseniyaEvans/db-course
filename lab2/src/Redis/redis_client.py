import redis
import sys
import Redis.config as config


class RedisClient:
    __instance = None

    def __init__(self):
        if not RedisClient.__instance:
            self.__conn = redis.Redis(host=config.Redis.HOST, port=config.Redis.PORT, db=0, decode_responses=True)

    @classmethod
    def get_connection(cls):
        if not cls.__instance:
            cls.__instance = RedisClient()
        return cls.__instance.__conn

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = RedisClient()
        return cls.__instance