#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20210917
# @Author : 张广南
    用例标题
        撤销止盈止损订单
    前置条件
        不要触发
    步骤/文本
        1、登录币本位永续界面
        2、选择BTC/USD，选择杠杆5X，点击开仓-限价按钮
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
        TestCoinswapTriggerOrder_021
"""

from common.SwapServiceAPI import t as swap_api
from common.util import compare_dict
from pprint import pprint
import pytest, allure, random, time
from config.case_content import epic, features

@allure.epic(epic[1])
@allure.feature(features[2]['feature'])
@allure.story(features[2]['story'][2])
@pytest.mark.stable
class TestCoinswapTriggerOrder_021:

    @allure.step('前置条件')
    def setup(self):
        print(''' 不要触发 ''')

    @allure.title('撤销止盈止损订单')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        self.contract_code = contract_code
        with allure.step('1、登录币本位永续界面'):
            pass
        with allure.step('2、选择BTC/USD，选择杠杆5X，点击开仓-限价按钮'):
            pass
        with allure.step('3、下一单带有止盈止损的限价单'):
            r = swap_api.swap_history_trade(contract_code=contract_code, size='1')
            pprint(r)
            self.price = r['data'][0]['data'][0]['price']
            orderprice = round((self.price * 0.99), 1)
            sltriggerprice = round((self.price * 0.97), 1)
            slorderprice = round((self.price * 0.98), 1)
            pprint(slorderprice)
            r = swap_api.swap_order(contract_code=contract_code,
                                    client_order_id='',
                                    price=str(orderprice),
                                    volume='1',
                                    direction='buy',
                                    offset='open',
                                    lever_rate='5',
                                    order_price_type='limit',
                                    sl_trigger_price=sltriggerprice,
                                    sl_order_price=slorderprice
                                    )
            pprint(r)

            orderid = r['data']['order_id_str']
            pprint(orderid)
        with allure.step('4、待限价单成交之后，在当前委托-止盈止损界面点击订单右方的撤销按钮有结果A'):
            r = swap_api.swap_order(contract_code=contract_code, client_order_id="", price=orderprice, volume='1',
                                direction='sell', offset='open', lever_rate='5', order_price_type='limit')
            pprint(r)
            time.sleep(2)
            r = swap_api.swap_tpsl_openorders(contract_code=contract_code)
            actual_orderinfo = r['data']['orders'][0]
            tporderid = actual_orderinfo['order_id']
            expectdic = {'contract_code': contract_code,
                         'order_price': slorderprice,
                         'source_order_id': orderid,
                         'tpsl_order_type': 'sl',
                         'trigger_price': sltriggerprice,
                         }
            assert compare_dict(expectdic, actual_orderinfo)

        with allure.step('5、查看当前委托-止盈止损页面有结果B'):
            swap_api.swap_tpsl_cancel(contract_code=contract_code, order_id=tporderid)
            time.sleep(2)
            r = swap_api.swap_tpsl_openorders(contract_code=contract_code)
            totalsize = r['data']['total_size']
            assert totalsize == 0

        with allure.step('6、查看历史委托-止盈止损页面有结果C'):
            r = swap_api.swap_tpsl_hisorders(contract_code=contract_code, status='0', create_date='7')
            actual_orderinfo = r['data']['orders'][0]
            assert compare_dict(expectdic, actual_orderinfo)

    @allure.step('恢复环境')
    def teardown(self):
        r = swap_api.swap_empty_position(contract_code=self.contract_code, price=self.price)
        print('\n恢复环境操作完毕')
        return r


if __name__ == '__main__':
    pytest.main()
