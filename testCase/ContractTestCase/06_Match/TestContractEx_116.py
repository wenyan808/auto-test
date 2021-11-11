#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211028
# @Author : 
    用例标题
        撮合当周 卖出平仓 全部成交单人多笔价格不同的订单     
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        正确撮合
    优先级
        2
    用例别名
        TestContractEx_116
"""

from common.ContractServiceAPI import t as contract_api
from common.ContractServiceAPI import common_user_contract_service_api as common_api
import pytest
import allure
from tool.atp import ATP


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('撮合')  # 这里填功能
@allure.story('委托单')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner :吉龙')
@pytest.mark.stable
class TestContractEx_116:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol):
        print("前置条件  {}".format(symbol))
        ATP.make_market_depth()

    @allure.title('撮合当周 卖出平仓 全部成交单人多笔价格不同的订单')
    @allure.step('测试执行')
    def test_execute(self, symbol):
        with allure.step('步骤详见官方文档'):
            current = ATP.get_current_price(contract_code=symbol)
            offset = 'close'
            direction = 'sell'
            order_price_type = "limit"
            contract_type = "this_week"

            common_api.contract_order(symbol=symbol, price=current*1.01, volume='10', contract_type=contract_type,
                                      direction="sell", offset="open", order_price_type=order_price_type)
            contract_api.contract_order(symbol=symbol, price=current, volume='10', contract_type=contract_type,
                                        direction="buy", offset="open", order_price_type=order_price_type)

            common_api.contract_order(symbol=symbol, price=current*1.01, volume='5', contract_type=contract_type,
                                      direction="buy", offset=offset, order_price_type=order_price_type)
            common_api.contract_order(symbol=symbol, price=current, volume='5', contract_type=contract_type,
                                      direction="buy", offset=offset, order_price_type=order_price_type)

            res = contract_api.contract_order(symbol=symbol, price=current, volume='10', contract_type=contract_type,
                                              direction=direction, offset=offset, order_price_type=order_price_type)
            print(res)
            assert res["status"] == "ok"

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        ATP.cancel_all_order()
        ATP.clean_market()
