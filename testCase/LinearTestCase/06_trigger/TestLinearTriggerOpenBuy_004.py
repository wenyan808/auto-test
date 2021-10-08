#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20210929
# @Author : YuHuiQing
    用例标题
        计划委托买入开多
    前置条件
        
    步骤/文本
        1、行情-最新价更新为49800；
        2、计划委托下单，触发价为50000；买入价为49800；
        3、行情-最新价更新；使最新价达到50000价，触发计划委托单转换为限制单；
    预期结果
        A)计划委托单下单成功；
        B)达到触发价，计划委托转成限价单；
    优先级
        0
    用例别名
        TestLinearTriggerOpenBuy_004
"""

from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order

from pprint import pprint
import pytest, allure, random, time
from tool import atp

@allure.epic('正向永续')  # 这里填业务线
@allure.feature('计划委托下单')  # 这里填功能
@allure.story('下单成功')  # 这里填子功能，没有的话就把本行注释掉
class TestLinearTriggerOpenBuy_004:

    @allure.step('前置条件')
    def setup(self):
        print("清卖盘》》》》", atp.ATP.clean_market(contract_code='BTC-USDT', direction='sell'))
        print("清买盘》》》》", atp.ATP.clean_market(contract_code='BTC-USDT', direction='buy'))

    @allure.title('计划委托买入开多')
    @allure.step('测试执行')
    def test_execute(self):
        contractCode = 'BTC-USDT'
        triggerPrice = '50000'
        orderPrice = '49800'
        volume = 10
        direction = 'buy'
        offset = 'open'
        leverRate = 5
        with allure.step('1、行情-最新价更新为49800'):
            linear_api.linear_order(contract_code=contractCode,price='49800',order_price_type='limit',lever_rate=5,direction='buy',offset=offset,
                                    volume=1,)
            time.sleep(0.3)
            linear_api.linear_order(contract_code=contractCode, price='49800',order_price_type='limit', lever_rate=5,direction='sell', offset=offset,
                                    volume=1, )
            # 等待成交刷新最新价
            time.sleep(0.3)
            print("》》》》》》》》》》》》》》1、最新价更新为49800")
            pass
        with allure.step('2、计划委托下单，触发价为50000；买入价为49800；'):
            orderResult = linear_order.linear_swap_triggerOrder_insert(contract_code=contractCode,trigger_type='ge', trigger_price=triggerPrice,
                                                             order_price=orderPrice, volume=volume, direction=direction,
                                                             offset=offset, lever_rate=leverRate,symbol='BTC')
            print(orderResult)
            print("》》》》》》》》》》》》》》2、计划委托单下单成功，触发价为50000")
            time.sleep(0.5)
            # 下单成功后，验证计划委托单成功
            orderInfo = linear_order.linear_swap_open_triggerorders(contract_code=contractCode, trade_type=1)
            print(orderInfo)
            if orderResult['data']['order_id'] == orderInfo['data']['orders'][0]['order_id']:
                print("》》》》》》》》》》》》》》计划委托单下单验证通过")
            else:
                assert False
            pass
        with allure.step('3、行情-最新价更新；使最新价达到50000价，触发计划委托单转换为限制单'):
            linear_api.linear_order(contract_code=contractCode, price='50000', order_price_type='limit', lever_rate=5,
                                    direction='buy', offset=offset,
                                    volume=1, )
            time.sleep(0.3)
            linear_api.linear_order(contract_code=contractCode, price='50000', order_price_type='limit', lever_rate=5,
                                    direction='sell', offset=offset,
                                    volume=1, )
            print("》》》》》》》》》》》》》》3、行情-最新价更新；使最新价达到50000价，触发计划委托单转换为限制单")
            time.sleep(0.5)# 等待成交刷新最新价，验证限价单被触发
            triggerOrder = linear_order.linear_swap_open_triggerorders(contract_code=contractCode)
            time.sleep(0.3)
            print(">>>>>>>>>>>>>>>>>>>计划委托单", triggerOrder)
            if len(triggerOrder['data']['orders']) == 0:
                print("计划委托订单已触发")
            else:
                assert False

            limitOrder = linear_order.linear_swap_openorders(contract_code=contractCode)
            time.sleep(0.3)
            print(">>>>>>>>>>>>>>>>>>>限价单：", limitOrder)
            if len(limitOrder['data']['orders']) != 0:
                print("计划委托订单已触发")
            else:
                assert False
            pass
        with allure.step('4、下单使触发后的限价单成交'):
            linear_api.linear_order(contract_code=contractCode, price='49800', order_price_type='limit', lever_rate=5,
                                    direction='sell', offset=offset,
                                    volume=10)
            pass
    @allure.step('恢复环境')
    def teardown(self):
        print('恢复环境操作：平掉用户所有的持仓数据')
        linear_api.linear_order(contract_code='BTC-USDT', price='49800', order_price_type='limit', lever_rate=5,
                                direction='buy', offset='close',
                                volume=12 )
        time.sleep(1)
        linear_api.linear_order(contract_code='BTC-USDT', price='49800', order_price_type='limit', lever_rate=5,
                                direction='sell', offset='close',
                                volume=12 )

if __name__ == '__main__':
    pytest.main()
