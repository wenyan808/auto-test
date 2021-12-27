#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/20
# @Author  : Alex Li
"""

所属分组
    定序,清算,落库,复核
用例标题
    当周合约下单挂单数据，检查清算后的redis的APO中的订单数据
前置条件

步骤/文本
    1.用户下当周合约的挂单，记住user_order_id
预期结果
    1、连接redis的APO，找到用户APO数据
    2、根据user_order_id核对APO中持仓数据（注意下面的user_order_id替换成实际下单的数据）Order:#847833760893657088#1  （1为多单，2为空单）"
优先级
    0
"""


import allure
import pytest
from common.ContractServiceAPI import t as contract_api
from tool.atp import ATP
from common.redisComm import *


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('定序,清算,落库,复核')  # 这里填功能
@allure.story('当周合约下单挂单数据，检查清算后的redis的APO中的订单数据')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestClear_contract_001:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol_period):
        print("前置条件 {}".format(symbol_period))
        ATP.make_market_depth()

    @allure.title('获取合约信息')
    @allure.step('测试执行')
    def test_execute(self, symbol_period):
        with allure.step('1、用户下当周合约的挂单，记住user_order_id'):
            pass
        with allure.step('2、根据user_order_id核对APO中持仓数据（注意下面的user_order_id替换成实际下单的数据）Order:#847833760893657088#1  （1为多单，2为空单）'):
            current_price = ATP.get_current_price(contract_code=symbol_period)
            res = contract_api.contract_order(
                symbol='BTC', contract_type='this_week', price=current_price, volume=1, direction='buy', offset='open')
            print(res)
            self._order_id_str = res["data"]["order_id_str"]
            redis_client = redisConf('redis6380').instance()
            position = redis_client.hmget(
                "RsT:APO:11538447#BTC", "Order:#{}#1".format(self._order_id_str))
            print(position)
            assert position != None

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.cancel_all_order()


if __name__ == '__main__':
    pytest.main()
