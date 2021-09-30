#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20210930
# @Author : chenwei
    用例标题
        计划委托买入开多未输入触发价
    前置条件
        
    步骤/文本
        1、登录合约交易系统
        2、选择币种BTC，选择杠杆5X，点击开仓-计划按钮
        3、不输入触发价
        4、输入买入价（如：45000）
        5、输入买入量10张
        6、点击买入开多按钮
    预期结果
        A)输入框提示请输入触发价
        
    优先级
        2
    用例别名
        TestLinearTriggerOpenBuy_007
"""

from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order

from pprint import pprint
import pytest, allure, random, time
from tool.atp import ATP

@allure.epic('业务线')  # 这里填业务线
@allure.feature('功能')  # 这里填功能
@allure.story('子功能')  # 这里填子功能，没有的话就把本行注释掉
class TestLinearTriggerOpenBuy_007:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, contract_code):
        # 撤销当前用户 某个品种所有限价挂单
        ATP.cancel_all_order(contract_code=contract_code)
        # 修改当前品种杠杆 默认5倍
        ATP.switch_level(contract_code=contract_code)
        # 清除盘口所有卖单
        ATP.clean_market(contract_code=contract_code, direction='sell')
        # 清除盘口所有买单
        ATP.clean_market(contract_code=contract_code, direction='buy')

    @allure.title('计划委托买入开多未输入触发价')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        orderPrice = 49800
        volume = 10
        direction = 'buy'
        offset = 'open'
        leverRate = 5
        with allure.step('1、登录合约交易系统'):
            pass
        with allure.step('2、选择币种BTC，选择杠杆5X，点击开仓-计划按钮'):
            pass
        with allure.step('3、不输入触发价'):
            pass
        with allure.step('4、输入买入价（如：45000）'):
            pass
        with allure.step('5、输入买入量10张'):
            pass
        with allure.step('6、点击买入开多按钮'):
            r = linear_order.linear_swap_triggerOrder_insert(contract_code=contract_code, trigger_price="",
                                                             order_price=orderPrice, volume=volume, direction=direction,
                                                             offset=offset, lever_rate=leverRate)
            print(r)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
