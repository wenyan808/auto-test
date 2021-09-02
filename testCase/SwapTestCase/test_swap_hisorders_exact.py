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
@allure.feature('组合查询合约历史委托')
class TestSwapHisordersExact:

    def test_swap_hisorders_exact(self, contract_code):
        r = t.swap_hisorders_exact(contract_code=contract_code,
                                   trade_type='0',
                                   type='1',
                                   status='0',
                                   start_time='',
                                   end_time='',
                                   from_id='',
                                   size='',
                                   direct='')
        schema = {
            "status": "ok",
            "data": {
                "orders": [
                    {
                        "query_id": Or(int, float, None),
                        "symbol": str,
                        "contract_code": contract_code,
                        "volume": Or(int, float, None),
                        "price": Or(int, float, None),
                        "order_price_type": str,
                        "direction": str,
                        "offset": str,
                        "lever_rate": Or(int, float, None),
                        "order_id": Or(int, float, None),
                        "order_id_str": str,
                        "order_source": str,
                        "create_date": Or(int, float, None),
                        "trade_volume": Or(int, float, None),
                        "trade_turnover": Or(int, float, None),
                        "fee": Or(int, float, None),
                        "fee_asset": str,
                        "trade_avg_price": Or(int, float, None),
                        "margin_frozen": Or(int, float, None),
                        "profit": Or(int, float, None),
                        "real_profit": Or(int, float, None),
                        "status": int,
                        "liquidation_type": str,
                        "order_type": Or(int, float, None),
                        "is_tpsl": Or(int, float, None)
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
