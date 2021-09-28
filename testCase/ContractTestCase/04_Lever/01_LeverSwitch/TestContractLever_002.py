#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20210917
# @Author : 
    用例标题
        当前有挂单切换杠杆倍数测试
    前置条件
        1、用户在该业务线下已开户
        2、用户在当前委托下只有止盈止损挂单
    步骤/文本
        1、在交割合约交易页，选择BTC当周合约
        2、观察杠杆倍数指示按钮有结果A
        3、点击杠杆切换按钮有结果B
        4、在杠杆滑动条上，点击30X有结果C
        5、点击杠杆切换框外的区域，有结果D
        6、持仓区域，点击“当前委托”按钮，选择止盈之损tab栏，有结果E
    预期结果
        A)杠杆倍数显示正常(如:5X)
        B)弹起杠杆切换框，杠杆滑动条停留在当前杠杆倍数的位置，杠杆滑动条置灰并有文案提示：您当前有挂单，无法切换杠杆倍数
        C)杠杆滑动条无法选择杠杆倍数
        D)杠杆切换弹框消失，杠杆倍数保持不变
        E)止盈止损委托单，倍数数值与杠杆倍数指示按钮显示的一致
        
    优先级
        0
    用例别名
        TestContractLever_002
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


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('杠杆')  # 这里填功能
@allure.story('杠杆调节')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
class TestContractLever_002:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol, symbol_period):
        print(''' 1、用户在该业务线下已开户
        2、用户在当前委托下只有止盈止损挂单 ''')
        self.symbol = symbol
        # 清除盘口所有卖单
        print(ATP.clean_market(contract_code=symbol_period, direction='sell'))
        time.sleep(2)
        # 清除盘口所有买单
        print(ATP.clean_market(contract_code=symbol_period, direction='buy'))

        r = contract_api.contract_cancelall(symbol=symbol)
        pprint(r)
        r = contract_api.contract_tpsl_cancelall(symbol=symbol)
        pprint(r)
        r = contract_api.contract_trigger_cancelall(symbol=symbol)
        pprint(r)
        r = contract_api.contract_cancelall(symbol=symbol)
        pprint(r)

        print(symbol)
        time.sleep(2)

    @allure.title('当前有挂单切换杠杆倍数测试')
    @allure.step('测试执行')
    def test_execute(self, symbol, symbol_period):
        with allure.step('1、在交割合约交易页，选择BTC当周合约'):
            pass
        with allure.step('2、观察杠杆倍数指示按钮有结果A'):
            pass
        with allure.step('3、点击杠杆切换按钮有结果B'):
            pass
        with allure.step('4、在杠杆滑动条上，点击30X有结果C'):
            pass
        with allure.step('5、点击杠杆切换框外的区域，有结果D'):
            r = contract_api.contract_available_level_rate(symbol=symbol)
            availableleverlist = r['data'][0]['available_level_rate'].split(',')
            i = random.choice(availableleverlist)
            availableleverlist.remove(i)
            j = random.choice(availableleverlist)
            '''下单任意一种杠杆'''
            r = contract_api.contract_history_trade(symbol=symbol_period, size='1')
            pprint(r)
            price = r['data'][0]['data'][0]['price']
            orderprice = round((price * 0.2), 2)
            r = contract_api.contract_order(symbol=symbol,
                                            contract_type='this_week',
                                            contract_code='',
                                            client_order_id='',
                                            price=orderprice,
                                            volume='1',
                                            direction='buy',
                                            offset='open',
                                            lever_rate=i,
                                            order_price_type='limit')
            self.orderid = r['data']['order_id_str']
            pprint(r)
            time.sleep(0.5)
            '''调整杠杆率'''
            r = contract_api.contract_switch_lever_rate(symbol=symbol, lever_rate=j)
            pprint(r)

            assert r['err_msg'] == '当前有挂单,无法切换倍数'
        with allure.step('6、持仓区域，点击“当前委托”按钮，选择止盈之损tab栏，有结果E'):
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        if self.orderid:
            r = contract_api.contract_cancel(symbol=self.symbol, order_id=self.orderid)
            pprint(r)


if __name__ == '__main__':
    pytest.main()
