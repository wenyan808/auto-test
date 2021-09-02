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
@allure.feature('获取历史成交记录')
class TestSwapMatchresults:

    def test_swap_matchresults(self, contract_code):
        r = t.swap_matchresults(contract_code=contract_code,
                                trade_type='0',
                                create_date='7',
                                page_index='',
                                page_size='')
        schema = {
            "data": {
                "current_page": int,
                "total_page": int,
                "total_size": int,
                "trades": [{
                    "contract_code": contract_code,
                    "create_date": Or(float, int),
                    "direction": str,
                    "match_id": Or(float, int),
                    "id": Or(str, None),
                    "offset": str,
                    "offset_profitloss": Or(float, int),
                    "real_profit": Or(float, int),
                    "order_id": Or(float, int),
                    "order_id_str": str,
                    "symbol": str,
                    "order_source": str,
                    "trade_fee": Or(float, int),
                    "fee_asset": str,
                    "trade_price": Or(float, int),
                    "trade_turnover": Or(float, int),
                    "role": str,
                    "trade_volume": Or(float, int)
                }]
            },
            "status": "ok",
            "ts": int
        }
        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
