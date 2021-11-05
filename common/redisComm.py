import redis
from config.conf import REDIS_CONF

class redisConf:

    def __init__(self,redisName):
        redisConfig = eval(REDIS_CONF)
        self.host = str(redisConfig[redisName]['host'])
        self.port = int(redisConfig[redisName]['port'])
        self.password = str(redisConfig[redisName]['pwd'])
        self.coon = redis.Redis(host=self.host, port=self.port, password=self.password, decode_responses=True, db=0)

    def getKey(self,key):
        values = self.coon.hgetall(key)
        return  values





