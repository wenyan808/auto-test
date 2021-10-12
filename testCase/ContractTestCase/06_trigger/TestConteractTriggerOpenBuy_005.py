#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20210930
# @Author : chenwei
    用例标题
        计划委托买入开多触发价小于最新价
    前置条件
        
    步骤/文本
        1、登录合约交易系统
        2、选择币种BTC，选择杠杆5X，点击开仓-计划按钮
        3、输入触发价（如：50000，最新价：50500）
        4、输入买入价（如：45000）
        5、输入买入量10张
        6、点击买入开多按钮，弹框点击确认
    预期结果
        A)提示下单成功
        B)当前委托-计划委托列表查询创建订单
    优先级
        1
    用例别名
        TestConteractTriggerOpenBuy_005
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
@pytest.mark.stable
class TestConteractTriggerOpenBuy_005:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol, symbol_period):
        self.symbol = symbol
        # 清除盘口所有卖单
        print(ATP.clean_market(contract_code=symbol_period, direction='sell'))
        time.sleep(2)
        # 清除盘口所有买单
        print(ATP.clean_market(contract_code=symbol_period, direction='buy'))

        print(ATP.switch_level(contract_code=symbol_period))

        r = contract_api.contract_cancelall(symbol=symbol)
        pprint(r)
        r = contract_api.contract_tpsl_cancelall(symbol=symbol)
        pprint(r)
        r = contract_api.contract_trigger_cancelall(symbol=symbol)
        pprint(r)
        r = contract_api.contract_cancelall(symbol=symbol)
        pprint(r)
        time.sleep(2)

    @allure.title('计划委托买入开多触发价小于最新价')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        self.symbol = symbol
        volume = 10
        direction = 'buy'
        offset = 'open'
        leverRate = 5
        trigger_type = "le"
        contract_type = "this_week"
        print('\n步骤一:获取最近价\n')
        r = contract_api.contract_history_trade(symbol=symbol_period, size='1')
        pprint(r)
        lastprice = r['data'][0]['data'][0]['price']
        # print(lastprice)
        triggerPrice = round((lastprice * 0.98), 1)
        orderPrice = round((lastprice * 0.9), 1)
        with allure.step('1、登录合约交易系统'):
            pass
        with allure.step('2、选择币种BTC，选择杠杆5X，点击开仓-计划按钮'):
            pass
        with allure.step('3、输入触发价（如：50000，最新价：50500）'):
            pass
        with allure.step('4、输入买入价（如：45000）'):
            pass
        with allure.step('5、输入买入量10张'):
            pass
        with allure.step('6、点击买入开多按钮，弹框点击确认'):
            r = contract_order.contract_triggerorder_insert(symbol=symbol, trigger_type=trigger_type,
                                                            trigger_price=triggerPrice, contract_type=contract_type,
                                                            order_price=orderPrice, volume=volume, direction=direction,
                                                            offset=offset, lever_rate=leverRate)
            print(r)
            order_id = r['data']['order_id']
            print(order_id)
            time.sleep(2)
            r = contract_order.contract_open_triggerorders(symbol=symbol)
            print(r)
            orders_id = r['data']['orders'][0]['order_id']
            assert order_id == orders_id

    @allure.step('恢复环境')
    def teardown(self):
        contract_order.contract_triggerorder_cancelall(symbol=self.symbol)
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
