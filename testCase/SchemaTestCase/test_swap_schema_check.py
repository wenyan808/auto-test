from common.SwapServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema, And, Or, Regex, SchemaError
from pprint import pprint
import pytest, allure, random, time


@allure.epic('反向永续')
class TestSwapCancelall:
    if __name__ == '__main__':
        pytest.main()

    @allure.feature('获取用户账户信息')
    def test_swap_account_info(self, contract_code):
        r = t.swap_account_info(contract_code=contract_code)
        schema = {
            "status": "ok",
            "data": [
                {
                    "symbol": str,
                    "contract_code": str,
                    "margin_balance": Or(float, int, 0),
                    "margin_static": Or(float, int, 0),
                    "margin_position": Or(float, int, 0),
                    "margin_frozen": Or(float, int, 0),
                    "margin_available": Or(float, int, 0),
                    "profit_real": Or(float, int, 0),
                    "profit_unreal": Or(float, int, 0),
                    "withdraw_available": Or(float, int, 0),
                    "risk_rate": Or(float, int, 0),
                    "liquidation_price": Or(float, int, 0),
                    "lever_rate": Or(float, int, 0),
                    "adjust_factor": Or(float, int, 0),
                    "transfer_profit_ratio": Or(float, int, None)
                }
            ],
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('获取用户资产和持仓信息')
    def test_swap_account_position_info(self, contract_code):
        r = t.swap_account_position_info(contract_code=contract_code)
        schema = {
            "status": "ok",
            "ts": int,
            "data": [{
                "symbol": str,
                "contract_code": str,
                "margin_balance": Or(float, int),
                "margin_position": Or(float, int),
                "margin_frozen": Or(float, int),
                "margin_available": Or(float, int),
                "profit_real": Or(float, int),
                "profit_unreal": Or(float, int),
                "risk_rate": Or(float, int, None),
                "withdraw_available": Or(float, int),
                "liquidation_price": Or(float, int, None),
                "lever_rate": Or(float, int),
                "adjust_factor": Or(float, int),
                "margin_static": Or(float, int),
                "positions": [{
                    "symbol": str,
                    "contract_code": str,
                    "volume": Or(float, int),
                    "available": Or(float, int),
                    "frozen": Or(float, int),
                    "cost_open": Or(float, int),
                    "cost_hold": Or(float, int),
                    "profit_unreal": Or(float, int),
                    "profit_rate": Or(float, int),
                    "profit": Or(float, int),
                    "position_margin": Or(float, int),
                    "lever_rate": Or(float, int),
                    "direction": str,
                    "last_price": Or(float, int)
                }]
            }]
        }
        Schema(schema).validate(r)

    @allure.feature('查询平台阶梯调整系数')
    def test_swap_adjustfactor(self, contract_code):
        r = t.swap_adjustfactor(contract_code=contract_code)
        schema = {
            "status": "ok",
            "data": [
                {
                    "symbol": str,
                    "contract_code": str,
                    "list": [
                        {
                            "lever_rate": int,
                            "ladders": [
                                {
                                    "ladder": int,
                                    "min_size": Or(int, None),
                                    "max_size": Or(int, None),
                                    "adjust_factor": Or(float, int)
                                }
                            ]
                        }
                    ]
                }
            ],
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('查询系统状态')
    def test_swap_api_state(self, contract_code):
        r = t.swap_api_state(contract_code=contract_code)
        pprint(r)
        schema = {
            "status": "ok",
            "data": [
                {
                    "symbol": str,
                    "contract_code": contract_code,
                    "open": Or(float, int, None),
                    "close": Or(float, int, None),
                    "cancel": Or(float, int, None),
                    "transfer_in": Or(float, int, None),
                    "transfer_out": Or(float, int, None),
                    "master_transfer_sub": Or(float, int, None),
                    "sub_transfer_master": Or(float, int, None),
                }
            ],
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('获取用户的API指标禁用信息')
    def test_swap_api_trading_status(self):
        r = t.swap_api_trading_status()
        pprint(r)
        schema = {
            "status": "ok",
            "data":
                {
                    "is_disable": Or(float, int, None),
                    "order_price_types": str,
                    "disable_reason": str,
                    "disable_interval": Or(float, int, None),
                    "recovery_time": Or(float, int, None),
                    "COR": {
                        "orders_threshold": Or(float, int, None),
                        "orders": Or(float, int, None),
                        "invalid_cancel_orders": Or(float, int, None),
                        "cancel_ratio_threshold": Or(float, int, None),
                        "cancel_ratio": Or(float, int, None),
                        "is_trigger": Or(float, int, None),
                        "is_active": Or(float, int, None)
                    },
                    "TDN":
                        {
                            "disables_threshold": Or(float, int, None),
                            "disables": Or(float, int, None),
                            "is_trigger": Or(float, int, None),
                            "is_active": Or(float, int, None)
                        }
                },
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('查询用户品种实际可用杠杆倍数')
    def test_swap_available_level_rate(self, contract_code):
        r = t.swap_available_level_rate(contract_code=contract_code)
        schema = {
            "status": "ok",
            "data": [
                {
                    "contract_code": str,
                    "available_level_rate": str
                }
            ],
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('获取基差数据')
    def test_swap_basis(self, contract_code):
        r = t.swap_basis(contract_code=contract_code, period='1min', basis_price_type='open', size='20')
        schema = {
            "ch": str,
            "data": [{
                "basis": Or(float, int, None),
                "basis_rate": Or(float, int, None),
                "contract_price": Or(float, int, None),
                "id": Or(float, int, None),
                "index_price": Or(float, int, None),
            }],
            "status": "ok",
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('批量获取合约的资金费率')
    def test_swap_batch_funding_rate(self, contract_code):
        r = t.swap_batch_funding_rate(contract_code=contract_code)
        schema = {
            "status": "ok",
            "data": [
                {
                    "symbol": str,
                    "contract_code": contract_code,
                    "fee_asset": str,
                    "funding_time": str,
                    "funding_rate": str,
                    "estimated_rate": str,
                    "next_funding_time": str
                }
            ],
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('批量获取聚合行情')
    def test_swap_batch_merged(self, contract_code):
        r = t.swap_batch_merged(contract_code=contract_code)
        schema = {
            'status': 'ok',
            'ticks': [{
                'contract_code': contract_code,
                'amount': str,
                'ask': list,
                'bid': list,
                'close': str,
                'count': int,
                'high': str,
                'id': int,
                'low': str,
                'open': str,
                'ts': int,
                'vol': str
            }],
            'ts': int
        }
        Schema(schema).validate(r)

    @allure.feature('合约批量下单')
    def test_swap_batchorder(self, contract_code):
        r = t.swap_batchorder({"orders_data": [{
            "contract_code": contract_code,
            "client_order_id": '',
            "price": '1',
            "volume": '1',
            "direction": 'buy',
            "offset": 'open',
            "lever_rate": '5',
            "order_price_type": 'limit'},
            {
                "contract_code": contract_code,
                "client_order_id": '',
                "price": '2',
                "volume": '1',
                "direction": 'buy',
                "offset": 'open',
                "lever_rate": '5',
                "order_price_type": 'limit'}]})

        schema = {
            "status": "ok",
            "data": {
                "errors": [
                    {
                        "index": int,
                        "err_code": int,
                        "err_msg": str
                    }
                ],
                "success": [
                    {
                        # "client_order_id": int,
                        "index": int,
                        "order_id": int,
                        "order_id_str": str
                    }
                ]
            },
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('获取市场最优挂单')
    def test_swap_bbo(self, contract_code):
        r = t.swap_bbo(contract_code=contract_code)
        schema = {
            'status': 'ok',
            'ticks': [{
                'contract_code': contract_code,
                'ask': list,
                'bid': list,
                'mrid': int,
                'ts': int
            }],
            'ts': int}

        Schema(schema).validate(r)

    @allure.feature('撤销订单')
    def test_swap_cancel(self, contract_code):
        a = t.swap_order(contract_code=contract_code,
                         client_order_id='',
                         price='1',
                         volume='1',
                         direction='buy',
                         offset='open',
                         lever_rate='5',
                         order_price_type='limit')
        time.sleep(1)
        r = t.swap_cancel(contract_code=contract_code,
                          order_id=a['data']['order_id'])
        schema = {
            "status": "ok",
            "data": {
                "errors": [
                    {
                        "order_id": str,
                        "err_code": int,
                        "err_msg": str
                    }
                ],
                "successes": str
            },
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('全部撤单')
    def test_swap_cancelall(self, contract_code):
        i = 0
        while i < 12:
            i += 1
            t.swap_order(contract_code=contract_code,
                         client_order_id='',
                         price='1',
                         volume='1',
                         direction='buy',
                         offset='open',
                         lever_rate='5',
                         order_price_type='limit')
        time.sleep(1)
        r = t.swap_cancelall(contract_code=contract_code)
        schema = {
            "status": "ok",
            "data": {
                "errors": [
                    {
                        "order_id": str,
                        "err_code": int,
                        "err_msg": str
                    }
                ],
                "successes": str
            },
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('获取合约信息')
    def test_swap_contract_info(self, contract_code):
        r = t.swap_contract_info(contract_code=contract_code)
        schema = {
            "status": "ok",
            "data": [
                {
                    "symbol": str,
                    "contract_code": contract_code,
                    "contract_size": Or(float, int, None),
                    "price_tick": Or(float, int, None),
                    "settlement_date": str,
                    "delivery_time": str,
                    "create_date": str,
                    "contract_status": Or(float, int, None)
                }
            ],
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('获取行情深度数据')
    def test_swap_depth(self, contract_code):
        r = t.swap_depth(contract_code=contract_code, type='step0')
        schema = {
            'ch': str,
            'status': 'ok',
            'tick': {
                'asks': list,
                'bids': list,
                'ch': str,
                'id': int,
                'mrid': int,
                'ts': int,
                'version': int
            },
            'ts': int
        }
        Schema(schema).validate(r)

    @allure.feature('获取聚合行情')
    def test_swap_detail_merged(self, contract_code):
        r = t.swap_detail_merged(contract_code=contract_code)
        schema = {
            'ch': str,
            'status': 'ok',
            'tick': {
                'amount': str,
                'ask': list,
                'bid': list,
                'close': str,
                'count': int,
                'high': str,
                'id': int,
                'low': str,
                'open': str,
                'ts': int,
                'vol': str
            },
            'ts': int
        }
        Schema(schema).validate(r)

    @allure.feature('精英账户多空持仓对比-账户数')
    def test_swap_elite_account_ratio(self, contract_code):
        r = t.swap_elite_account_ratio(contract_code=contract_code, period='60min')
        pprint(r)
        schema = {
            "status": "ok",
            "data":
                {
                    "symbol": str,
                    "contract_code": contract_code,
                    "list": [
                        {
                            "buy_ratio": Or(float, int, None),
                            "sell_ratio": Or(float, int, None),
                            "locked_ratio": Or(float, int, None),
                            "ts": int
                        }
                    ]
                },
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('精英账户多空持仓对比-持仓量')
    def test_swap_elite_position_ratio(self, contract_code):
        r = t.swap_elite_position_ratio(contract_code=contract_code, period='12hour')
        schema = {
            "status": "ok",
            "data": {
                "symbol": str,
                "contract_code": contract_code,
                "list": [
                    {
                        "buy_ratio": Or(float, int, None),
                        "sell_ratio": Or(float, int, None),
                        "ts": int
                    }
                ]
            },
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('获取预估结算价')
    def test_swap_estimated_rate_kline(self, contract_code):
        r = t.swap_estimated_settlement_price(contract_code=contract_code)
        schema = {
            "status": "ok",
            "data": [{
                "contract_code": contract_code,
                "estimated_settlement_price": Or(float, int, None),
                "settlement_type": 'settlement'
            }],
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('获取预测资金费率的K线')
    def test_swap_estimated_rate_kline(self, contract_code):
        schema = {
            "ch": str,
            "data": [
                {
                    "vol": str,
                    "close": str,
                    "count": str,
                    "high": str,
                    "id": int,
                    "low": str,
                    "open": str,
                    "amount": str
                }
            ],
            "status": "ok",
            "ts": int
        }
        r = t.swap_estimated_rate_kline(contract_code=contract_code, period='1min', size='20')
        Schema(schema).validate(r)

    @allure.feature('查询用户当前的手续费费率')
    def test_swap_fee(self, contract_code):
        r = t.swap_fee(contract_code=contract_code)
        schema = {
            "status": "ok",
            "data": [
                {
                    "symbol": str,
                    "contract_code": contract_code,
                    "fee_asset": str,
                    "open_maker_fee": str,
                    "open_taker_fee": str,
                    "close_maker_fee": str,
                    "close_taker_fee": str,
                }
            ],
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('查询用户财务记录')
    def test_swap_financial_record(self, contract_code):
        r = t.swap_financial_record(contract_code=contract_code, type='0', create_date='90', page_index='',
                                    page_size='')
        schema = {
            "status": "ok",
            "data": {
                "financial_record": [
                    {
                        "id": int,
                        "ts": int,
                        "symbol": str,
                        "contract_code": contract_code,
                        "type": int,
                        "amount": int,
                    }
                ],
                "total_page": int,
                "current_page": int,
                "total_size": int
            },
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('组合查询用户财务记录')
    def test_swap_financial_record_exact(self, contract_code):
        r = t.swap_financial_record_exact(contract_code=contract_code, type='5', start_time='', end_time='', from_id='',
                                          size='', direct='')
        schema = {
            "status": "ok",
            "data": {
                "financial_record": [
                    {
                        "id": Or(float, int, None),
                        "ts": Or(float, int, None),
                        "symbol": str,
                        "contract_code": contract_code,
                        "type": Or(float, int, None),
                        "amount": Or(float, int, None)
                    }
                ],
                "remain_size": Or(float, int, None),
                "next_id": Or(float, int, None),
            },
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('获取合约的资金费率')
    def test_swap_funding_rate(self, contract_code):
        r = t.swap_funding_rate(contract_code=contract_code)
        schema = {
            "status": "ok",
            "data":
                {
                    "symbol": str,
                    "contract_code": contract_code,
                    "fee_asset": str,
                    "funding_time": str,
                    "funding_rate": str,
                    "estimated_rate": str,
                    "next_funding_time": str
                }
            ,
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('平台持仓量的查询')
    def test_swap_his_open_interest(self, contract_code):
        r = t.swap_his_open_interest(contract_code=contract_code, period='60min', size='20', amount_type='1')
        schema = {
            "status": "ok",
            "data":
                {
                    "symbol": str,
                    "contract_code": contract_code,
                    "tick": [
                        {
                            "volume": Or(int, float, None),
                            "amount_type": int,
                            "ts": int
                        }
                    ]
                },
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('获取合约历史委托')
    def test_swap_hisorders(self, contract_code):
        r = t.swap_hisorders(contract_code=contract_code,
                             trade_type='0',
                             type='1',
                             status='0',
                             create_date='7',
                             page_index='',
                             page_size='')
        schema = {
            "status": "ok",
            "data": {
                "orders": [
                    {
                        "symbol": str,
                        "contract_code": contract_code,
                        "volume": Or(int, float, None),
                        "price": Or(int, float, None),
                        "order_price_type": Or(int, float, None),
                        "direction": str,
                        "offset": str,
                        "lever_rate": Or(int, float, None),
                        "order_id": Or(int, float, None),
                        "order_id_str": str,
                        "order_source": "api",
                        "create_date": int,
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
                        "order_type": int,
                        "update_time": int,
                        "is_tpsl": Or(int, float, None)
                    }
                ],
                "total_page": int,
                "current_page": int,
                "total_size": int
            },
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('组合查询合约历史委托')
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

    @allure.feature('获取合约的历史资金费率')
    def test_swap_historical_funding_rate(self, contract_code):
        r = t.swap_historical_funding_rate(contract_code=contract_code, page_index='', page_size='')
        schema = {
            "data": {
                "current_page": int,
                "data": [
                    {
                        "avg_premium_index": str,
                        "contract_code": contract_code,
                        "fee_asset": str,
                        "funding_rate": str,
                        "funding_time": str,
                        "realized_rate": str,
                        "symbol": str
                    }
                ],
                "total_page": int,
                "total_size": int
            },
            "status": "ok",
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('获取指数的K线数据')
    def test_swap_history_index(self, contract_code):
        r = t.swap_history_index(symbol=contract_code, period='1min', size='1')
        schema = {
            "ch": str,
            "status": "ok",
            "ts": int,
            "data": [
                {
                    "id": Or(int, None),
                    "vol": Or(int, float, None),
                    "count": Or(int, float, None),
                    "open": Or(int, float, None),
                    "close": Or(int, float, None),
                    "low": Or(int, float, None),
                    "high": Or(int, float, None),
                    "amount": Or(int, float, None)
                }
            ]
        }
        Schema(schema).validate(r)

    @allure.feature('批量获取最近的交易记录')
    def test_swap_history_trade(self, contract_code):
        r = t.swap_history_trade(contract_code=contract_code, size='1')
        schema = {
            "ch": str,
            "status": "ok",
            "ts": int,
            "data": [
                {
                    "id": Or(int, None),
                    "ts": int,
                    "data": [
                        {
                            "amount": Or(int, float),
                            "quantity": Or(int, float, None),
                            "direction": str,
                            "id": Or(int, None),
                            "price": Or(int, float),
                            "ts": int
                        }
                    ]
                }
            ]
        }
        Schema(schema).validate(r)

    @allure.feature('获取合约指数信息')
    def test_swap_index(self, contract_code):
        r = t.swap_index(contract_code=contract_code)
        schema = {
            "status": "ok",
            "data": [
                {
                    "contract_code": contract_code,
                    "index_price": Or(int, float),
                    "index_ts": int
                }
            ],
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('查询合约风险准备金余额历史数据')
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

    @allure.feature('获取K线数据')
    def test_swap_kline(self, contract_code):
        r = t.swap_kline(contract_code=contract_code, period='1min', size='20', From='', to='')
        schema = {
            "ch": str,
            "data": [
                {
                    "vol": Or(int, float),
                    "close": Or(int, float),
                    "count": Or(int, float),
                    "high": Or(int, float),
                    "id": Or(int, float),
                    "low": Or(int, float),
                    "open": Or(int, float),
                    "amount": Or(int, float)
                }
            ],
            "status": "ok",
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('获取平台阶梯保证金')
    def test_swap_ladder_margin(self, contract_code):
        r = t.swap_ladder_margin(contract_code=contract_code)
        schema = {
            "status": "ok",
            "data": [{
                "symbol": str,
                "contract_code": contract_code,
                "list": [{
                    "lever_rate": Or(int, float),
                    "ladders": [{
                        "min_margin_balance": Or(int, float, None),
                        "max_margin_balance": Or(int, float, None),
                        "min_margin_available": Or(int, float, None),
                        "max_margin_available": Or(int, float, None)
                    }
                    ]
                }]
            }],
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('闪电平仓下单')
    def test_swap_lightning_close_position(self, contract_code):
        t.swap_order(contract_code=contract_code,
                     client_order_id='',
                     price='',
                     volume='1',
                     direction='buy',
                     offset='open',
                     lever_rate='150',
                     order_price_type='opponent')

        r = t.swap_lightning_close_position(contract_code=contract_code,
                                            volume='1',
                                            direction='sell',
                                            client_order_id='',
                                            order_price_type='')
        schema = {
            "status": "ok",
            "data": {
                "order_id": int,
                "order_id_str": str
                #   "client_order_id": int
            },
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('获取强平订单')
    def test_swap_liquidation_orders(self, contract_code):
        r = t.swap_liquidation_orders(contract_code=contract_code, trade_type='0', create_date='7', page_index='',
                                      page_size='')
        schema = {
            "status": "ok",
            "data": {
                "orders": [
                    {
                        "symbol": str,
                        "contract_code": contract_code,
                        "direction": str,
                        "offset": str,
                        "volume": Or(float, int),
                        "price": Or(float, int),
                        "created_at": int,
                    }
                ],
                "total_page": int,
                "current_page": int,
                "total_size": int
            },
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('获取标记价格的K线数据')
    def test_swap_mark_price_kline(self, contract_code):
        r = t.swap_mark_price_kline(contract_code=contract_code, period='1min', size='20')
        schema = {
            "ch": str,
            "data": [
                {
                    "vol": str,
                    "close": str,
                    "count": str,
                    "high": str,
                    "id": int,
                    "low": str,
                    "open": str,
                    "trade_turnover": str,
                    "amount": str
                }
            ],
            "status": "ok",
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('母子账户划转')
    def test_swap_master_sub_transfer(self, sub_uid, contract_code):
        r = t.swap_master_sub_transfer(sub_uid=sub_uid, contract_code=contract_code, amount='1', type='master_to_sub')
        schema = {'data': {'order_id': str},
                  'status': 'ok',
                  'ts': int}
        Schema(schema).validate(r)

    @allure.feature('获取母账户下的所有母子账户的划转记录')
    def test_swap_master_sub_transfer_record(self, contract_code):
        r = t.swap_master_sub_transfer_record(contract_code=contract_code, transfer_type='34', create_date='7',
                                              page_index='', page_size='')
        schema = {
            'data': {
                'current_page': int,
                'total_page': int,
                'total_size': int,
                'transfer_record': [{
                    'amount': float,
                    'contract_code': contract_code,
                    'id': int,
                    'sub_account_name': str,
                    'sub_uid': str,
                    'symbol': str,
                    'transfer_type': int,
                    'ts': int
                }]
            },
            'status': 'ok',
            'ts': int
        }
        Schema(schema).validate(r)

    @allure.feature('获取历史成交记录')
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

    @allure.feature('组合查询用户历史成交记录')
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

    @allure.feature('量获取当前可用合约总持仓')
    def test_swap_open_interest(self, contract_code):
        r = t.swap_open_interest(contract_code=contract_code)
        schema = {
            "status": "ok",
            "data":
                [{
                    "symbol": "BTC",
                    "volume": Or(float, int),
                    "amount": Or(float, int),
                    "trade_amount": Or(float, int),
                    "trade_volume": Or(float, int),
                    "trade_turnover": Or(float, int),
                    "contract_code": "BTC-USD"
                }],
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('获取合约当前未成交委托')
    def test_swap_openorders(self, contract_code):
        t.swap_order(contract_code=contract_code,
                     client_order_id='',
                     price='50000',
                     volume='1',
                     direction='buy',
                     offset='open',
                     lever_rate='5',
                     order_price_type='limit')
        time.sleep(1)

        r = t.swap_openorders(contract_code=contract_code,
                              page_size='',
                              page_index='')
        schema = {
            'data': {
                'current_page': 1,
                'orders': [{
                    'canceled_at': Or(int, None),
                    'client_order_id': Or(str, None),
                    'contract_code': 'BTC-USD',
                    'created_at': int,
                    'direction': str,
                    'fee': 0,
                    'fee_asset': 'BTC',
                    'is_tpsl': int,
                    'lever_rate': Or(float, int),
                    'liquidation_type': Or(int, None),
                    'margin_frozen': Or(float, int),
                    'offset': str,
                    'order_id': int,
                    'order_id_str': str,
                    'order_price_type': str,
                    'order_source': str,
                    'order_type': int,
                    'price': Or(float, int),
                    'profit': Or(float, int),
                    'real_profit': Or(float, int),
                    'status': int,
                    'symbol': 'BTC',
                    'trade_avg_price': Or(float, int, None),
                    'trade_turnover': Or(float, int),
                    'trade_volume': Or(float, int),
                    'update_time': int,
                    'volume': Or(float, int)
                }],
                'total_page': int,
                'total_size': int
            },
            'status': 'ok',
            'ts': int
        }
        Schema(schema).validate(r)

    @allure.feature('合约下单')
    def test_swap_order(self, contract_code):
        r = t.swap_order(contract_code=contract_code,
                         client_order_id='',
                         price='50000',
                         volume='1',
                         direction='buy',
                         offset='open',
                         lever_rate='5',
                         order_price_type='limit')
        schema = {
            "status": "ok",
            "data": {
                "order_id": int,
                "order_id_str": str
            },
            "ts": int
        }
        pprint(r)
        Schema(schema).validate(r)

    @allure.feature('获取订单明细信息')
    def test_swap_order_detail(self, contract_code):
        a = t.swap_order(contract_code=contract_code,
                         client_order_id='',
                         price='50000',
                         volume='1',
                         direction='buy',
                         offset='open',
                         lever_rate='5',
                         order_price_type='limit')
        time.sleep(2)
        created_at = a['ts']
        order_id = a['data']['order_id']

        r = t.swap_order_detail(contract_code=contract_code,
                                order_id=order_id,
                                created_at=created_at,
                                order_type='1',
                                page_index='',
                                page_size='')
        schema = {
            "status": "ok",
            "data": {
                "symbol": str,
                "contract_code": contract_code,
                "volume": Or(float, int, None),
                "price": Or(float, int, None),
                "order_price_type": str,
                "direction": str,
                "offset": str,
                "lever_rate": Or(float, int, None),
                "margin_frozen": Or(float, int, None),
                "profit": Or(float, int, None),
                "real_profit": Or(float, int, None),
                "order_source": str,
                "created_at": int,
                "canceled_at": int,
                "instrument_price": Or(float, int, None),
                "final_interest": Or(float, int, None),
                "adjust_value": Or(float, int, None),
                "fee": Or(float, int, None),
                "fee_asset": str,
                "liquidation_type": str,
                "order_id": Or(float, int, None),
                "order_id_str": str,
                "client_order_id": Or(float, int, None),
                "order_type": str,
                "status": int,
                "trade_avg_price": Or(float, int, None),
                "trade_turnover": Or(float, int, None),
                "trade_volume": Or(float, int, None),
                "is_tpsl": Or(float, int, None),
                "trades": [
                    {
                        "trade_id": Or(float, int, None),
                        "id": Or(str, None),
                        "trade_volume": Or(float, int, None),
                        "trade_price": Or(float, int, None),
                        "trade_fee": Or(float, int, None),
                        "fee_asset": str,
                        "trade_turnover": Or(float, int, None),
                        "role": str,
                        "profit": Or(float, int, None),
                        "real_profit": Or(float, int, None),
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

    @allure.feature('获取合约订单信息')
    def test_swap_order_info(self, contract_code):
        a = t.swap_order(contract_code=contract_code,
                         client_order_id='',
                         price='50000',
                         volume='1',
                         direction='buy',
                         offset='open',
                         lever_rate='5',
                         order_price_type='limit')

        r = t.swap_order_info(contract_code=contract_code,
                              order_id=a['data']['order_id'],
                              client_order_id='')
        schema = {
            'data': [{
                'symbol': 'BTC',
                'contract_code': 'BTC-USD',
                'created_at': int,
                'direction': str,
                'fee': Or(float, int),
                'fee_asset': 'BTC',
                'lever_rate': Or(float, int),
                'margin_frozen': Or(float, int),
                'offset': str,
                'order_id': Or(float, int),
                'order_id_str': str,
                'client_order_id': Or(str, None),
                'order_price_type': str,
                'order_source': str,
                'order_type': Or(float, int),
                'price': Or(float, int),
                'profit': Or(float, int),
                'real_profit': Or(float, int),
                'status': Or(float, int),
                'trade_avg_price': Or(float, int, None),
                'trade_turnover': Or(float, int),
                'trade_volume': Or(float, int),
                'volume': Or(float, int),
                'liquidation_type': str,
                'canceled_at': int,
                'update_time': Or(int, None),
                "is_tpsl": int
            }],
            'status': 'ok',
            'ts': int
        }
        Schema(schema).validate(r)

    @allure.feature('查询用户当前的下单量限制')
    def test_swap_order_limit(self, contract_code):
        r = t.swap_order_limit(contract_code=contract_code,
                               order_price_type='limit')
        schema = {
            "status": "ok",
            "data": {
                "order_price_type": str,
                "list": [
                    {
                        "symbol": "BTC",
                        "contract_code": "BTC-USD",
                        "open_limit": Or(float, int),
                        "close_limit": Or(float, int)
                    }
                ]
            },
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('获取用户持仓信息')
    def test_swap_position_info(self, contract_code):
        r = t.swap_position_info(contract_code=contract_code)
        schema = {
            "status": "ok",
            "data": [
                {
                    "symbol": "BTC",
                    "contract_code": "BTC-USD",
                    "volume": Or(float, int),
                    "available": Or(float, int),
                    "frozen": Or(float, int),
                    "cost_open": Or(float, int),
                    "cost_hold": Or(float, int),
                    "profit_unreal": Or(float, int),
                    "profit_rate": Or(float, int),
                    "profit": Or(float, int),
                    "position_margin": Or(float, int),
                    "lever_rate": Or(float, int),
                    "direction": str,
                    "last_price": Or(float, int)
                }
            ],
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('用户持仓量限制的查询')
    def test_swap_position_limit(self, contract_code):
        r = t.swap_position_limit(contract_code=contract_code)
        schema = {
            "status": "ok",
            "data": [
                {
                    "symbol": "BTC",
                    "contract_code": "BTC-USD",
                    "buy_limit": Or(float, int),
                    "sell_limit": Or(float, int)
                }
            ],
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('获取溢价指数K线')
    def test_swap_premium_index_kline(self, contract_code):
        r = t.swap_premium_index_kline(contract_code=contract_code, period='1min', size='20')
        schema = {
            "ch": str,
            "data": [
                {
                    "vol": str,
                    "close": str,
                    "count": str,
                    "high": str,
                    "id": int,
                    "low": str,
                    "open": str,
                    "amount": str
                }
            ],
            "status": "ok",
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('获取合约最高限价和最低限价')
    def test_swap_price_limit(self, contract_code):
        r = t.swap_price_limit(contract_code=contract_code)
        schema = {
            "status": "ok",
            "data":
                [{
                    "symbol": "BTC",
                    "high_limit": Or(float, int),
                    "low_limit": Or(float, int),
                    "contract_code": "BTC-USD"
                }],
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('查询开仓单关联的止盈止损订单详情')
    def test_swap_relation_tpsl_order(self, contract_code):
        a = t.swap_order(contract_code=contract_code,
                         client_order_id='',
                         price='50000',
                         volume='1',
                         direction='buy',
                         offset='open',
                         lever_rate='5',
                         order_price_type='limit')
        r = t.swap_relation_tpsl_order(contract_code=contract_code, order_id=a['data']['order_id'])
        schema = {
            "status": "ok",
            "data": {
                "symbol": "BTC",
                "contract_code": "BTC-USD",
                "volume": int,
                "price": Or(int, float),
                "order_price_type": str,
                "direction": str,
                "offset": str,
                "lever_rate": int,
                "order_id": int,
                "order_id_str": str,
                "client_order_id": Or(int, None),
                "created_at": int,
                "trade_volume": int,
                "trade_turnover": Or(int, float),
                "fee": Or(int, float),
                "trade_avg_price": Or(int, float, None),
                "margin_frozen": float,
                "profit": Or(float, int),
                "status": int,
                "order_type": int,
                "order_source": str,
                "fee_asset": "BTC",
                # "liquidation_type": str,
                "canceled_at": int,
                "tpsl_order_info": [{
                    "volume": int,
                    "tpsl_order_type": str,
                    "direction": str,
                    "order_id": int,
                    "order_id_str": str,
                    "trigger_type": str,
                    "trigger_price": float,
                    "order_price": float,
                    "created_at": int,
                    "order_price_type": str,
                    "relation_tpsl_order_id": str,
                    "status": int,
                    "canceled_at": Or(int, None),
                    "fail_code": Or(int, None),
                    "fail_reason": Or(str, None),
                    "triggered_price": Or(float, None),
                    "relation_order_id": str
                }],
            },
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('查询合约风险准备金余额和预估分摊比例')
    def test_swap_risk_info(self, contract_code):
        r = t.swap_risk_info(contract_code=contract_code)
        schema = {
            "status": "ok",
            "ts": int,
            "data": [
                {
                    "contract_code": "BTC-USD",
                    "insurance_fund": float,
                    "estimated_clawback": float
                }
            ]
        }
        Schema(schema).validate(r)

    @allure.feature('获取平台历史结算记录')
    def test_swap_settlement_records(self, contract_code):
        r = t.swap_settlement_records(contract_code=contract_code)
        schema = {
            "status": "ok",
            "ts": int,
            "data": {
                "settlement_record": [
                    {
                        "symbol": "BTC",
                        "contract_code": "BTC-USD",
                        "settlement_time": int,
                        "clawback_ratio": Or(float, 0),
                        "settlement_price": float,
                        "settlement_type": "settlement"
                    }
                ],
                "current_page": int,
                "total_page": int,
                "total_size": int
            }
        }
        Schema(schema).validate(r)

    @allure.feature('查询单个子账户资产信息')
    def test_swap_sub_account_info(self, sub_uid, contract_code):
        r = t.swap_sub_account_info(contract_code=contract_code, sub_uid=sub_uid)
        schema = {
            "status": "ok",
            "data": [
                {
                    "symbol": "BTC",
                    "contract_code": "BTC-USD",
                    "margin_balance": float,
                    "margin_position": Or(float, 0),
                    "margin_frozen": Or(float, 0),
                    "margin_available": float,
                    "profit_real": float,
                    "profit_unreal": Or(float, 0),
                    "withdraw_available": float,
                    "risk_rate": Or(float, None),
                    "liquidation_price": Or(float, None),
                    "adjust_factor": float,
                    "lever_rate": int,
                    "transfer_profit_ratio": Or(float, None),
                    "margin_static": float
                }
            ],
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('批量获取子账户资产信息')
    def test_swap_sub_account_info_list(self, contract_code):
        r = t.swap_sub_account_info_list(contract_code=contract_code)
        schema = {
            "status": "ok",
            "ts": int,
            "data": {
                "current_page": int,
                "total_page": int,
                "total_size": int,
                "sub_list": [{
                    "sub_uid": int,
                    "account_info_list": [{
                        "symbol": "BTC",
                        "contract_code": "BTC-USD",
                        "margin_balance": Or(float, 0),
                        "liquidation_price": Or(float, None),
                        "risk_rate": Or(float, None)
                    }
                    ]
                }]
            }
        }
        Schema(schema).validate(r)

    @allure.feature('查询母账户下所有子账户资产信息')
    def test_swap_sub_account_list(self, contract_code):
        r = t.swap_sub_account_list(contract_code=contract_code)
        schema = {
            "status": "ok",
            "ts": int,
            "data": [
                {
                    "sub_uid": int,
                    "list": [
                        {
                            "symbol": str,
                            "contract_code": str,
                            "margin_balance": Or(float, 0),
                            "liquidation_price": Or(float, None),
                            "risk_rate": Or(float, None)
                        }
                    ]
                }
            ]
        }
        Schema(schema).validate(r)

    @allure.feature('批量设置子账户交易权限')
    def test_swap_sub_auth(self, sub_uid):
        r = t.swap_sub_auth(sub_uid=sub_uid, sub_auth='1')
        schema = {
            "status": "ok",
            "data": {
                "errors": [
                    {
                        "sub_uid": str,
                        "err_code": int,
                        "err_msg": str
                    }
                ],
                "successes": str
            },
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('查询单个子账户持仓信息')
    def test_swap_sub_position_info(self, contract_code, sub_uid):
        r = t.swap_sub_position_info(contract_code=contract_code, sub_uid=sub_uid)
        schema = {
            "status": "ok",
            "ts": int,
            "data": [
                {
                    "symbol": "BTC",
                    "contract_code": "BTC-USD",
                    "volume": float,
                    "available": float,
                    "frozen": float,
                    "cost_open": float,
                    "cost_hold": float,
                    "profit_unreal": float,
                    "profit_rate": float,
                    "profit": float,
                    "position_margin": float,
                    "lever_rate": int,
                    "direction": str,
                    "last_price": float
                }
            ]
        }
        Schema(schema).validate(r)

    @allure.feature('切换杠杆倍数')
    def test_swap_switch_lever_rate(self, contract_code):
        r = t.swap_switch_lever_rate(contract_code=contract_code, lever_rate='5')
        schema = {
            "status": "ok",
            "ts": int,
            "data": {
                "contract_code": str,
                "lever_rate": int
            }
        }
        Schema(schema).validate(r)

    @allure.feature('止盈止损订单撤单')
    def test_swap_tpsl_order(self, contract_code):
        a = t.swap_tpsl_order(contract_code=contract_code,
                              direction='buy',
                              volume='1',
                              tp_trigger_price='20000',
                              tp_order_price_type='limit',
                              tp_order_price='20000')
        r = t.swap_tpsl_cancel(contract_code=contract_code,
                               order_id=a['data']['tp_order']['order_id'])
        schema = {
            'status': 'ok',
            'ts': int,
            'data': {
                'errors': [{
                    'err_code': int,
                    'err_msg': str,
                    'order_id': str
                }],
                'successes': str
            }
        }
        Schema(schema).validate(r)

    @allure.feature('止盈止损订单全部撤单')
    def test_swap_tpsl_cancelall(self, contract_code):
        t.swap_tpsl_order(contract_code=contract_code,
                          direction='buy',
                          volume='1',
                          tp_trigger_price='40000',
                          tp_order_price_type='limit',
                          tp_order_price='50000')
        r = t.swap_tpsl_cancelall(contract_code=contract_code)
        schema = {
            "status": "ok",
            "data": {
                "errors": [{
                    'err_code': int,
                    'err_msg': str,
                    'order_id': str
                }],
                "successes": str
            },
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('查询止盈止损订单历史委托')
    def test_swap_tpsl_hisorders(self, contract_code):
        r = t.swap_tpsl_hisorders(contract_code=contract_code, status='0', create_date='7')
        schema = {
            "status": "ok",
            "data": {
                "total_page": int,
                "total_size": int,
                "current_page": int,
                "orders": [{
                    "symbol": "BTC",
                    "contract_code": "BTC-USD",
                    "volume": float,
                    "order_type": int,
                    "direction": str,
                    "tpsl_order_type": str,
                    "order_id": int,
                    "order_id_str": str,
                    "order_source": str,
                    "order_price": float,
                    "created_at": int,
                    "order_price_type": str,
                    "trigger_type": str,
                    "trigger_price": Or(int, float),
                    "status": int,
                    "source_order_id": Or(str, None),
                    "relation_tpsl_order_id": str,
                    "canceled_at": Or(int, None),
                    "fail_code": Or(str, None),
                    "fail_reason": Or(str, None),
                    "triggered_price": Or(float, None),
                    "relation_order_id": str,
                    "update_time": int
                }]
            },
            "ts": int
        }

        Schema(schema).validate(r)

    @allure.feature('查询止盈止损订单当前委托')
    def test_swap_tpsl_openorders(self, contract_code):
        t.swap_tpsl_order(contract_code=contract_code,
                          direction='buy',
                          volume='1',
                          tp_trigger_price='20000',
                          tp_order_price_type='limit',
                          tp_order_price='20000')
        r = t.swap_tpsl_openorders(contract_code=contract_code)
        schema = {
            "status": "ok",
            "data": {
                "total_page": int,
                "total_size": int,
                "current_page": int,
                "orders": [{
                    "symbol": "BTC",
                    "contract_code": "BTC-USD",
                    "volume": float,
                    "order_type": int,
                    "tpsl_order_type": str,
                    "direction": str,
                    "order_id": int,
                    "order_id_str": str,
                    "order_source": str,
                    "order_price": float,
                    "trigger_type": str,
                    "trigger_price": float,
                    "created_at": int,
                    "order_price_type": str,
                    "status": int,
                    "source_order_id": Or(str, None),
                    "relation_tpsl_order_id": str
                }]
            },
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('对仓位设置止盈止损订单')
    def test_swap_tpsl_order(self, contract_code):
        r = t.swap_tpsl_order(contract_code=contract_code,
                              direction='buy',
                              volume='1',
                              tp_trigger_price='20000',
                              tp_order_price_type='limit',
                              tp_order_price='20000')
        schema = {
            "status": "ok",
            "data": {
                "tp_order": {
                    "order_id": int,
                    "order_id_str": str
                },
                "sl_order": Or({
                    "order_id": int,
                    "order_id_str": str
                }, None)
            },
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('跟踪委托撤单')
    def test_swap_track_cancel(self, contract_code):
        a = t.swap_track_order(contract_code=contract_code,
                               direction='buy',
                               offset='open',
                               lever_rate='5',
                               volume='1',
                               callback_rate='0.01',
                               active_price='20000',
                               order_price_type='formula_price')
        r = t.swap_track_cancel(contract_code=contract_code,
                                order_id=a['data']['order_id'])
        schema = {
            'status': 'ok',
            'ts': int,
            'data': {
                'errors': [{
                    'err_code': int,
                    'err_msg': str,
                    'order_id': str
                }],
                'successes': str
            }
        }
        Schema(schema).validate(r)

    @allure.feature('跟踪委托全部撤单')
    def test_swap_track_cancelall(self, contract_code):
        t.swap_track_order(contract_code=contract_code,
                           direction='buy',
                           offset='open',
                           lever_rate='5',
                           volume='1',
                           callback_rate='0.01',
                           active_price='20000',
                           order_price_type='formula_price')
        time.sleep(2)
        r = t.swap_track_cancelall(contract_code=contract_code)
        schema = {
            "status": "ok",
            "data": {
                "errors": [{
                    'err_code': int,
                    'err_msg': str,
                    'order_id': str
                }],
                "successes": str
            },
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('获取跟踪委托历史委托')
    def test_swap_track_hisorders(self, contract_code):
        r = t.swap_track_hisorders(contract_code=contract_code, status='0', trade_type='0', create_date='7')
        schema = {
            "status": "ok",
            "data": {
                "total_page": int,
                "total_size": int,
                "current_page": int,
                "orders": [{
                    "symbol": "BTC",
                    "contract_code": "BTC-USD",
                    "triggered_price": Or(str, None),
                    "volume": float,
                    "order_type": int,
                    "direction": str,
                    "offset": str,
                    "lever_rate": int,
                    "order_id": int,
                    "order_id_str": str,
                    "order_source": str,
                    "created_at": int,
                    "update_time": int,
                    "order_price_type": str,
                    "status": int,
                    "canceled_at": int,
                    "fail_code": Or(int, None),
                    "fail_reason": Or(str, None),
                    "callback_rate": float,
                    "active_price": float,
                    "is_active": int,
                    "market_limit_price": Or(float, None),
                    "formula_price": Or(float, None),
                    "real_volume": Or(float, 0),
                    "relation_order_id": str
                }]
            },
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('获取跟踪委托当前委托')
    def test_swap_track_openorders(self, contract_code):
        t.swap_track_order(contract_code=contract_code,
                           direction='buy',
                           offset='open',
                           lever_rate='5',
                           volume='1',
                           callback_rate='0.01',
                           active_price='20000',
                           order_price_type='formula_price')
        r = t.swap_track_openorders(contract_code=contract_code)
        schema = {
            "status": "ok",
            "data": {
                "total_page": int,
                "total_size": int,
                "current_page": int,
                "orders": [{
                    "symbol": "BTC",
                    "contract_code": "BTC-USD",
                    "volume": float,
                    "order_type": int,
                    "direction": str,
                    "offset": str,
                    "lever_rate": int,
                    "order_id": int,
                    "order_id_str": str,
                    "order_source": str,
                    "created_at": int,
                    "order_price_type": str,
                    "status": int,
                    "callback_rate": float,
                    "active_price": float,
                    "is_active": int
                }]
            },
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('跟踪委托下单')
    def test_swap_track_order(self, contract_code):
        r = t.swap_track_order(contract_code=contract_code,
                               direction='buy',
                               offset='open',
                               lever_rate='5',
                               volume='1',
                               callback_rate='0.01',
                               active_price='20000',
                               order_price_type='formula_price')
        schema = {
            "status": "ok",
            "data": {
                "order_id": int,
                "order_id_str": str
            },
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('获取市场最近成交记录')
    def test_swap_trade(self, contract_code):
        r = t.swap_trade(contract_code=contract_code)
        schema = {
            "ch": str,
            "status": "ok",
            "tick": {
                "data": [
                    {
                        "contract_code": str,
                        "amount": str,
                        "quantity": str,
                        "direction": str,
                        "id": int,
                        "price": str,
                        "ts": int
                    }
                ],
                "id": int,
                "ts": int
            },
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('查询用户当前的划转限制')
    def test_swap_transfer_limit(self, contract_code):
        r = t.swap_transfer_limit(contract_code=contract_code)
        schema = {
            "status": "ok",
            "data": [
                {
                    "symbol": "BTC",
                    "contract_code": "BTC-USD",
                    "transfer_in_max_each": float,
                    "transfer_in_min_each": float,
                    "transfer_out_max_each": float,
                    "transfer_out_min_each": float,
                    "transfer_in_max_daily": float,
                    "transfer_out_max_daily": float,
                    "net_transfer_in_max_daily": float,
                    "net_transfer_out_max_daily": float
                }
            ],
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('合约计划委托撤单')
    def test_swap_trigger_cancel(self, contract_code):
        a = t.swap_trigger_order(contract_code=contract_code,
                                 trigger_type='le',
                                 trigger_price='20000',
                                 order_price='20000',
                                 order_price_type='limit',
                                 volume='1',
                                 direction='buy',
                                 offset='open',
                                 lever_rate='5')
        time.sleep(2)

        r = t.swap_trigger_cancel(contract_code=contract_code,
                                  order_id=a['data']['order_id'])
        pprint(r)
        schema = {
            "status": "ok",
            "data": {
                "errors": [
                    {
                        "order_id": str,
                        "err_code": int,
                        "err_msg": str
                    }
                ],
                "successes": str
            },
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('合约计划委托全部撤单')
    def test_swap_trigger_cancelall(self, contract_code):
        t.swap_trigger_order(contract_code=contract_code,
                             trigger_type='le',
                             trigger_price='20000',
                             order_price='20000',
                             order_price_type='limit',
                             volume='1',
                             direction='buy',
                             offset='open',
                             lever_rate='5')
        time.sleep(1)

        r = t.swap_trigger_cancelall(contract_code=contract_code)
        schema = {
            "status": "ok",
            "data": {
                "errors": [
                    {
                        "order_id": str,
                        "err_code": int,
                        "err_msg": str
                    },
                    {
                        "order_id": str,
                        "err_code": int,
                        "err_msg": str
                    }
                ],
                "successes": str
            },
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('获取计划委托历史委托')
    def test_swap_trigger_hisorders(self, contract_code):
        r = t.swap_trigger_hisorders(contract_code=contract_code,
                                     trade_type='0',
                                     status='0',
                                     create_date='7',
                                     page_index='',
                                     page_size='')
        schema = {
            "status": "ok",
            "data": {
                "orders": [
                    {
                        "symbol": str,
                        "contract_code": str,
                        "trigger_type": str,
                        "volume": float,
                        "order_type": int,
                        "direction": str,
                        "offset": str,
                        "lever_rate": int,
                        "order_id": int,
                        "order_id_str": str,
                        "relation_order_id": str,
                        "order_price_type": str,
                        "status": int,
                        "order_source": str,
                        "trigger_price": float,
                        "triggered_price": Or(float, None),
                        "order_price": float,
                        "created_at": int,
                        "triggered_at": Or(int, None),
                        "order_insert_at": int,
                        "canceled_at": int,
                        "fail_code": Or(int, None),
                        "fail_reason": Or(str, None),
                        "update_time": int
                    }
                ],
                "total_page": int,
                "current_page": int,
                "total_size": int
            },
            "ts": int
        }
        Schema(schema).validate(r)

    @allure.feature('获取计划委托当前委托')
    def test_swap_trigger_openorders(self, contract_code):
        t.swap_trigger_order(contract_code=contract_code,
                             trigger_type='le',
                             trigger_price='50000',
                             order_price='50000',
                             order_price_type='limit',
                             volume='1',
                             direction='buy',
                             offset='open',
                             lever_rate='5')
        time.sleep(1)
        r = t.swap_trigger_openorders(contract_code=contract_code,
                                      page_index='',
                                      page_size='')

        schema = {
            "status": "ok",
            "data": {
                "orders": [
                    {
                        "symbol": "BTC",
                        "contract_code": "BTC-USD",
                        "trigger_type": "ge",
                        "volume": 4,
                        "order_type": 1,
                        "direction": "sell",
                        "offset": "open",
                        "lever_rate": 1,
                        "order_id": 23,
                        "order_id_str": "161251",
                        "order_source": "web",
                        "trigger_price": 2,
                        "order_price": 2,
                        "created_at": int,
                        "order_price_type": str,
                        "status": int
                    }],
                "total_page": int,
                "current_page": int,
                "total_size": int
            },
            "ts": int
        }

        Schema(schema).validate(r)

    @allure.feature('合约计划委托下单')
    def test_swap_trigger_order(self,contract_code):

        r = t.swap_trigger_order(contract_code=contract_code,
                                 trigger_type='le',
                                 trigger_price='20000',
                                 order_price='20000',
                                 order_price_type='limit',
                                 volume='1',
                                 direction='buy',
                                 offset='open',
                                 lever_rate='5')
        schema = {
                    "status": "ok",
                    "data": {
                        "order_id": int,
                        "order_id_str": str,
                    },
                    "ts": int
                }
        Schema(schema).validate(r)

    @allure.feature('查询用户结算记录')
    def test_swap_user_settlement_records(self, contract_code):
        r = t.swap_user_settlement_records(contract_code=contract_code, start_time='', end_time='', page_index='1',
                                           page_size='10')

        schema = {
            "status": "ok",
            "data": {
                "settlement_records": [
                    {
                        "symbol": str,
                        "contract_code": str,
                        "margin_balance_init": float,
                        "margin_balance": float,
                        "settlement_profit_real": float,
                        "settlement_time": int,
                        "clawback": float,
                        "funding_fee": float,
                        "offset_profitloss": float,
                        "fee": float,
                        "fee_asset": str,
                        "positions": [
                            {
                                "symbol": str,
                                "contract_code": str,
                                "direction": str,
                                "volume": float,
                                "cost_open": float,
                                "cost_hold_pre": float,
                                "cost_hold": float,
                                "settlement_profit_unreal": float,
                                "settlement_price": float,
                                "settlement_type": "settlement"
                            }
                        ]
                    }
                ],
                "current_page": int,
                "total_page": int,
                "total_size": int
            },
            "ts": int
        }

        Schema(schema).validate(r)
