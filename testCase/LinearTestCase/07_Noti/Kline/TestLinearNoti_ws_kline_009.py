#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211013
# @Author : 
    用例标题
        WS订阅K线(sub) 1mon
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        id、open、close、low、high价格正确；amount、vol、count值正确,不存在Null,[]
    优先级
        0
    用例别名
        TestLinearNoti_ws_kline_009
"""

from common.LinearServiceWS import t as linear_service_ws
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
import pytest, allure, random, time
from tool.atp import ATP


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('WS订阅K线(sub) 1mon')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestLinearNoti_ws_kline_009:

    @allure.step('前置条件')
    def setup(self):
        print("\n自动化步骤："
              "\n*、发送请求kline 1mon的请求；"
              "\n*、验证Kline 1mon返回结果；各返回值不为空[]")

    @allure.title('WS订阅K线(sub) 1mon')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step('详见官方文档'):
            self.contract_code = contract_code
            self.period = '1mon'
            subs = {
                "sub": "market.{}.kline.{}".format(self.contract_code, self.period),
                "id": "id1"
            }
            tryTimes = 1
            while True:
                result = linear_service_ws.linear_sub(subs)
                resultStr = '\nWS返回结果 = ' + str(result)
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
                        print('WS未返回预期数据，等待1秒，第', tryTimes - 1, '次重试………………')
            # 请求topic校验
            assert result['ch'] == "market." + self.contract_code + ".kline." + self.period
            # 开仓价校验，不为空
            assert result['tick']['open'] is not None
            # 收仓价校验
            assert result['tick']['close'] is not None
            # 最低价校验,不为空
            assert result['tick']['low'] is not None
            # 最高价校验,不为空
            assert result['tick']['high'] is not None
            # 币的成交量
            assert result['tick']['amount'] >= 0
            # 成交量张数。 值是买卖双边之和
            assert result['tick']['vol'] >= 0
            # 成交笔数。 值是买卖双边之和
            assert result['tick']['count'] >= 0
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
