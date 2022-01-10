#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/9
# @Author  : Alex Li
"""
    用例标题
        母用户- 币本位交割当周-切换杠杆倍数-有持仓有限价单挂单切换杠杆
    前置条件

    步骤/文本
        1、在币本位交割合约交易页，选择币本位交割当周合约，检查杠杆倍数

    预期结果
        滑动条灰显，您当前有挂单，无法切换杠杆倍数，切换杠杆失败
    优先级
        0
    用例别名
        TestContractLever_s113
"""

from common.ContractServiceAPI import t as contract_api
import pytest
import time
import allure
from schema import Schema
from common.redisComm import *
from common.mysqlComm import *
from tool.atp import ATP


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('切换杠杆')  # 这里填功能
@allure.story('在币本位交割合约交易页，选择币本位交割当周合约，检查杠杆倍数')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : 叶永刚')
@pytest.mark.stable
class TestContractLever_s113:

    params = [
        {"contract_type": "this_week", "period": "_CW", "case_title": "母用户- 币本位交割当周-切换杠杆倍数-有持仓有限价单挂单切换杠杆",
            "id": "TestContractLever_113", "lever_rate": 5},
        {"contract_type": "next_week", "period": "_NW", "case_title": "母用户- 币本位交割次周-切换杠杆倍数-有持仓有限价单挂单切换杠杆",
            "id": "TestContractLever_114", "lever_rate": 5},
        {"contract_type": "quarter", "period": "_CQ", "case_title": "母用户- 币本位交割当季-切换杠杆倍数-有持仓有限价单挂单切换杠杆",
            "id": "TestContractLever_115", "lever_rate": 5},
        {"contract_type": "next_quarter", "period": "_NQ", "case_title": "母用户- 币本位交割次季-切换杠杆倍数-有持仓有限价单挂单切换杠杆",
         "id": "TestContractLever_116", "lever_rate": 5},
        {"contract_type": "this_week", "period": "_CW", "case_title": "母用户- 币本位交割当周-切换杠杆倍数-高倍杠杆-有持仓有限价单挂单切换杠杆",
         "id": "TestContractLever_121", "lever_rate": 50},
        {"contract_type": "next_week", "period": "_NW", "case_title": "母用户- 币本位交割次周-切换杠杆倍数-高倍杠杆-有持仓有限价单挂单切换杠杆",
            "id": "TestContractLever_122", "lever_rate": 50},
        {"contract_type": "quarter", "period": "_CQ", "case_title": "母用户- 币本位交割当季-切换杠杆倍数-高倍杠杆-有持仓有限价单挂单切换杠杆",
            "id": "TestContractLever_123", "lever_rate": 50},
        {"contract_type": "next_quarter", "period": "_NQ", "case_title": "母用户- 币本位交割次季-切换杠杆倍数-高倍杠杆-有持仓有限价单挂单切换杠杆",
         "id": "TestContractLever_124", "lever_rate": 50}
    ]

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol_period):
        print("前置：{}", symbol_period)
        ATP.cancel_all_types_order()

    @ allure.title('母用户- 币本位交割当周-切换杠杆倍数')
    @ allure.step('测试执行')
    @ pytest.mark.parametrize('param', params, ids=[x['id'] for x in params])
    def test_execute(self, symbol, param):
        allure.dynamic.title(param['case_title'])
        symbol_period = symbol+param["period"]
        ATP.make_market_depth(
            contract_code=symbol_period, volume=1, depth_count=1)

        currentPrice = ATP.get_current_price(
            contract_code=symbol_period)  # 最新价
        # 构造持仓
        contract_api.contract_order(symbol=symbol, contract_type=param["contract_type"], price=currentPrice,
                                    direction='buy', offset="open", volume=1, lever_rate=5, order_price_type='limit')
        # 构造挂单
        contract_api.contract_order(
            symbol=symbol, contract_type=param["contract_type"], price=round(currentPrice*0.95, 2), direction='buy', volume=5, lever_rate=5, order_price_type='limit')
        time.sleep(1)
        with allure.step('1、在币本位交割合约交易页，选择币本位交割当周合约，检查杠杆倍数'):
            res = contract_api.contract_switch_lever_rate(
                symbol=symbol, lever_rate=param["lever_rate"])
            # 有挂单不允许切换
            print(res)

            # 根据查持仓来判断，否则容易成交
            position_info = contract_api.contract_account_position_info(
                symbol=symbol)
            print(position_info)
            contract_type_position = False  # 是否有该 contract_type 持仓
            if position_info["data"]:
                for v in position_info["data"]:
                    if(v["symbol"] == symbol):
                        if(v["positions"]):
                            for position in v["positions"]:
                                if position["contract_type"] == param["contract_type"]:
                                    contract_type_position = True
            if not contract_type_position:
                schema = {'status': str, 'err_code': int,
                          'err_msg': str, 'ts': int}
                Schema(schema).validate(res)
                assert res["status"] == "error"

    @ allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
