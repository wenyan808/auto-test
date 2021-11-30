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
class TestSwapApiSchema_047:

    @allure.title("组合查询合约历史委托")
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            r = user01.swap_hisorders_exact(contract_code=contract_code, trade_type=0, type=1, status=0,size=2)
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "data": {
                    "orders": [
                        {
                            "query_id": int,
                            "symbol": symbol,
                            "contract_code": contract_code,
                            "volume": Or(float, int, 0, None),
                            "price": Or(float, int, 0, None),
                            "order_price_type": str,
                            "direction": Or("buy", "sell"),
                            "offset": Or("open", "close"),
                            "lever_rate": int,
                            "order_id": int,
                            "order_id_str": str,
                            "order_source": str,
                            "create_date": int,
                            "trade_volume": Or(float, int, 0, None),
                            "trade_turnover": Or(float, int, 0, None),
                            "fee": Or(float, int, 0, None),
                            "fee_asset": str,
                            "trade_avg_price": Or(float, int, 0, None),
                            "margin_frozen": Or(float, int, 0, None),
                            "profit": Or(float, int, 0, None),
                            "real_profit": Or(float, int, 0, None),
                            "status": int,
                            "liquidation_type": str,
                            "order_type": int,
                            "is_tpsl": Or(0, 1)
                        }
                    ],
                    "remain_size": int,
                    "next_id": int
                },
                "ts": int
            }
            Schema(schema).validate(r)
            pass
