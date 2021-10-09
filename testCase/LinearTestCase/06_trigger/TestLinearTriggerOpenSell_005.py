#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20210929
# @Author : YuHuiQing
    用例标题
        计划委托买入开空
    前置条件
        
    步骤/文本
        1、行情-最新价更新为50500；
        2、计划委托下单，触发价为50000；买入开空价为55000；
        3、行情-最新价更新；使最新价达到50000价，触发计划委托单转换为限制单；
    预期结果
        A)计划委托单下单成功；
        B)达到触发价，计划委托转成限价单；
    优先级
        0
    用例别名
        TestLinearTriggerOpenSell_005
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
@allure.feature('计划委托下单-开空')  # 这里填功能
@allure.story('最新价高于触发价-刷新最新价-触发')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
class TestLinearTriggerOpenSell_005:

    @allure.step('前置条件')
    def setup(self):
        print("清卖盘》》》》", atp.ATP.clean_market(contract_code='BTC-USDT', direction='sell'))
        print("清买盘》》》》", atp.ATP.clean_market(contract_code='BTC-USDT', direction='buy'))

    @allure.title('计划委托买入开多')
    @allure.step('测试执行')
    def test_execute(self):
        contractCode = 'BTC-USDT'
        curlimitPrice = '50500'
        triggerPrice = '50000'
        orderPrice = '55000'
        volume = 10
        direction = 'sell'
        offset = 'open'
        leverRate = 5
        with allure.step('1、行情-最新价更新为'+curlimitPrice):
            linear_api.linear_order(contract_code=contractCode,price=curlimitPrice,order_price_type='limit',lever_rate=5,direction='buy',offset=offset,
                                    volume=1,)
            linear_api.linear_order(contract_code=contractCode, price=curlimitPrice,order_price_type='limit', lever_rate=5,direction='sell', offset=offset,
                                    volume=1, )
            # 等待成交刷新最新价
            time.sleep(1)
            pass
        with allure.step('2、计划委托下单，触发价为'+triggerPrice+'；开空卖出价为'+orderPrice+'；'):
            orderResult = linear_order.linear_swap_triggerOrder_insert(contract_code=contractCode,trigger_type='le', trigger_price=triggerPrice,
                                                             order_price=orderPrice, volume=volume, direction=direction,
                                                             offset=offset, lever_rate=leverRate,symbol='BTC')
            triggerOrderId = orderResult['data']['order_id']
            print('计划委托单号 = ', triggerOrderId)
            # 单号返回为空则下单失败
            if not triggerOrderId:
                assert False
            pass
        with allure.step('3、行情-最新价更新；使最新价达到'+triggerPrice+'价，触发计划委托单转换为限制单'):
            linear_api.linear_order(contract_code=contractCode, price=triggerPrice, order_price_type='limit', lever_rate=5,
                                    direction='buy', offset=offset,
                                    volume=1, )
            linear_api.linear_order(contract_code=contractCode, price=triggerPrice, order_price_type='limit', lever_rate=5,
                                    direction='sell', offset=offset,
                                    volume=1, )
            time.sleep(1)# 等待成交刷新最新价，验证限价单被触发
            pass
        with allure.step('4、验证计划委托单被触发'):
            triggerOrderHistoryOrder = linear_order.linear_swap_his_triggerorders(contract_code=contractCode,
                                                                                  trade_type=3)
            # print('计划委托7天内买入平空单历史 =',triggerOrderHistoryOrder)
            historySize = triggerOrderHistoryOrder['data']['total_size']
            i = 0
            while i < int(historySize):
                # 循环历史计划委托单，获取测试的计划委托单
                if triggerOrderHistoryOrder['data']['orders'][i]['order_id'] == triggerOrderId:
                    # 找到当前测试的计划委托单后，判断他关联的限价单号值不为空，则证明该计划委托单已被触发，并转化限价单成功
                    if not triggerOrderHistoryOrder['data']['orders'][i]['relation_order_id']:
                        assert False
                i = i + 1
            pass
    @allure.step('恢复环境')
    def teardown(self):
        triggerOrder = '50000'
        print('恢复环境操作：撤销转换的限价单；平掉用户所有的持仓数据')
        linear_order.linear_swap_selection_cancel(contract_code='BTC-USDT')
        time.sleep(1)
        linear_api.linear_order(contract_code='BTC-USDT', price= triggerOrder, order_price_type='limit', lever_rate=5,
                                direction='buy', offset='close',
                                volume=2 )
        linear_api.linear_order(contract_code='BTC-USDT', price= triggerOrder, order_price_type='limit', lever_rate=5,
                                direction='sell', offset='close',
                                volume=2 )
        time.sleep(1)

if __name__ == '__main__':
    pytest.main()
