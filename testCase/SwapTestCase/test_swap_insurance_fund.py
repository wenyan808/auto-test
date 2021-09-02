#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/10/13
# @Author  : zhangranghan


from common.SwapServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema, And, Or, Regex, SchemaError

from pprint import pprint
import pytest, allure, random, time


@allure.epic('反向永续')
@allure.feature('查询合约风险准备金余额历史数据')
class TestSwapTrade:

    def test_swap_trade(self, contract_code):
        r = t.swap_insurance_fund(contract_code=contract_code, page_index='', page_size='')
        schema = {
            "status": "ok",
            "ts": int,
            "data": {
                "symbol": str,
                "contract_code": contract_code,
                "tick": [
                    {
                        "insurance_fund": Or(float, int),
                        "ts": int
                    }
                ],
                "total_page": int,
                "current_page": int,
                "total_size": int
            }
        }
        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
