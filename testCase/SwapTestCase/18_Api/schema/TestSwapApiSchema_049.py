#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu

import pytest, allure, random, time
from schema import Schema, Or
from common.SwapServiceAPI import user01
from common.CommonUtils import currentPrice
from config.conf import DEFAULT_CONTRACT_CODE
from config.case_content import epic,features

@allure.epic(epic[1])
@allure.feature(features[17]['feature'])
@allure.story(features[17]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_049:

    @allure.title("组合查询用户历史成交记录")
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            r = user01.swap_matchresults_exact(contract_code=contract_code, trade_type=0,size=3)
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "data": {
                    "trades": [
                        {
                            "id": str,
                            "query_id": int,
                            "match_id": int,
                            "order_id": int,
                            "order_id_str": str,
                            "symbol": symbol,
                            "contract_code": contract_code,
                            "direction": Or("buy", "sell"),
                            "offset": Or("open", "close"),
                            "trade_volume": Or(float, int, 0, None),
                            "trade_price": Or(float, int, 0, None),
                            "trade_turnover": Or(float, int, 0, None),
                            "create_date": int,
                            "offset_profitloss": Or(float, int, 0, None),
                            "real_profit": Or(float, int, 0, None),
                            "trade_fee": Or(float, int, 0, None),
                            "role": Or('Maker', 'Taker'),
                            "fee_asset": symbol,
                            "order_source": str
                        }
                    ],
                    "remain_size": int,
                    "next_id": int
                },
                "ts": int
            }
            Schema(schema).validate(r)
            pass
