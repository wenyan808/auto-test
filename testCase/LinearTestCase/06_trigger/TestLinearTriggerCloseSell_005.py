#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211009
# @Author : 
    用例标题
        计划委托卖出平多触发价小于最新价
    前置条件
        
    步骤/文本
        1、登录合约交易系统
        2、选择币种BTC，选择杠杆5X，点击平仓-计划按钮
        3、输入触发价（如：50000，最新价：50500）
        4、输入卖出价（如：55000）
        5、输入卖出量10张
        6、点击卖出平多按钮，弹框点击确认
    预期结果
        A)提示下单成功
        B)当前委托-计划委托列表查询创建订单
    优先级
        1
    用例别名
        TestLinearTriggerCloseSell_005
"""

from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from tool import atp
from pprint import pprint
import pytest, allure, random, time


@allure.epic('正向永续')  # 这里填业务线
@allure.feature('计划委托-平多')  # 这里填功能
@allure.story('触发价低于最新价-刷新最新价-触发')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 邱大伟')
class TestLinearTriggerCloseSell_005:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self,symbol, contract_code, lever_rate, directionB, directionS, offsetC, offsetO):
        print('\n测试标题：触发价低于最新价场景，验证计划委托平多单-委托触发'
              '\n*、先清盘避免盘口数据干扰;'
              '\n*、用户先开仓持仓;'
              '\n*、以触发价低于最新价，买入价低于最新价下平仓计划委托单；'
              '\n*、触发计划委托订单；'
              '\n*、验证计划委托订单触发否')
        print("清盘》》》》", atp.ATP.clean_market())
        self.symbol =symbol
        self.contract_code = contract_code
        self.lever_rate = lever_rate
        self.directionB = directionB
        self.directionS = directionS
        self.offsetC = offsetC
        self.offsetO = offsetO
        self.currentPrice = atp.ATP.get_current_price()  # 最新价
        self.lowPrice = round(self.currentPrice * 0.99, 2)  # 买入价
        self.highPrice = round(self.currentPrice * 1.01, 2)  # 触发价
        print(contract_code, '最新价 = ', self.currentPrice, ' 触发价 = ', self.highPrice, '买入价 = ', self.lowPrice)
        print('开仓……')
        linear_api.linear_order(contract_code=contract_code, price=self.currentPrice, order_price_type='limit',
                                lever_rate=lever_rate, direction='buy', offset=offsetO,
                                volume=1)
        linear_api.linear_order(contract_code=contract_code, price=self.currentPrice, order_price_type='limit',
                                lever_rate=lever_rate, direction='sell', offset=offsetO,
                                volume=1)

    @allure.title('计划委托卖出平多触发价小于最新价')
    @allure.step('测试执行')
    def test_execute(self):
        with allure.step('1、登录合约交易系统'):
            pass
        with allure.step('2、选择币种BTC，选择杠杆5X，点击平仓-计划按钮'):
            pass
        with allure.step('3、输入触发价（如：50000，最新价：50500）'):
            pass
        with allure.step('4、输入卖出价（如：55000）'):
            pass
        with allure.step('5、输入卖出量10张'):
            pass
        with allure.step('6、点击卖出平多按钮，弹框点击确认'):
            orderResult = linear_order.linear_swap_triggerOrder_insert(contract_code=self.contract_code, trigger_type='le',
                                                                       trigger_price=self.lowPrice,
                                                                       order_price=self.lowPrice, volume=1,
                                                                       direction=self.directionS,
                                                                       offset=self.offsetC, lever_rate=self.lever_rate,
                                                                       symbol=self.symbol)
            print(orderResult)
            triggerOrderId = orderResult['data']['order_id']
            print('计划委托单号 = ', triggerOrderId)
            # 单号返回为空则下单失败
            if not triggerOrderId:
                assert False
            pass
        with allure.step('7、刷新最新价，触发计划委托单'):
            linear_api.linear_order(contract_code=self.contract_code, price=self.lowPrice, order_price_type='limit',
                                    lever_rate=self.lever_rate, direction=self.directionB, offset=self.offsetO,
                                    volume=1)
            linear_api.linear_order(contract_code=self.contract_code, price=self.lowPrice, order_price_type='limit',
                                    lever_rate=self.lever_rate, direction=self.directionS, offset=self.offsetO,
                                    volume=1)
            # 等待成交刷新最新价
            time.sleep(1)
        with allure.step('8、验证计划委托单被触发'):
            triggerOrderHistoryOrders = linear_order.linear_swap_his_triggerorders(contract_code=self.contract_code,
                                                                                   trade_type=3)
            # print('计划委托7天内买入平空单历史 =',triggerOrderHistoryOrder)
            historySize = triggerOrderHistoryOrders['data']['total_size']
            # 单页只显示10条数据
            if historySize > 10:
                historySize = 10
            elif historySize == 0:  # 未触发
                assert False
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
        linear_api.linear_order(contract_code=self.contract_code, price=self.highPrice, order_price_type='limit',
                                lever_rate=self.lever_rate,
                                direction=self.directionB, offset=self.offsetC,
                                volume=2)
        linear_api.linear_order(contract_code=self.contract_code, price=self.lowPrice, order_price_type='limit',
                                lever_rate=self.lever_rate,
                                direction=self.directionS, offset=self.offsetC,
                                volume=1)


if __name__ == '__main__':
    pytest.main()
