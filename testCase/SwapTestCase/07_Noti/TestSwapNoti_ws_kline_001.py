#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211012
# @Author : 
    用例标题
        WS订阅K线(sub) 1min
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        id、open、close、low、high价格正确；amount、vol、count值正确,不存在Null,[]
    优先级
        0
    用例别名
        TestSwapNoti_ws_kline_001
"""

from common.SwapServiceWS import t as swap_service_ws
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order
from tool import atp
from pprint import pprint
import pytest, allure, random, time


@allure.epic('反向永续')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('WS订阅K线(sub) 1min')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_ws_kline_001:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, contract_code, lever_rate, offsetO, offsetC, directionB, directionS):
        print("\n自动化步骤："
              "\n*、先执行两笔成交，更新K线数据；"
              "\n*、再发送请求kline 1min的请求；"
              "\n*、验证Kline 1min返回结果；各返回值不为空[]")
        print("\n清盘》》》》", atp.ATP.clean_market())
        self.contract_code = contract_code
        self.lever_rate = lever_rate
        self.offsetO = offsetO
        self.offsetC = offsetC
        self.directionB = directionB
        self.directionS = directionS
        self.order_price_type = 'limit'
        self.currentPrice = atp.ATP.get_current_price()  # 最新价
        self.lowPrice = round(self.currentPrice * 0.99, 2)  # 买入价
        self.highPrice = round(self.currentPrice * 1.01, 2)  # 触发价
        print('进行2笔交易，更新Kline数据')
        swap_api.swap_order(contract_code=self.contract_code, price=self.lowPrice,
                            order_price_type=self.order_price_type,
                            lever_rate=self.lever_rate, direction=self.directionB, offset=self.offsetO, volume=1)

        swap_api.swap_order(contract_code=self.contract_code, price=self.lowPrice,
                            order_price_type=self.order_price_type,
                            lever_rate=self.lever_rate, direction=self.directionS, offset=self.offsetO, volume=1)
        # 等待成交刷新最新价
        time.sleep(1)
        swap_api.swap_order(contract_code=self.contract_code, price=self.highPrice,
                            order_price_type=self.order_price_type,
                            lever_rate=self.lever_rate, direction=self.directionB, offset=self.offsetO, volume=1)

        swap_api.swap_order(contract_code=self.contract_code, price=self.highPrice,
                            order_price_type=self.order_price_type,
                            lever_rate=self.lever_rate, direction=self.directionS, offset=self.offsetO, volume=1)

    @allure.title('WS订阅K线(sub) 1min')
    @allure.step('测试执行')
    def test_execute(self):
        with allure.step('详见官方文档'):
            self.period = '1min'
            subs = {
                "sub": "market.{}.kline.{}".format(self.contract_code, self.period),
                "id": "id1"
            }
            tryTimes = 1
            while True:
                result = swap_service_ws.swap_sub(subs)
                resultStr = '\nKline返回结果 = ' + str(result)
                print('\033[1;32;49m%s\033[0m' % resultStr)
                # 由于Kline可能更新有点慢，等1秒，再执行一次获取结果；避免失败用例造成死循环；这里重试5次
                if 'tick' in result:
                    break
                else:
                    # 超过5次，跳过循环
                    if tryTimes > 5:
                        break
                    else:
                        tryTimes = tryTimes +1
                        time.sleep(1)
                        print('k线未返回预期数据，等待1秒，第', tryTimes - 1, '次重试………………')
            # 请求topic校验
            assert result['ch'] == "market."+self.contract_code+".kline."+self.period
            # 开仓价校验，不为空
            assert result['tick']['open'] is not None
            # 收仓价校验
            assert result['tick']['close'] is not None
            # 最低价校验,不为空
            assert result['tick']['low'] is not None
            # 最高价校验,不为空
            assert result['tick']['high'] is not None
            # 币的成交量
            assert result['tick']['amount'] > 0
            # 成交量张数。 值是买卖双边之和
            assert result['tick']['vol'] >= 4
            # 成交笔数。 值是买卖双边之和
            assert result['tick']['count'] >= 2
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
