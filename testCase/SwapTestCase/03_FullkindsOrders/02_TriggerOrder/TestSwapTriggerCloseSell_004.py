#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211010
# @Author :Alexli
"""
	所属分组
		计划委托
	用例标题
		计划委托卖出平多触发价大于最新价
	前置条件

	类型
		文本
	步骤/文本
        1、登录合约交易系统
        2、选择币种BTC，选择杠杆5X，点击平仓-计划按钮
        3、输入触发价（如：50000，最新价：49999）
        4、输入卖出价（如：55000）
        5、输入卖出量10张
        6、点击卖出平多按钮，弹框点击确认
	预期结果
		A)提示下单成功
        B)当前委托-计划委托列表查询创建订单
	标签
		P0
	优先级
		0
	用例别名
		TestSwapTriggerCloseSell_004
"""

from common.SwapServiceAPI import t as swap_api
from common.util import compare_dict

from pprint import pprint
import pytest, allure, random, time


@allure.epic('反向永续')  # 这里填业务线
@allure.feature('计划委托')  # 这里填功能
@allure.story('计划委托卖出平多触发价大于最新价')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestSwapTriggerCloseSell_004:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, contract_code):
        print("自买自卖产生持仓")

        r = swap_api.swap_trade(contract_code=contract_code)
        pprint(r)
        self.price = r['data'][0]['data'][0]['price']
        self.leverrate = '5'

        swap_api.swap_order(contract_code=contract_code, price=self.price, volume='20', direction='buy',
                        offset='open', lever_rate=self.leverrate, order_price_type='limit')
        time.sleep(0.5)
        swap_api.swap_order(contract_code=contract_code, price=self.price, volume='20', direction='sell',
                        offset='open', lever_rate=self.leverrate, order_price_type='limit')

    @allure.title('计划委托卖出平多触发价大于最新价')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        self.contract_code = contract_code
        #orderpricetype = 'optimal_10'
        sltriggerprice = round((self.price * 1.01), 2)
        slorderprice = round((self.price * 1.02), 2)
        r = swap_api.swap_trigger_openorders(contract_code=contract_code,
                                             page_index='',
                                             page_size='')
        totalsize1 = r['data']['total_size']

        with allure.step('1、登录合约交易系统'):
            pass
        with allure.step('2、选择币种BTC，选择杠杆5X，点击平仓-计划按钮'):
            pass
        with allure.step('3、输入触发价（如：50000，最新价：49999）'):
            pass
        with allure.step('4、输入卖出价（如：55000）'):
            pass
        with allure.step('5、输入卖出量10张'):
            pass
        with allure.step('6、点击卖出平多按钮，弹框点击确认'):
            r = swap_api.swap_trigger_order(contract_code=contract_code,
                                            trigger_type='ge',
                                            trigger_price=sltriggerprice,
                                            order_price=slorderprice,
                                            order_price_type='limit',
                                            volume='10',
                                            direction='sell',
                                            offset='close',
                                            lever_rate=self.leverrate)
            pprint(r)
            self.orderid = r['data']['order_id_str']
            print(self.orderid)
            assert r['status'] == 'ok'
            time.sleep(2)
            r = swap_api.swap_trigger_openorders(contract_code=contract_code,
                                                 page_index='',
                                                 page_size='')
            totalsize2 = r['data']['total_size']
            actual_orderinfo = r['data']['orders'][0]
            pprint(actual_orderinfo)
        with allure.step('7、当前委托-计划委托列表查询创建订单B'):
            assert totalsize2 - totalsize1 == 1
            expectdic = {'contract_code': contract_code,
                         'order_price': slorderprice,
                         'order_id': self.orderid,
                         'trigger_type': 'ge',
                         'trigger_price': sltriggerprice,
                         'volume': 10.0,
                         'lever_rate': self.leverrate,
                         'offset': 'close'
                         }
            assert compare_dict(expectdic, actual_orderinfo)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        if self.orderid:
            swap_api.swap_trigger_cancel(contract_code=self.contract_code, order_id=self.orderid)
        r = swap_api.swap_empty_position(contract_code=self.contract_code, price=self.price)
        print('\n恢复环境操作完毕')
        return r

if __name__ == '__main__':
    pytest.main()
