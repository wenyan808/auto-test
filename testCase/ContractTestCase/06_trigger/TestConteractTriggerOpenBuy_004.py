#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20210930
# @Author : 
    用例标题
        计划委托买入开多触发价大于最新价
    前置条件
        
    步骤/文本
        1、登录合约交易系统
        2、选择币种BTC，选择杠杆5X，点击开仓-计划按钮
        3、输入触发价（如：50000，最新价：49999）
        4、输入买入价（如：45000）
        5、输入买入量10张
        6、点击买入开多按钮，弹框点击确认
    预期结果
        A)提示下单成功
        B)当前委托-计划委托列表查询创建订单
    优先级
        1
    用例别名
        TestConteractTriggerOpenBuy_004
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
class TestConteractTriggerOpenBuy_004:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol):
        # 撤销当前用户 某个品种所有限价挂单
        ATP.cancel_all_order(symbol=symbol)
        # 修改当前品种杠杆 默认5倍
        ATP.switch_level(symbol=symbol)
        # 清除盘口所有卖单
        ATP.clean_market(symbol=symbol, direction='sell')
        # 清除盘口所有买单
        ATP.clean_market(symbol=symbol
                         , direction='buy')

    @allure.title('计划委托买入开多触发价大于最新价')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
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
        with allure.step('3、输入触发价（如：50000，最新价：49999）'):
            pass
        with allure.step('4、输入买入价（如：45000）'):
            pass
        with allure.step('5、输入买入量10张'):
            pass
        with allure.step('6、点击买入开多按钮，弹框点击确认'):
            r=linear_order.linear_swap_triggerOrder_insert(symbol=symbol,trigger_price=triggerPrice,
                                                         order_price=orderPrice,volume=volume, direction=direction,
                                                         offset=offset,lever_rate=leverRate)
            print(r)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
