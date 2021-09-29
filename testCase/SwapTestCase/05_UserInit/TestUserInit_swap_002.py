#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20210929
# @Author : 
    用例标题
        检查用户已开户，个人初始化
    前置条件
        用户已开户
    步骤/文本
        1、进入redis， 删除用户APO数据
           命令    del RsT:APO:user_id#BCH   
        2、进入通用MQ
        2、进入：Exchange: UserProductTriggerInitChannel
        3、手动在MQ中发送个人初始化（注意:user_id需要实际替换成用户的ID）
        {"ETH":{"user_id":"DEL_USER_PRODUCT_APO"}}
        
    预期结果
        发送初始化命令后，查看redis中APO数据，存在该用户APO数据（注意:user_id需要实际替换成用户的ID）
        命令     hgetall RsT:APO:user_id#BCH    
    优先级
        0
    用例别名
        TestUserInit_swap_002
"""

from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order

from pprint import pprint
import pytest, allure, random, time
from common import redisComm
from common.util import api_http_post


@allure.epic('反向永续')  # 这里填业务线
@allure.feature('个人初始化')  # 这里填功能
@allure.story('指定品种')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
class TestUserInit_swap_002:

    @allure.step('前置条件')
    def setup(self):
        print(''' 用户已开户 ''')

    @allure.title('检查用户已开户，个人初始化')
    @allure.step('测试执行')
    def test_execute(self):
        userId = '100000000'
        contractCode = 'BTC'
        host = "172.18.6.243"
        port = 6383
        password = 'rNEAz9uFwHoymy5i'
        r = redisComm.redisConf(host, port, password)
        with allure.step('1、进入redis， 删除用户APO数据'):
            pass
        with allure.step('执行RedisAPO删除> RsT:APO:user_id#BTC   '):
            if r.delAPO(userId, contractCode) == 1:
                print(contractCode+">APO信息删除成功")
            else:
                print(contractCode+">无APO数据")
            pass
        with allure.step('2、进入通用MQ'):
            pass
        with allure.step('2、进入：Exchange: UserProductTriggerInitChannel'):
            pass
        with allure.step('3、手动在MQ中发送个人初始化（注意:user_id需要实际替换成用户的ID）'):
            requestHeaders = {
                "authorization": "Basic Z3Vlc3Q6Z3Vlc3Q=",
                "Accept": "application/json",
                'Content-Type': 'application/json',
                "Accept-language": "zh-CN",
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
            }
            param = {
              "vhost": "/",
              "name": "amq.default",
              "properties": {
                "delivery_mode": 1,
                "headers": {}
              },
              "routing_key": "UserProductTriggerInitChannel",
              "delivery_mode": "1",
              "payload": "{BTC:{100000000:DEL_USER_PRODUCT_APO}}",
              "headers": {},
              "props": {},
              "payload_encoding": "string"
            }
            api_http_post('http://172.18.6.241:15672/api/exchanges/%2F/amq.default/publish', param, add_to_headers=requestHeaders)
            time.sleep(1)
            pass
        with allure.step('进入redis，查看初始化后'+contractCode+'(品种)的APO'):
            if r.keyIsExists(userId, contractCode) == 1:
                print(contractCode+"初始化成功")
            else:
                assert "初始化失败"
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
