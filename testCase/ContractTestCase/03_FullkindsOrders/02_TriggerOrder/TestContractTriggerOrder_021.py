#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20210917
# @Author : 
    用例标题
        撤销止盈止损订单
    前置条件
        不要触发
    步骤/文本
        1、登录交割合约界面
        2、选择BTC当周，选择杠杆5X，点击开仓-限价按钮
        3、下一单带有止盈止损的限价单
        4、待限价单成交之后，在当前委托-止盈止损界面点击订单右方的撤销按钮有结果A
        5、查看当前委托-止盈止损页面有结果B
        6、查看历史委托-止盈止损页面有结果C
    预期结果
        A)撤销申请成功
        B)当前委托-止盈止损列表订单消失
        C)在历史委托-止盈止损有刚才撤销的订单记录
    优先级
        0
    用例别名
        TestContractTriggerOrder_021
"""

from common.ContractServiceAPI import t as contract_api
from common.util import compare_dict
from pprint import pprint
import pytest
import allure
import random
import time

from tool.atp import ATP


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('计划委托')  # 这里填功能
# @allure.story('子功能')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 张广南', 'Case owner : 邱大伟')
class TestContractTriggerOrder_021:

    @allure.step('前置条件')
    def setup(self):
        print('\n前置条件')
        ATP.close_all_position()
        ATP.clean_market()

    @allure.title('撤销止盈止损订单')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        self.symbol = symbol
        with allure.step('1、登录交割合约界面'):
            pass
        with allure.step('2、选择BTC当周，选择杠杆5X，点击开仓-限价按钮'):
            pass
        with allure.step('3、下一单带有止盈止损的限价单'):
            r = contract_api.contract_history_trade(
                symbol=symbol_period, size='1')
            pprint(r)
            self.price = r['data'][0]['data'][0]['price']
            orderprice = round((self.price * 0.99), 1)
            sltriggerprice = round((self.price * 0.97), 1)
            slorderprice = round((self.price * 0.98), 1)

            r = contract_api.contract_order(symbol=symbol,
                                            contract_type='this_week',
                                            contract_code='',
                                            client_order_id='',
                                            price=orderprice,
                                            volume='1',
                                            direction='buy',
                                            offset='open',
                                            lever_rate='5',
                                            order_price_type='limit',
                                            sl_trigger_price=sltriggerprice,
                                            sl_order_price=slorderprice
                                            )

            orderid = r['data']['order_id_str']
            pprint(orderid)
        with allure.step('4、待限价单成交之后，在当前委托-止盈止损界面点击订单右方的撤销按钮有结果A'):
            contract_api.contract_order(symbol=symbol, contract_type='this_week', price=orderprice, volume='1',
                                        direction='sell', offset='open', lever_rate='5', order_price_type='limit')
            time.sleep(4)
            r = contract_api.contract_tpsl_openorders(symbol=symbol)
            pprint(r)
            actual_orderinfo = r['data']['orders'][0]
            tporderid = actual_orderinfo['order_id']
            expectdic = {'symbol': symbol,
                         'contract_type': 'this_week',
                         'order_price': slorderprice,
                         'source_order_id': orderid,
                         'tpsl_order_type': 'sl',
                         'trigger_price': sltriggerprice,
                         }
            assert compare_dict(expectdic, actual_orderinfo)

        with allure.step('5、查看当前委托-止盈止损页面有结果B'):
            contract_api.contract_tpsl_cancel(
                symbol=symbol, order_id=tporderid)

            r = contract_api.contract_tpsl_openorders(symbol=symbol)
            totalsize = r['data']['total_size']
            assert totalsize == 0

        with allure.step('6、查看历史委托-止盈止损页面有结果C'):
            r = contract_api.contract_tpsl_hisorders(
                symbol=symbol, status='0', create_date='7')
            actual_orderinfo = r['data']['orders'][0]
            expectdic = {'symbol': symbol,
                         'contract_type': 'this_week',
                         'order_price': slorderprice,
                         'source_order_id': orderid,
                         'tpsl_order_type': 'sl',
                         'trigger_price': sltriggerprice,
                         }
            assert compare_dict(expectdic, actual_orderinfo)

    @allure.step('恢复环境')
    def teardown(self):
        r = contract_api.contract_empty_position(
            symbol=self.symbol, price=self.price)
        print('\n恢复环境操作完毕')
        return r


if __name__ == '__main__':
    pytest.main()
