#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22
# @Author  : Alex Li
"""

所属分组
    反向交割 API 测试
用例标题
    获取用户的合约历史成交记录
前置条件

步骤/文本
    1.调用接口：api/v1/contract_matchresults
预期结果
    A)接口返回的json格式、字段名、字段值正确
优先级
    1
"""
from pprint import pprint

import allure
import pytest
from schema import Or, Schema

from common.ContractServiceAPI import t as contract_api


@allure.epic('反向交割')  # 这里填业务线
@allure.feature('API 测试')  # 这里填功能
@allure.story('获取用户的合约历史成交记录')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : Alex Li', 'Case owner : Alex Li')
@pytest.mark.stable
class TestApiSchema_046:

    @allure.step('前置条件')
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, symbol):
        print("前置条件 {}".format(symbol))

    @allure.title('获取用户的合约历史成交记录')
    @allure.step('测试执行')
    def test_execute(self, symbol):
        with allure.step('1、调用接口：api/v1/contract_matchresults'):
            pass
        with allure.step('2、接口返回的json格式、字段名、字段值正确'):
            # 构造持仓量
            res = contract_api.contract_matchresults(
                symbol=symbol, trade_type=0, create_date=30)
            pprint(res)

            schema = {
                "status": "ok",
                "data": {
                    "trades": [
                        {
                            "match_id": int,
                            "order_id": int,
                            "symbol": str,
                            "contract_type": str,
                            "contract_code": str,
                            "direction": str,
                            "offset": str,
                            "trade_volume": Or(float, int),
                            "trade_price": Or(float, int),
                            "trade_turnover": Or(float, int),
                            "trade_fee": Or(float, int),
                            "offset_profitloss": Or(float, int),
                            "create_date": int,
                            "role": str,
                            "order_source": str,
                            "order_id_str": str,
                            "fee_asset": str,
                            "real_profit": Or(float, int),
                            "id": str
                        }
                    ],
                    "total_page": int,
                    "current_page": int,
                    "total_size": int
                },
                "ts": int
            }
            Schema(schema).validate(res)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
