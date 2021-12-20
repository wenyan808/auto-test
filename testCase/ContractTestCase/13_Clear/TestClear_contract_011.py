#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/20
# @Author  : Alex Li
"""

所属分组
    定序,清算,落库,复核
用例标题
    当季合约成交数据，检查清算后的redis的APO中的订单数据
前置条件

步骤/文本
    1.次周
预期结果
    1、连接redis的APO，找到用户APO数据
    2、核对APO中持仓数据Position:#BCH#BCH211231#1（1为多仓 2为空仓）,value值中第6位和第7位，分别是持仓量和可平量"
优先级
    0
"""

from decimal import Decimal

import allure
import pytest
from common.ContractServiceAPI import t as contract_api
from common.redisComm import *
from tool.atp import ATP


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('定序,清算,落库,复核')  # 这里填功能
@allure.story('当季合约成交数据，检查清算后的redis的APO中的订单数据')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestClear_contract_011:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol_period):
        print("前置条件 {}".format(symbol_period))
        ATP.make_market_depth()

    @allure.title('获取合约信息')
    @allure.step('测试执行')
    def test_execute(self, symbol_period, symbol):
        contract_type = "quarter"
        with allure.step('1、次周合约成交数据，检查清算后的redis的APO中的订单数据'):
            pass
        with allure.step('2、核对APO中持仓数据Position:  # BCH#BCH211231#1（1为多仓 2为空仓）,value值中第6位和第7位，分别是持仓量和可平量'):
            current_price = ATP.get_current_price(contract_code=symbol_period)
            res = contract_api.contract_order(
                symbol=symbol, contract_type=contract_type, price=current_price, volume=1, direction='buy', offset='open')
            print(res)

            # 获取合约信息
            contract_info = contract_api.contract_contract_info(
                symbol=symbol, contract_type=contract_type)
            print(contract_info)
            contract_code = contract_info["data"][0]["contract_code"]

            # redis 取值
            redis_client = redisConf('redis6380').instance()
            orderPosition = redis_client.hmget(
                "RsT:APO:11538447#BTC", "Position:#{}#{}#1".format(symbol, contract_code))
            redis_position = Decimal(str.split(orderPosition[0], ',')[5])
            assert redis_position > 0

            # 获取持仓信息
            position_info = contract_api.contract_position_info(symbol=symbol)
            print(position_info)

            # reids 值与实际值比较
            for i, val in enumerate(position_info["data"]):
                if(val["symbol"] == symbol and val["contract_code"] == contract_code and val["contract_type"] == contract_type):
                    print("loop {} assert success.".format(i))
                    assert redis_position == val["volume"]
                    break

    @ allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.cancel_all_order()


if __name__ == '__main__':
    pytest.main()
