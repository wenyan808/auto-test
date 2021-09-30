#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20210929
# @Author : 
    用例标题
        计划委托买入开多
    前置条件
        
    步骤/文本
        1、登录合约交易系统
        2、选择币种BTC，选择杠杆5X，点击开仓-计划按钮
        3、输入触发价（如：50000）
        4、输入买入价（如：49800）
        5、输入买入量10张
        6、点击买入开多按钮
    预期结果
        A)弹框显示计划委托买入开多详情信息
    优先级
        0
    用例别名
        TestLinearTriggerOpenBuy_001
"""

from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order

from pprint import pprint
import pytest, allure, random, time


@allure.epic('业务线')  # 这里填业务线
@allure.feature('功能')  # 这里填功能
@allure.story('子功能')  # 这里填子功能，没有的话就把本行注释掉
class TestLinearTriggerOpenBuy_001:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('计划委托买入开多')
    @allure.step('测试执行')
    def test_execute(self):
        contractCode = 'BTC-USDT'
        triggerPrice = 50000
        orderPrice = 49800
        volume = 10
        direction = 'buy'
        offset = 'open'
        leverRate = 5
        with allure.step('1、登录合约交易系统'):
            pass
        with allure.step('2、选择币种BTC，选择杠杆5X，点击开仓-计划按钮'):
            pass
        with allure.step('3、输入触发价（如：50000）'):
            pass
        with allure.step('4、输入买入价（如：49800）'):
            pass
        with allure.step('5、输入买入量10张'):
            pass
        with allure.step('6、点击买入开多按钮'):
            r=linear_order.linear_swap_triggerOrder_insert(contract_code=contractCode,trigger_price=triggerPrice,
                                                         order_price=orderPrice,volume=volume, direction=direction,
                                                         offset=offset,lever_rate=leverRate)
            print(r)
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()