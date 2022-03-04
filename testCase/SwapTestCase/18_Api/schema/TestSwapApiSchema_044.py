#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu
from pprint import pprint

import allure
import time
from schema import Schema, Or

from common.SwapServiceAPI import user01
from config.case_content import epic, features
from tool.atp import ATP


@allure.epic(epic[1])
@allure.feature(features[17]['feature'])
@allure.story(features[17]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
class TestSwapApiSchema_043:

    @classmethod
    def setup_class(cls):
        with allure.step('变量初始化'):
        #     cls.contract_code = DEFAULT_CONTRACT_CODE
        #     cls.symbol = DEFAULT_SYMBOL
        #     cls.latest_price = SwapTool.currentPrice(contract_code=cls.contract_code)
            pass
        # with allure.step('挂盘'):
        #     cls.orderId = user01.swap_order(contract_code=cls.contract_code,price=round(cls.latest_price * 0.8, 2),
        #                                     direction='buy')['data']['order_id_str']
        #     time.sleep(1)  # 等待盘口更新

    @classmethod
    def teardown_class(cls):
        with allure.step('恢复环境：撤单'):
            print(ATP.cancel_all_order())

    @allure.title("获取用户的合约订单明细信息")
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            price = ATP.get_current_price()
            a = user01.swap_order(contract_code=contract_code, price=round(price * 0.8, 2), direction='buy')
            orderid = a['data']['order_id_str']
            time.sleep(1)
            r = user01.swap_order_detail(order_id=orderid, contract_code=contract_code)
            pprint(r)
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "data": {
                    "symbol": symbol,
                    "contract_code": contract_code,
                    "volume": Or(int,float,None),
                    "price": Or(int,float,None),
                    "order_price_type": str,
                    "direction": Or("buy","sell"),
                    "offset": Or("open","close"),
                    "lever_rate": Or(int,float,None),
                    "margin_frozen": Or(int,float,None),
                    "profit": Or(int,float,None),
                    "real_profit": Or(int,float,None),
                    "order_source": str,
                    "created_at": int,
                    "canceled_at": int,
                    "instrument_price": Or(int,float,None),
                    "final_interest": Or(int,float,None),
                    "adjust_value": Or(int,float,None),
                    "fee": Or(int,float,None),
                    "fee_asset": symbol,
                    "liquidation_type": str,
                    "order_id": int,
                    "order_id_str": str,
                    "client_order_id": int,
                    "order_type": int,
                    "status": int,
                    "trade_avg_price": Or(int,float,None),
                    "trade_turnover": int,
                    "trade_volume": int,
                    "is_tpsl": int,
                    "trades": [
                        {
                            "trade_id": int,
                            "id": str,
                            "trade_volume": Or(int,float,None),
                            "trade_price": Or(int,float,None),
                            "trade_fee": Or(int,float,None),
                            "fee_asset": symbol,
                            "trade_turnover": Or(int,float,None),
                            "role": Or("maker","taker"),
                            "profit": Or(int,float,None),
                            "real_profit": Or(int,float,None),
                            "created_at": int
                        }
                    ],
                    "total_page": int,
                    "total_size": int,
                    "current_page": int
                },
                "ts": int
            }
            Schema(schema).validate(r)
            pass
