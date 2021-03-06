#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211008
# @Author : YuHuiQing
    用例标题
        请求K线(传参from,to)
    前置条件
        
    步骤/文本
        请求K线(传参from,to)，可参考文档：https://docs.huobigroup.com/docs/usdt_swap/v1/cn/#websocket-3
    预期结果
        id、open、close、low、high价格正确；amount、vol、count值正确,不存在Null,[]
    优先级
        
    用例别名
        restful请求
"""

import allure
import pytest
import time

from common.LinearServiceAPI import t as linear_api
from common.LinearServiceWS import t as linear_service_ws
import pytest, allure, random, time
from tool.atp import  ATP


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('请求K线(传参from,to)')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestLinearNoti_001:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self,contract_code,lever_rate,offsetO,directionB,directionS):
        print("\n自动化步骤："
              "\n*、先执行两笔成交，更新K线数据；"
              "\n*、再发送req请求from（now - 1分钟） to(now)kline 1min的请求；"
              "\n*、验证Kline 1min返回结果；各返回值不为空[]")
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
        ATP.common_user_make_order(price=self.lowPrice, direction='sell')
        ATP.common_user_make_order(price=self.highPrice, direction='buy')
        ATP.common_user_make_order(price=self.highPrice, direction='sell')

    @allure.title('请求K线(传参from,to)')
    @allure.step('测试执行')
    def test_execute(self):
        with allure.step('1、订阅Kline获取订阅结果'):
            self.period = '1min'
            self.toTime = int(time.time())
            self.fromTime = self.toTime - 60 * 3
            subs = {
                "req": "market.{}.kline.{}".format(self.contract_code, self.period),
                "id": "id1",
                "from": self.fromTime,
                "to": self.toTime
            }
            tryTimes = 1
            while True:
                result = linear_service_ws.linear_sub(subs)
                resultStr = '\nKline返回结果 = ' + str(result)
                print('\033[1;32;49m%s\033[0m' % resultStr)
                # 由于Kline可能更新有点慢，等1秒，再执行一次获取结果；避免失败用例造成死循环；这里重试5次
                if 'data' in result:
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
            assert result['rep'] == "market." + self.contract_code + ".kline." + self.period
            # 返回的data数量
            c = 0
            while c < len(result['data']):
                # 开仓价校验，不为空
                assert result['data'][c]['open'] is not None
                # 收仓价校验
                assert result['data'][c]['close'] is not None
                # 最低价校验,不为空
                assert result['data'][c]['low'] is not None
                # 最高价校验,不为空
                assert result['data'][c]['high'] is not None
                # 币的成交量
                assert result['data'][c]['amount'] >= 0
                # 成交量张数。 值是买卖双边之和
                assert result['data'][c]['vol'] >= 0
                # 成交笔数。 值是买卖双边之和
                assert result['data'][c]['count'] >= 0
                c = c + 1
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
