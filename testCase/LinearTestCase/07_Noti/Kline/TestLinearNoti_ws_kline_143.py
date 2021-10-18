#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211014
# @Author : 
    用例标题
        WS订阅K线(req) 不传合约代码
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        
    优先级
        2
    用例别名
        TestLinearNoti_ws_kline_143
"""

from common.LinearServiceWS import t as linear_service_ws
import pytest, allure, random, time


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('WS订阅K线(req) 1mon 不传合约代码')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestLinearNoti_ws_kline_143:

    @allure.step('前置条件')
    def setup(self):
        print("\n自动化步骤："
              "\n*、发送req请求from to请求kline ，请求参数，不传合约代码；"
              "\n*、验证Kline 1mon返回结果；invalid topic")

    @allure.title('WS订阅K线(req) 不传合约代码')
    @allure.step('测试执行')
    def test_execute(self):
        with allure.step('详见官方文档'):
            self.period = '1min'
            self.toTime = int(time.time())
            self.fromTime = self.toTime - 60 * 60 * 10
            subs = {
                "req": "market.kline.{}".format( self.period),
                "id": "id4",
                "from": self.fromTime,
                "to": self.toTime
            }
            result = linear_service_ws.linear_sub(subs)
            resultStr = '\nKline返回结果 = ' + str(result)
            print('\033[1;32;49m%s\033[0m' % resultStr)
            assert 'invalid topic' in result['err-msg']
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()