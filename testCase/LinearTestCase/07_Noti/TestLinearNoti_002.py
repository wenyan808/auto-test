#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211009
# @Author : 
    用例标题
        WS订阅深度(150档不合并，即传参step0)
    前置条件
        
    步骤/文本
        WS订阅深度(150档不合并，即传参step0)，可参考文档：https://docs.huobigroup.com/docs/usdt_swap/v1/cn/#websocket-3
    预期结果
        asks,bids 数据正确,不存在Null,[]
    优先级
        0
    用例别名
        TestLinearNoti_002
"""

from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.LinearServiceWS import t as linear_service_ws
import pytest, allure, random, time
from tool.atp import  ATP

@allure.epic('正向永续')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('WS订阅深度(150档不合并，即传参step0)')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestLinearNoti_002:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, contract_code, lever_rate, offsetO, directionB, directionS):
        self.lever_rate = lever_rate
        self.contract_code = contract_code
        self.order_price_type = 'limit'
        self.offsetO = offsetO
        self.currentPrice = ATP.get_current_price()  # 最新价
        self.lowPrice = round(self.currentPrice * 0.99, 2)  # 买入价
        self.highPrice = round(self.currentPrice * 1.01, 2)  # 触发价
        self.directionB = directionB
        self.directionS = directionS
        ATP.common_user_make_order(price=self.lowPrice, direction='buy')
        ATP.common_user_make_order(price=self.highPrice, direction='sell')
        # 等待深度更新
        time.sleep(3)
    @allure.title('WS订阅深度(150档不合并，即传参step0)')
    @allure.step('测试执行')
    def test_execute(self):
        with allure.step('WS订阅深度(150档不合并，即传参step0)，可参考文档：https://docs.huobigroup.com/docs/usdt_swap/v1/cn/#websocket-3'):
            self.depthType = 'step0'
            subs = {
                "sub": "market.{}.depth.{}".format(self.contract_code, self.depthType),
                "id": "id5"
            }
            tryTimes = 1
            while True:
                result = linear_service_ws.linear_sub(subs)
                resultStr = '\nDepth返回结果 = ' + str(result)
                print('\033[1;32;49m%s\033[0m' % resultStr)
                # 由于Kline可能更新有点慢，等1秒，再执行一次获取结果；避免失败用例造成死循环；这里重试5次
                if 'tick' in result:
                    break
                else:
                    # 超过5次，跳过循环
                    if tryTimes > 5:
                        break
                    else:
                        tryTimes = tryTimes + 1
                        time.sleep(1)
                        print('k线未返回预期数据，等待1秒，第', tryTimes - 1, '次重试………………')
            # 请求topic校验
            assert result['ch'] == "market." + self.contract_code + ".depth." + self.depthType
            assert result['tick']['bids'] is not None , 'bids为空'
            assert result['tick']['asks'] is not None , 'asks为空'
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print("")
if __name__ == '__main__':
    pytest.main()
