import redis


class redisConf:

    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password
        self.coon = redis.Redis(host=self.host, port=self.port, password=self.password, decode_responses=True, db=0)

    def getAPO(self, userId, contractCode):
        key = "RsT:APO:" + userId + "#" + contractCode
        return self.coon.hgetall(key)

    def delAPO(self, userId, contractCode):
        key = "RsT:APO:" + userId + "#" + contractCode
        return self.coon.delete(key)

    def keyIsExists(self, userId, contractCode):
        key = "RsT:APO:" + userId + "#" + contractCode
        return self.coon.exists(key)


# t = redisConf()
# print(t.delAPO('100000000','BTC-USDT'))
