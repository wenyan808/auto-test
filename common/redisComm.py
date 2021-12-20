import redis
from config.conf import REDIS_CONF

class redisConf:

    redisClient = None

    def __init__(self,redisName):
        try:
            redisConfig = eval(REDIS_CONF)
            self.host = str(redisConfig[redisName]['host'])
            self.port = int(redisConfig[redisName]['port'])
            self.password = str(redisConfig[redisName]['pwd'])
            self.redisClient = redis.Redis(host=self.host, port=self.port, password=self.password, max_connections=10,
                                           decode_responses=True, db=0)
        except Exception as e:
            print(f'Redis执行异常={str(e)}')

    def instance(self):
        if self.redisClient is None:
            self.redisClient = redis.Redis(host=self.host, port=self.port, password=self.password, max_connections=10,
                                           decode_responses=True, db=0)
        return self.redisClient

    def __del__(self):
        try:
            print("REDIS CONN DESTRUCTOR")
            self.redisClient.close()
        except Exception as e:
            print(e)





