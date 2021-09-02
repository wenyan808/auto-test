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
@allure.feature('组合查询用户历史成交记录')
class TestSwapMatchresultsExact:

    def test_swap_matchresults_exact(self, contract_code):
        r = t.swap_matchresults_exact(contract_code=contract_code,
                                      trade_type='0',
                                      start_time='',
                                      end_time='',
                                      from_id='',
                                      size='',
                                      direct='')
        schema = {
            "status": "ok",
            "data": {
                "trades": [
                    {
                        "id": Or(str, None),
                        "query_id": int,
                        "match_id": int,
                        "order_id": int,
                        "order_id_str": str,
                        "symbol": str,
                        "contract_code": contract_code,
                        "direction": str,
                        "offset": str,
                        "trade_volume": Or(float, int),
                        "trade_price": Or(float, int),
                        "trade_turnover": Or(float, int),
                        "create_date": int,
                        "offset_profitloss": Or(float, int),
                        "real_profit": Or(float, int),
                        "trade_fee": Or(float, int),
                        "role": str,
                        "fee_asset": str,
                        "order_source": str
                    }
                ],
                "remain_size": int,
                "next_id": Or(int, None)
            },
            "ts": int
        }
        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
