#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211012
# @Author : chenwei
    用例标题
        WS订阅基差数据
    前置条件
        
    步骤/文本
        WS订阅基差K线订阅1min举例： {sub": "market.BTC-USD.basis.1min.open","id": "id7"}
        返回成功举例：{"ch":"market.BTC-USD.basis.1min.open","ts":1617164081549,"tick":{"id":1617164040,"index_price":"58686.78333333333","contract_price":"58765","basis":"78.21666666667","basis_rate":"0.0013327816285723049700163397705562309" }}
        参考地址：https://docs.huobigroup.com/docs/coin_margined_swap/v1/cn/#45aabcd3fd"
    预期结果
        id、index_price、contract_price、basis、basis_rate正确
    优先级
        0
    用例别名
        Test_WS_swap_Index_004
"""

from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order

from pprint import pprint
import pytest, allure, random, time
from common.SwapServiceWS import t as websocketsevice
from tool.atp import ATP


@allure.epic('反向永续')  # 这里填业务线
@allure.feature('指数基差')  # 这里填功能
@allure.story('WS订阅')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : chenwei', 'Case owner : 叶永刚')
class Test_WS_swap_Index_004:

    @allure.step('前置条件')
    def setup(self):
        ATP.cancel_all_types_order()
        print(''' 制造成交数据 ''')
        ATP.make_market_depth()
        sell_price = ATP.get_adjust_price(1.02)
        buy_price = ATP.get_adjust_price(0.98)
        ATP.common_user_make_order(price=sell_price, direction='sell')
        ATP.common_user_make_order(price=buy_price, direction='buy')
        time.sleep(1)
        self.current_price = ATP.get_current_price()

    @allure.title('WS订阅基差数据')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step('WS订阅基差K线订阅1min举例： {sub": "market.BTC-USD.basis.1min.open","id": "id7"}'):
            period = "1min"
            basis_price_type = "open"
            r = websocketsevice.swap_sub_basis(contract_code, period,basis_price_type)
            pprint(r)
        with allure.step('返回成功举例：{"ch":"market.BTC-USD.basis.1min.open","ts":1617164081549,"tick":{"id":1617164040,"index_price":"58686.78333333333","contract_price":"58765","basis":"78.21666666667","basis_rate":"0.0013327816285723049700163397705562309" }}'):
            pass
        with allure.step('参考地址：https://docs.huobigroup.com/docs/coin_margined_swap/v1/cn/#45aabcd3fd"'):
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.clean_market()


if __name__ == '__main__':
    pytest.main()
