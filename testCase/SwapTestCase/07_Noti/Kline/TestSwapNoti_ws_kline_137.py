#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211014
# @Author : 
    用例标题
        WS订阅K线(req) 1mon 合约不存在
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        
    优先级
        3
    用例别名
        TestSwapNoti_ws_kline_137
"""

from common.SwapServiceWS import t as swap_service_ws
import pytest, allure, random, time


@allure.epic('反向永续')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('WS订阅K线(req) 1mon 合约不存在')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_ws_kline_137:

    @allure.step('前置条件')
    def setup(self):
        print("\n自动化步骤："
              "\n*、发送req请求from to请求kline ，请求参数中合约不存在；"
              "\n*、验证Kline 1mon返回结果；invalid topic")

    @allure.title('WS订阅K线(req) 1mon 合约不存在')
    @allure.step('测试执行')
    def test_execute(self):
        with allure.step('详见官方文档'):
            self.contract_code = 'BTC-BTC'  # 不存在的合约
            self.period = '1mon'
            self.toTime = int(time.time())
            self.fromTime = self.toTime - 60 * 60 * 24 * 30 * 12
            subs = {
                "req": "market.{}.kline.{}".format(self.contract_code, self.period),
                "id": "id4",
                "from": self.fromTime,
                "to": self.toTime
            }
            result = swap_service_ws.swap_sub(subs)
            resultStr = '\nKline返回结果 = ' + str(result)
            print('\033[1;32;49m%s\033[0m' % resultStr)
            assert 'invalid topic' in result['err-msg']
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
