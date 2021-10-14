#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211013
# @Author : 
    用例标题
        WS订阅K线(req) 合约代码大小写
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        
    优先级
        2
    用例别名
        TestSwapNoti_ws_kline_146
"""

from common.SwapServiceWS import t as swap_service_ws
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order
from tool import atp
from pprint import pprint
import pytest, allure, random, time


@allure.epic('反向永续')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('WS订阅K线(req) 合约代码大小写')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_ws_kline_146:

    @allure.step('前置条件')
    def setup(self):
        print("\n自动化步骤："
              "\n*、发送req请求from to请求kline ，请求参数中period不传；"
              "\n*、验证Kline 1min返回结果：正常")

    @allure.title('WS订阅K线(req) 合约代码大小写')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step('详见官方文档'):
            contract_codeB = contract_code.split('-')[0]
            contract_codeA = contract_code.split('-')[1]
            self.contract_code = contract_codeB+'-'+contract_codeA.lower()
            self.period = '1min'
            self.toTime = int(time.time())
            self.fromTime = self.toTime - 60 * 3
            subs = {
                "req": "market.{}.kline.{}".format(self.contract_code, self.period),
                "id": "id4",
                "from": self.fromTime,
                "to": self.toTime
            }
            result = swap_service_ws.swap_sub(subs)
            resultStr = '\nKline返回结果 = ' + str(result)
            print('\033[1;32;49m%s\033[0m' % resultStr)
            assert 'ok' in result['status']
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
