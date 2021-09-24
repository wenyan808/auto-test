#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20210918
# @Author : 
    用例标题
        计划委托正常限价开仓测试
    前置条件
        
    步骤/文本
        1、登录U本位永续界面
        2、选择BTC当周，选择杠杆5X，点击开仓-计划按钮
        3、输入触发价（如：50000）
        4、输入买入价（如：49800）
        5、输入买入量10张
        6、点击买入开多按钮后弹框确认有结果A
        7、查看当前委托列表中的计划委托有结果B
    预期结果
        A)提示下单成功
        B)在当前委托-计划委托统计数量+1，列表数量+1,展示合约交易类型，委托类型，倍数，时间，委托数量，委托价信息和下单数值一致
    优先级
        0
    用例别名
        TestUSDTSwapTriggerOrder_001
"""

from common.LinearServiceAPI import t as linear_api
from common.util import compare_dict

from pprint import pprint
import pytest, allure, random, time


@allure.epic('业务线')  # 这里填业务线
@allure.feature('功能')  # 这里填功能
#@allure.story('子功能')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
class TestUSDTSwapTriggerOrder_001:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('计划委托正常限价开仓测试')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        self.contract_code = contract_code
        leverrate = '5'
        r = linear_api.linear_cross_trigger_openorders(contract_code=contract_code,
                                             page_index='',
                                             page_size='')
        totalsize1 = r['data']['total_size']

        with allure.step('1、登录U本位永续界面'):
            pass
        with allure.step('2、选择BTC当周，选择杠杆5X，点击开仓-计划按钮'):
            pass
        with allure.step('3、输入触发价（如：50000）'):
            r = linear_api.linear_history_trade(contract_code=contract_code, size='1')
            pprint(r)
            self.price = r['data'][0]['data'][0]['price']
            sltriggerprice = round((self.price * 0.97), 2)
            slorderprice = round((self.price * 0.98), 2)
            pprint(slorderprice)

        with allure.step('4、输入买入价（如：49800）'):
            pass
        with allure.step('5、输入买入量10张'):
            pass
        with allure.step('6、点击买入开多按钮后弹框确认有结果A'):
            r = linear_api.linear_cross_trigger_order(contract_code=contract_code,
                                            trigger_type='le',
                                            trigger_price=sltriggerprice,
                                            order_price=slorderprice,
                                            order_price_type='limit',
                                            volume='10',
                                            direction='buy',
                                            offset='open',
                                            lever_rate=leverrate)
            pprint(r)
            self.orderid = r['data']['order_id_str']
            print(self.orderid)
            assert r['status'] == 'ok'
            time.sleep(2)
            r = linear_api.linear_cross_trigger_openorders(contract_code=contract_code,
                                                 page_index='',
                                                 page_size='')
            totalsize2 = r['data']['total_size']
            actual_orderinfo = r['data']['orders'][0]
            pprint(actual_orderinfo)
        with allure.step('7、查看当前委托列表中的计划委托有结果B'):
            assert totalsize2 - totalsize1 == 1
            expectdic = {'contract_code': contract_code,
                         'order_price': slorderprice,
                         'order_id': self.orderid,
                         'trigger_type': 'le',
                         'trigger_price': sltriggerprice,
                         'volume': 10.0,
                         'lever_rate': leverrate
                         }
            assert compare_dict(expectdic, actual_orderinfo)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        if self.orderid:
            r = linear_api.linear_cross_trigger_cancel(contract_code=self.contract_code, order_id=self.orderid)


if __name__ == '__main__':
    pytest.main()
