#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/10/18
# @Author  : Alex Li
"""
所属分组
    合约测试基线用例//01 反向交割//09 订单推送
用例标题
    订阅持仓变动（无持仓变动）    
前置条件
    
步骤/文本
    成功建立和 WebSocket API 的连接之后，向server发送数据订阅，数据格式参考文档：https://docs.huobigroup.com/docs/dm/v1/cn/#websocket-5

预期结果
    订阅成功，返回'err-code': 0，订阅成功之后无新的推送
优先级
    0
"""

import pytest
import allure
from tool.atp import ATP
from common.ContractServiceWS import t as contract_service_ws


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('订单推送')  # 这里填功能
@allure.story('订阅持仓变动（无持仓变动）')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : 柳攀峰')
@pytest.mark.stable
class TestContractNotification_001:

    @allure.step('前置条件:非colo域名')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol):
        print("前置条件  {}".format(symbol))

    @allure.title('订阅持仓变动（无持仓变动）')
    @allure.step('测试执行')
    def test_execute(self, symbol):
        symbol = 'BTC'
        with allure.step('1、订阅持仓变动（无持仓变动）'):
            subs = {
                "op": "sub",
                "cid": 11538447,
                "topic": "positions.{}".format(symbol)
            }
            result = contract_service_ws.contract_notification(subs)
            print(result)
            assert result["op"] == 'notify'

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
