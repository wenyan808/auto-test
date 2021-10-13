#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211012
# @Author : chenwei
    用例标题
        WS订阅指数K线数据
    前置条件
        
    步骤/文本
        WS订阅指数K线订阅参数1min举例：{"sub": "market.BTC-USD.index.1min", "id": "id1"}
        返回成功举例：{"ch":"market.BTC-USD.index.1min","ts":1604387688243,"tick":{"id":1604387640,"open":"13419.4325","close":"13420.3325","high":"13424.4925","low":"13419.4325","amount":"0","vol":"0","count":0}}
        参考地址：https://docs.huobigroup.com/docs/coin_margined_swap/v1/cn/#sub-k
    预期结果
        id、open、close、low、high价格正确；amount、vol、count值正确,不存在Null,[]
    优先级
        0
    用例别名
        Test_WS_swap_Index_001
"""

from common.ContractServiceAPI import t as contract_api
from common.ContractServiceOrder import t as contract_order
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order
from common.SwapServiceWS import t as websocketsevice
from pprint import pprint
import pytest, allure, random, time


@allure.epic('反向永续')  # 这里填业务线
@allure.feature('功能')  # 这里填功能
@allure.story('子功能')  # 这里填子功能，没有的话就把本行注释掉
class Test_WS_swap_Index_001:

    @allure.step('前置条件')
    def setup(self):
        print('''  ''')

    @allure.title('WS订阅指数K线数据')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step('WS订阅指数K线订阅参数1min举例：{"sub": "market.BTC-USD.index.1min", "id": "id1"}'):
            period = "1min"
            r = websocketsevice.swap_sub_index(contract_code,period)
            pprint(r)
        with allure.step('返回成功举例：{"ch":"market.BTC-USD.index.1min","ts":1604387688243,"tick":{"id":1604387640,"open":"13419.4325","close":"13420.3325","high":"13424.4925","low":"13419.4325","amount":"0","vol":"0","count":0}}'):
            pass
        with allure.step('参考地址：https://docs.huobigroup.com/docs/coin_margined_swap/v1/cn/#sub-k'):
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
