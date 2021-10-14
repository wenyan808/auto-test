#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20210929
# @Author : YuHuiQing
    用例标题
        计划委托买入开多
    前置条件
        
    步骤/文本
        1、行情-最新价更新为50500；
        2、计划委托下单，触发价为50000；买入价为45000；
        3、行情-最新价更新；使最新价达到50000价，触发计划委托单转换为限制单；
    预期结果
        A)计划委托单下单成功；
        B)达到触发价，计划委托转成限价单；
    优先级
        0
    用例别名
        TestLinearTriggerOpenBuy_005
"""

from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
import pytest, allure, random, time
from tool import atp

@allure.epic('正向永续')  # 这里填业务线
@allure.feature('计划委托下单-开多')  # 这里填功能
@allure.story('以触发价低于最新价-刷新最新价-触发')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 邱大伟')
class TestLinearTriggerOpenBuy_005:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol, contract_code, lever_rate, directionB, directionS, offsetC, offsetO):
        print('\n测试标题：触发价低于最新价场景，验证计划委托开多单-委托触发'
              '\n*、先清盘避免盘口数据干扰;'
              '\n*、以触发价低于最新价，买入价低于最新价下开多计划委托单；'
              '\n*、触发计划委托订单；'
              '\n*、验证计划委托订单触发否')
        print("清盘》》》》", atp.ATP.clean_market())
        print("恢复杠杆》》》", atp.ATP.switch_level(contract_code=contract_code))
        self.symbol = symbol
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

    @allure.title('计划委托买入开多')
    @allure.step('测试执行')
    def test_execute(self):
        with allure.step('1、行情-最新价更新为49800'):
            pass
        with allure.step('2、计划委托下单，触发价为50000；买入价为49800；'):
            self.trigger_price = self.lowPrice
            # ge大于等于(触发价比最新价大)；le小于(触发价比最新价小)
            if self.trigger_price >= self.currentPrice:
                self.trigger_type = 'ge'
            else:
                self.trigger_type = 'le'
            orderResult = linear_order.linear_swap_triggerOrder_insert(contract_code=self.contract_code,
                                                                       trigger_type= self.trigger_type,
                                                                       trigger_price=self.trigger_price,
                                                                       order_price=self.lowPrice, volume=1,
                                                                       direction=self.directionB,
                                                                       offset=self.offsetO, lever_rate=self.lever_rate,
                                                                       symbol=self.symbol)
            # 下单失败则断言失败
            if 'err_msg' in orderResult:
                print(orderResult)
                assert False
            else:
                triggerOrderId = orderResult['data']['order_id']
                print('计划委托单号 = ', triggerOrderId)
            pass
        with allure.step('3、行情-最新价更新；使最新价达到50000价，触发计划委托单转换为限制单'):
            linear_api.linear_order(contract_code=self.contract_code, price=self.lowPrice, order_price_type='limit',
                                    lever_rate=self.lever_rate, direction=self.directionB, offset=self.offsetO,
                                    volume=1)
            linear_api.linear_order(contract_code=self.contract_code, price=self.lowPrice, order_price_type='limit',
                                    lever_rate=self.lever_rate, direction=self.directionS, offset=self.offsetO,
                                    volume=1)
            # 等待成交刷新最新价
            time.sleep(1)
            pass
        with allure.step('4、验证计划委托单被触发'):
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
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print('恢复环境操作：撤销转换的限价单；平掉用户所有的持仓数据')
        linear_order.linear_swap_selection_cancel(contract_code=self.contract_code)
        linear_api.linear_order(contract_code=self.contract_code, price=self.highPrice, order_price_type='limit',
                                lever_rate=self.lever_rate,
                                direction=self.directionB, offset=self.offsetC,
                                volume=1)
        linear_api.linear_order(contract_code=self.contract_code, price=self.lowPrice, order_price_type='limit',
                                lever_rate=self.lever_rate,
                                direction=self.directionS, offset=self.offsetC,
                                volume=1)


if __name__ == '__main__':
    pytest.main()
