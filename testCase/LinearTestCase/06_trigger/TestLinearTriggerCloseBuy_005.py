#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211009
# @Author : 
    用例标题
        计划委托买入平空触发价小于最新价
    前置条件
        
    步骤/文本
        1、登录合约交易系统
        2、选择币种BTC，选择杠杆5X，点击平仓-计划按钮
        3、输入触发价（如：50000，最新价：50500）
        4、输入买入价（如：45000）
        5、输入买入量10张
        6、点击买入平空按钮，弹框点击确认
    预期结果
        A)提示下单成功
        B)当前委托-计划委托列表查询创建订单
    优先级
        1
    用例别名
        TestLinearTriggerCloseBuy_005
"""

from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order
from tool import atp

from pprint import pprint
import pytest, allure, random, time


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('计划委托-平空')  # 这里填功能
@allure.story('最新价高于触发价-刷新最新价-触发')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
class TestLinearTriggerCloseBuy_005:

    @allure.step('前置条件')
    def setup(self):
        contractCode = 'BTC-USDT'
        offset = 'open'
        leverRate = 5
        print("清卖盘》》》》", atp.ATP.clean_market(contract_code='BTC-USDT', direction='sell'))
        print("清买盘》》》》", atp.ATP.clean_market(contract_code='BTC-USDT', direction='buy'))
        print('开仓……')
        linear_api.linear_order(contract_code=contractCode, price='50500', order_price_type='limit',
                                lever_rate=leverRate, direction='buy', offset=offset,
                                volume=1)
        linear_api.linear_order(contract_code=contractCode, price='50500', order_price_type='limit',
                                lever_rate=leverRate, direction='sell', offset=offset,
                                volume=1)
        # 等待成交刷新最新价
        time.sleep(1)

    @allure.title('计划委托买入平空触发价小于最新价')
    @allure.step('测试执行')
    def test_execute(self):
        contractCode = 'BTC-USDT'
        triggerPrice = '50000'
        orderPrice = '45000'
        volume = 1
        direction = 'buy'
        offset = 'close'
        leverRate = 5
        with allure.step('1、登录合约交易系统'):
            pass
        with allure.step('2、选择币种BTC，选择杠杆5X，点击平仓-计划按钮'):
            pass
        with allure.step('3、输入触发价（如：50000，最新价：50500）'):
            pass
        with allure.step('4、输入买入价（如：45000）'):
            pass
        with allure.step('5、输入买入量10张'):
            pass
        with allure.step('6、点击买入平空按钮，弹框点击确认'):
            orderResult = linear_order.linear_swap_triggerOrder_insert(contract_code=contractCode, trigger_type='le',
                                                                       trigger_price=triggerPrice,
                                                                       order_price=orderPrice, volume=volume,
                                                                       direction=direction,
                                                                       offset=offset, lever_rate=leverRate,
                                                                       symbol='BTC')
            print('计划委托下单返回信息 = ',orderResult)
            triggerOrderId = orderResult['data']['order_id']
            print('计划委托单号 = ', triggerOrderId)
            # 单号返回为空则下单失败
            if not triggerOrderId:
                assert False
            pass
        with allure.step('7、刷新最新价，触发计划委托单'):
            contractCode = 'BTC-USDT'
            offset = 'open'
            price = '50000'
            leverRate = 5
            print('刷新最新价……')
            linear_api.linear_order(contract_code=contractCode, price=price, order_price_type='limit',
                                    lever_rate=leverRate, direction='buy', offset=offset,
                                    volume=1)
            linear_api.linear_order(contract_code=contractCode, price=price, order_price_type='limit',
                                    lever_rate=leverRate, direction='sell', offset=offset,
                                    volume=1)
            # 等待成交刷新最新价
            time.sleep(1)

        with allure.step('8、验证计划委托单被触发'):
            triggerOrderHistoryOrders = linear_order.linear_swap_his_triggerorders(contract_code=contractCode,
                                                                                   trade_type=3)
            # print('计划委托7天内买入平空单历史 =',triggerOrderHistoryOrder)
            historySize = triggerOrderHistoryOrders['data']['total_size']
            # 单页只显示10条数据
            if historySize > 10:
                historySize = 10

            i = 0
            while i < int(historySize):
                triggerOrderHistoryOrder = triggerOrderHistoryOrders['data']['orders'][i]['order_id']
                # 循环历史计划委托单，获取测试的计划委托单
                if triggerOrderHistoryOrder == triggerOrderId:
                    # 找到当前测试的计划委托单后，判断他关联的限价单号值不为空，则证明该计划委托单已被触发，并转化限价单成功
                    triggerOrderRelationOrder = triggerOrderHistoryOrders['data']['orders'][i]['relation_order_id']
                    if not triggerOrderRelationOrder:
                        assert False
                    # 在历史记录中找到了该计划委托订单则跳出循环，不再查找
                    break
                i = i + 1
    @allure.step('恢复环境')
    def teardown(self):
        print('\n平仓，清理测试数据')
        linear_api.linear_order(contract_code='BTC-USDT', price='45000', order_price_type='limit', lever_rate=5,
                                direction='buy', offset='close',
                                volume=1)
        linear_api.linear_order(contract_code='BTC-USDT', price='45000', order_price_type='limit', lever_rate=5,
                                direction='sell', offset='close',
                                volume=2)


if __name__ == '__main__':
    pytest.main()
