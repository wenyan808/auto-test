#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211013
# @Author : 
    用例标题
        WS订阅K线(sub) 合约代码为空
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        
    优先级
        3
    用例别名
        TestLinearNoti_ws_kline_079
"""

from common.LinearServiceWS import t as linear_service_ws
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
import pytest, allure, random, time
from tool.atp import ATP


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('WS订阅K线(sub) 合约代码为空')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestLinearNoti_ws_kline_079:

    @allure.step('前置条件')
    def setup(self):
        print("\n自动化步骤："
              "\n*、WS订阅K线(sub) 合约代码为空；"
              "\n*、验证Kline请求返回结果；报错invalid topic")

    @allure.title('WS订阅K线(sub) 合约代码为空')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step('详见官方文档'):
            self.contract_code = ''
            self.period = '1min'
            subs = {
                "sub": "market.{}.kline.{}".format(self.contract_code, self.period),
                "id": "id1"
            }
            result = linear_service_ws.linear_sub(subs)
            resultStr = '\nWS返回结果 = ' + str(result)
            print('\033[1;32;49m%s\033[0m' % resultStr)
            # 请求topic校验
            assert 'invalid topic' in result['err-msg']
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
