#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/9/2
# @Author  : zhangranghan



from common.LinearServiceAPI import t
from schema import Schema,Or
from pprint import pprint
import pytest,allure,random,time



@allure.feature('正向永续字段校验')
class TestLinearSchemaCheck:

    def setup_class(self):
        self.contract_code = 'BTC-USDT'
        #最新价
        self.last_price = t.linear_history_trade(contract_code=self.contract_code,size='1')['data'][0]['data'][0]['price']
        #买一卖一价
        self.buy_price = t.linear_depth(contract_code=self.contract_code,type='step0')['tick']['bids'][0][0]
        self.sell_price = t.linear_depth(contract_code=self.contract_code,type='step0')['tick']['asks'][0][0]
        #杠杆倍数
        self.lever_rate = t.linear_account_info(contract_code=self.contract_code)['data'][0]['lever_rate']





    @allure.title('获取合约用户账户信息')
    def test_linear_account_info(self,linear_contract_code,symbol):
        r = t.linear_account_info(contract_code=linear_contract_code)
        pprint(r)
        schema = {
            'data': [
                {
                    'adjust_factor': Or(float,int),
                    'contract_code': linear_contract_code,
                    'lever_rate': int,
                    'margin_account': str,
                    'liquidation_price': Or(float,None),
                    'margin_asset': 'USDT',
                    'margin_available': Or(float,None),
                    'margin_balance': Or(float,None),
                    'margin_frozen': Or(float,None,int),
                    'margin_mode': 'isolated',
                    'margin_position': Or(float,None),
                    'margin_static': Or(float,None),
                    'profit_real': Or(float,None),
                    'profit_unreal': Or(float,None),
                    'risk_rate': Or(float,None),
                    'symbol': symbol,
                    'withdraw_available': Or(float,None)
                }
            ],
            'status': 'ok',
            'ts': int
        }

        Schema(schema).validate(r)


    @allure.title('获取合约用户账户持仓信息')
    def test_linear_account_position_info(self,linear_contract_code,symbol):
        r = t.linear_account_position_info(contract_code=linear_contract_code)
        pprint(r)
        schema = {
            'data': [
                {
                    'adjust_factor': Or(float,int),
                    'contract_code': linear_contract_code,
                    'lever_rate': int,
                    'liquidation_price': Or(float,None),
                    'margin_account': str,
                    'margin_asset': 'USDT',
                    'margin_available': Or(float,None),
                    'margin_balance': Or(float,None),
                    'margin_frozen': Or(float,None,int),
                    'margin_mode': 'isolated',
                    'margin_position': Or(float,None),
                    'margin_static': Or(float,None),
                    'positions':Or([
                        {
                            'available': Or(float,None),
                            'contract_code': str,
                            'cost_hold': Or(float,None),
                            'cost_open': Or(float,None),
                            'direction': str,
                            'frozen': Or(float,None),
                            'last_price': Or(float,None,int),
                            'lever_rate': int,
                            'margin_account': str,
                            'margin_asset': 'USDT',
                            'margin_mode': 'isolated',
                            'position_margin': Or(float,None),
                            'profit': Or(float,None),
                            'profit_rate': Or(float,None),
                            'profit_unreal': Or(float,None),
                            'symbol': symbol,
                            'volume': Or(float,None),
                        }
                    ],None),
                    'profit_real': Or(float,None),
                    'profit_unreal': Or(float,None),
                    'risk_rate': Or(float,None),
                    'symbol': symbol,
                    'withdraw_available': Or(float,None)
                }
            ],
            'status': 'ok',
            'ts': int
        }

        Schema(schema).validate(r)


    @allure.title('查询平台阶梯调整系数')
    def test_linear_adjustfactor(self,linear_contract_code,symbol):
        r = t.linear_adjustfactor(contract_code=linear_contract_code)
        pprint(r)
        schema = {
                    'data': [
                        {
                            'contract_code': linear_contract_code,
                            'list': [
                                {
                                    'ladders': [
                                        {
                                            'adjust_factor': float,
                                            'ladder': int,
                                            'max_size': Or(int,None),
                                            'min_size': Or(int,None)
                                        }
                                    ],
                                    'lever_rate': int
                                }
                            ],
                            'margin_mode': 'isolated',
                            'symbol': symbol
                        }
                    ],
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)


    @allure.title('获取用户API指标禁用信息')
    def test_linear_api_trading_status(self):
        r = t.linear_api_trading_status()
        pprint(r)
        schema = {
            'data': {
                'COR': {
                    'cancel_ratio': Or(float,int),
                    'cancel_ratio_threshold': Or(float,int),
                    'invalid_cancel_orders': int,
                    'is_active': int,
                    'is_trigger': int,
                    'orders': int,
                    'orders_threshold': int
                },
                'TDN': {
                    'disables': int,
                    'disables_threshold': int,
                    'is_active': int,
                    'is_trigger': int
                },
                'disable_interval': int,
                'disable_reason': Or(str,None),
                'is_disable': int,
                'order_price_types': Or(str,None),
                'recovery_time': int
            },
            'status': 'ok',
            'ts': int
        }

        Schema(schema).validate(r)



    @allure.title('查询用户品种实际可用杠杆倍数（逐仓）')
    def test_linear_available_level_rate(self,linear_contract_code,symbol):
        r = t.linear_available_level_rate(contract_code=linear_contract_code)
        pprint(r)
        schema = {'data': [{'available_level_rate': str,
                           'contract_code': linear_contract_code,
                           'margin_mode': 'isolated'}],
                 'status': 'ok',
                 'ts': int}

        Schema(schema).validate(r)

    @allure.title('获取基差数据')
    def test_linear_basis(self,linear_contract_code):
        r = t.linear_basis(contract_code=linear_contract_code,period='1min',basis_price_type='open',size='200')
        pprint(r)
        schema = {'ch': 'market.{}.basis.1min.open'.format(linear_contract_code),
                    'data': [{'basis': str,
                           'basis_rate':str,
                           'contract_price': str,
                           'id': int,
                           'index_price': str}],
                    'status': 'ok',
                    'ts': int}
        Schema(schema).validate(r)



    @allure.title('批量获取合约的资金费率（全逐通用）')
    def test_linear_batch_funding_rate(self,linear_contract_code,symbol):
        r = t.linear_batch_funding_rate(contract_code=linear_contract_code)
        pprint(r)
        schema = {'data': [{'contract_code': linear_contract_code,
                           'estimated_rate': str,
                           'fee_asset': 'USDT',
                           'funding_rate': str,
                           'funding_time': str,
                           'next_funding_time': str,
                           'symbol': symbol}],
                 'status': 'ok',
                 'ts': int}


        Schema(schema).validate(r)

    @allure.title('合约批量下单1')
    def test_linear_batchorder1(self,linear_contract_code):
        r = t.linear_batchorder({"orders_data": [{
                                        "contract_code": linear_contract_code,
                                        "client_order_id": '',
                                        "price": self.buy_price-1,
                                        "volume": '1',
                                        "direction": 'buy',
                                        "offset": 'open',
                                        "lever_rate": self.lever_rate,
                                        "order_price_type": 'limit'}]})
        pprint(r)
        schema = {
                    'data': {
                        'errors': [

                        ],
                        'success': [
                            {
                                'index': int,
                                'order_id': int,
                                'order_id_str': str
                            }
                        ]
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)




    @allure.title('合约批量下单2（client_order_id）')
    def test_linear_batchorder2(self,linear_contract_code):
        r = t.linear_batchorder({"orders_data": [{
                                        "contract_code": linear_contract_code,
                                        "client_order_id": random.randint(1, 999999),
                                        "price": self.buy_price-1,
                                        "volume": '1',
                                        "direction": 'buy',
                                        "offset": 'open',
                                        "lever_rate": self.lever_rate,
                                        "order_price_type": 'limit'}]})
        pprint(r)
        schema = {
                    'data': {
                        'errors': [

                        ],
                        'success': [
                            {
                                'index': int,
                                'order_id': int,
                                'order_id_str': str,
                                'client_order_id': int
                            }
                        ]
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)



    @allure.title('获取市场最优挂单')
    def test_linear_bbo(self,linear_contract_code):
        r = t.linear_bbo(contract_code=linear_contract_code)
        pprint(r)
        schema = {
                    'ticks': [{'contract_code': linear_contract_code,
                               'ask': list,
                               'bid': list,
                               'mrid': int,
                               'ts': int}],
                    'status': 'ok',
                    'ts': int}
        Schema(schema).validate(r)



    @allure.title('撤销合约订单')
    def test_linear_cancel(self,linear_contract_code):
        a = t.linear_order(contract_code=linear_contract_code,
                       client_order_id='',
                       price=self.buy_price-1,
                       volume='1',
                       direction='buy',
                       offset='open',
                       lever_rate=self.lever_rate,
                       order_price_type='limit')
        time.sleep(1)
        order_id = a['data']['order_id']

        r = t.linear_cancel(contract_code=linear_contract_code,
                            order_id=order_id)
        pprint(r)
        schema = {
                    'data': {
                        'errors': [

                        ],
                        'successes': str
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('撤销全部合约单')
    def test_linear_cancelall(self,linear_contract_code):
        t.linear_order(contract_code=linear_contract_code,
                       client_order_id='',
                       price=self.buy_price-1,
                       volume='1',
                       direction='buy',
                       offset='open',
                       lever_rate=self.lever_rate,
                       order_price_type='limit')
        time.sleep(1)

        r = t.linear_cancelall(contract_code=linear_contract_code)
        pprint(r)
        schema = {
                    'data': {
                        'errors': [

                        ],
                        'successes': str
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('获取合约信息')
    def test_linear_contract_info1(self,linear_contract_code,symbol):
        r = t.linear_contract_info(contract_code=linear_contract_code)
        pprint(r)
        schema = {
                    'data': [
                        {
                            'contract_code': linear_contract_code,
                            'contract_size': Or(float,int),
                            'contract_status': int,
                            'create_date': str,
                            'delivery_time': str,
                            'price_tick': Or(float,int),
                            'settlement_date': str,
                            'support_margin_mode': Or('cross','isolated','all'),
                            'symbol': symbol
                        }
                    ],
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)


    @allure.title('获取合约用户账户信息（全仓）')
    def test_linear_cross_account_info(self,symbol):
        r = t.linear_cross_account_info(margin_account='USDT')
        pprint(r)
        schema1 = {'data': [{'contract_detail': [{'adjust_factor': float,
                                                'contract_code': str,
                                                'lever_rate': int,
                                                'liquidation_price': Or(None,float),
                                                'margin_available': float,
                                                'margin_frozen': Or(int,float,None),
                                                'margin_position': Or(float,int),
                                                'profit_unreal': Or(float,int),
                                                'symbol': str},],
                           'margin_account': 'USDT',
                           'margin_asset': 'USDT',
                           'margin_balance': float,
                           'margin_frozen': Or(int,float,None),
                           'margin_mode': 'cross',
                           'margin_position': float,
                           'margin_static': float,
                           'profit_real': float,
                           'profit_unreal': Or(int,float),
                           'risk_rate': float,
                           'withdraw_available': float}],
                 'status': 'ok',
                 'ts': int}

        schema2 = {'adjust_factor': float,
                    'contract_code': str,
                    'lever_rate': int,
                    'liquidation_price': Or(None,float),
                    'margin_available': float,
                    'margin_frozen': Or(int,float,None),
                    'margin_position': Or(float,int),
                    'profit_unreal': Or(float,int),
                    'symbol': str}


        Schema(schema1).validate(r)
        Schema(schema2).validate(r['data'][0]['contract_detail'][0])

    @allure.title('获取用户资产和持仓信息（全仓）')
    def test_linear_cross_account_position_info(self,linear_contract_code):

        r = t.linear_cross_account_position_info(margin_account='USDT')
        pprint(r)
        schema1 = {'data': {'contract_detail': [{'adjust_factor': float,
                                               'contract_code': str,
                                               'lever_rate': int,
                                               'liquidation_price': Or(None,float),
                                               'margin_available': float,
                                               'margin_frozen': Or(int,float),
                                               'margin_position': Or(int,float),
                                               'profit_unreal': Or(int,float),
                                               'symbol': str},],
                           'margin_account': 'USDT',
                           'margin_asset': 'USDT',
                           'margin_balance': Or(float,int),
                           'margin_frozen': Or(float,int),
                           'margin_mode': 'cross',
                           'margin_position': Or(float,int),
                           'margin_static': Or(float,int),
                           'positions': [{'available': Or(float,int),
                                          'contract_code': str,
                                          'cost_hold': Or(float,int),
                                          'cost_open': Or(float,int),
                                          'direction': str,
                                          'frozen': float,
                                          'last_price': Or(float,int),
                                          'lever_rate': int,
                                          'margin_account': 'USDT',
                                          'margin_asset': 'USDT',
                                          'margin_mode': 'cross',
                                          'position_margin': Or(float,int),
                                          'profit': Or(float,int),
                                          'profit_rate': Or(float,int),
                                          'profit_unreal': Or(float,int),
                                          'symbol': str,
                                          'volume': float},],
                          'profit_real': float,
                          'profit_unreal': float,
                          'risk_rate': float,
                          'withdraw_available': float},
                 'status': 'ok',
                 'ts': int}
        schema2 = {'adjust_factor': float,
                   'contract_code': str,
                   'lever_rate': int,
                   'liquidation_price': Or(None,float),
                   'margin_available': float,
                   'margin_frozen': Or(int,float),
                   'margin_position': Or(int,float),
                   'profit_unreal': Or(int,float),
                   'symbol': str}

        schema3 = {'available': Or(float,int),
                  'contract_code': str,
                  'cost_hold': Or(float,int),
                  'cost_open': Or(float,int),
                  'direction': str,
                  'frozen': float,
                  'last_price': Or(float,int),
                  'lever_rate': int,
                  'margin_account': 'USDT',
                  'margin_asset': 'USDT',
                  'margin_mode': 'cross',
                  'position_margin': Or(float,int),
                  'profit': Or(float,int),
                  'profit_rate': Or(float,int),
                  'profit_unreal': Or(float,int),
                  'symbol': str,
                  'volume': float}


        Schema(schema1).validate(r)
        Schema(schema2).validate(r['data']['contract_detail'][0])
        Schema(schema3).validate(r['data']['positions'][0])

    @allure.title('查询平台阶梯调整系数--全仓')
    def test_linear_cross_adjustfactor(self):
        r = t.linear_cross_adjustfactor()
        pprint(r)
        schema = {
                    'data': [
                        {
                            'contract_code': str,
                            'list': [
                                {
                                    'ladders': [
                                        {
                                            'adjust_factor': Or(float,int,None),
                                            'ladder': Or(float,int,None),
                                            'max_size': Or(float,int,None),
                                            'min_size': Or(float,int,None),
                                        }
                                    ],
                                    'lever_rate': int
                                },

                            ],
                            'margin_mode': str,
                            'symbol': str
                        },

                    ],
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('查询用户品种实际可用杠杆倍数（全仓）')
    def test_linear_cross_available_level_rate(self,linear_contract_code,symbol):
        r = t.linear_cross_available_level_rate(contract_code=linear_contract_code)
        pprint(r)
        schema = {'data': [{'available_level_rate': str,
                           'contract_code': linear_contract_code,
                           'margin_mode': 'cross'}],
                 'status': 'ok',
                 'ts': int}

        Schema(schema).validate(r)

    @allure.title('合约批量下单(全仓)')
    def test_linear_cross_batchorder1(self,linear_contract_code):
        r = t.linear_cross_batchorder({"orders_data": [{
                                        "contract_code": linear_contract_code,
                                        "client_order_id": '',
                                        "price": self.buy_price-1,
                                        "volume": '1',
                                        "direction": 'buy',
                                        "offset": 'open',
                                        "lever_rate": self.lever_rate,
                                        "order_price_type": 'limit'}]})
        pprint(r)
        schema = {
                    'data': {
                        'errors': [

                        ],
                        'success': [
                            {
                                'index': int,
                                'order_id': int,
                                'order_id_str': str
                            }
                        ]
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)




    @allure.title('合约批量下单(全仓)(client_order_id)')
    def test_linear_cross_batchorder2(self,linear_contract_code):
        r = t.linear_batchorder({"orders_data": [{
                                        "contract_code": linear_contract_code,
                                        "client_order_id": random.randint(1, 999999),
                                        "price": self.buy_price-1,
                                        "volume": '1',
                                        "direction": 'buy',
                                        "offset": 'open',
                                        "lever_rate": self.lever_rate,
                                        "order_price_type": 'limit'}]})
        pprint(r)
        schema = {
                    'data': {
                        'errors': [

                        ],
                        'success': [
                            {
                                'index': int,
                                'order_id': int,
                                'order_id_str': str,
                                'client_order_id': int
                            }
                        ]
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('撤销合约订单(全仓)')
    def test_linear_cross_cancel(self,linear_contract_code):
        a = t.linear_cross_order(contract_code=linear_contract_code,
                       client_order_id='',
                       price=self.buy_price-1,
                       volume='1',
                       direction='buy',
                       offset='open',
                       lever_rate=self.lever_rate,
                       order_price_type='limit')
        time.sleep(1)
        order_id = a['data']['order_id']

        r = t.linear_cross_cancel(contract_code=linear_contract_code,
                            order_id=order_id)
        pprint(r)
        schema = {
                    'data': {
                        'errors': [

                        ],
                        'successes': str
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('撤销全部合约单(全仓)')
    def test_linear_cross_cancelall(self,linear_contract_code):
        t.linear_cross_order(contract_code=linear_contract_code,
                       client_order_id='',
                       price=self.buy_price-1,
                       volume='1',
                       direction='buy',
                       offset='open',
                       lever_rate=self.lever_rate,
                       order_price_type='limit')
        time.sleep(1)

        r = t.linear_cross_cancelall(contract_code=linear_contract_code)
        pprint(r)
        schema = {
                    'data': {
                        'errors': [

                        ],
                        'successes': str
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('获取用户的合约历史委托(全仓)')
    def test_linear_cross_hisorders(self,linear_contract_code,symbol):
        r = t.linear_cross_hisorders(contract_code=linear_contract_code,
                               trade_type='0',
                               type='1',
                               status='0',
                               create_date='7',
                               page_index='',
                               page_size='')
        pprint(r)
        schema = {
                    'data': {
                        'current_page': int,
                        'orders': [
                            {
                                'contract_code': linear_contract_code,
                                'create_date': int,
                                'direction': str,
                                'fee': float,
                                'fee_asset': 'USDT',
                                'is_tpsl': Or(0,1),
                                'lever_rate': int,
                                'liquidation_type': str,
                                'margin_account': str,
                                'margin_asset': 'USDT',
                                'margin_frozen': Or(float,None),
                                'margin_mode': 'cross',
                                'offset': str,
                                'order_id': int,
                                'order_id_str': str,
                                'order_price_type': int,
                                'order_source': str,
                                'order_type': int,
                                'price': float,
                                'profit': float,
                                'real_profit':Or(float,int),
                                'status': int,
                                'symbol': symbol,
                                'trade_avg_price': Or(float,int),
                                'trade_turnover': float,
                                'trade_volume': float,
                                'update_time': int,
                                'volume': float
                            }
                        ],
                        'total_page': int,
                        'total_size': int
                    },
                    'status': 'ok',
                    'ts': int
                }
        Schema(schema).validate(r)

    @allure.title('组合查询合约历史委托（全仓）')
    def test_linear_cross_hisorders_exact(self,linear_contract_code,symbol):
        r = t.linear_cross_hisorders_exact(contract_code=linear_contract_code,
                                       trade_type='0',
                                       type='1',
                                       status='0',
                                       order_price_type='limit',
                                       start_time='',
                                       end_time='',
                                       from_id='',
                                        size='',
                                     direct='')
        pprint(r)
        schema = {'data': {'next_id': Or(int,None),
                              'orders': [{'contract_code': linear_contract_code,
                                          'create_date': int,
                                          'direction': str,
                                          'fee': float,
                                          'fee_asset': 'USDT',
                                          'is_tpsl': int,
                                          'lever_rate': int,
                                          'liquidation_type': str,
                                          'margin_account': 'USDT',
                                          'margin_frozen': float,
                                          'margin_mode': 'cross',
                                          'offset': str,
                                          'order_id': int,
                                          'order_id_str': str,
                                          'order_price_type': str,
                                          'order_source': str,
                                          'order_type': int,
                                          'price': float,
                                          'profit': float,
                                          'query_id': int,
                                          'real_profit': Or(int,float),
                                          'status': int,
                                          'symbol': symbol,
                                          'trade_avg_price': Or(int,float),
                                          'trade_turnover': float,
                                          'trade_volume':float,
                                          'volume': float},],
                              'remain_size': int},
                     'status': 'ok',
                     'ts': int}
        Schema(schema).validate(r)

    @allure.title('获取平台阶梯保证金（全仓）')
    def test_linear_cross_ladder_margin(self,linear_contract_code,symbol):
        r = t.linear_cross_ladder_margin(contract_code=linear_contract_code)
        pprint(r)
        schema = {'data': [{'contract_code': linear_contract_code,
                           'list': [{'ladders': [{'max_margin_available': Or(int,float,None),
                                                  'max_margin_balance': Or(int,float,None),
                                                  'min_margin_available': Or(int,float,None),
                                                  'min_margin_balance': Or(int,float)},None],
                                     'lever_rate': int},],
                                   'margin_account': 'USDT',
                                   'margin_mode': 'cross',
                                   'symbol': symbol}],
                         'status': 'ok',
                         'ts': int}
        Schema(schema).validate(r)

    @allure.title('合约闪电平仓下单(全仓)')
    def test_linear_cross_lightning_close_position(self,linear_contract_code):
        a = t.linear_cross_order(contract_code=linear_contract_code,
                       client_order_id='',
                       price='',
                       volume='1',
                       direction='buy',
                       offset='open',
                       lever_rate='5',
                       order_price_type='opponent')
        time.sleep(1)

        r = t.linear_cross_lightning_close_position(contract_code=linear_contract_code,
                                              volume='1',
                                              direction='sell',
                                              client_order_id='',
                                              order_price_type='lightning')
        pprint(r)
        schema = {
                    'data': {
                        'order_id': int,
                        'order_id_str': str
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('获取用户的合约历史成交记录(全仓)')
    def test_linear_cross_matchresults(self,linear_contract_code,symbol):
        r = t.linear_cross_matchresults(contract_code=linear_contract_code,
                                  trade_type='0',
                                  create_date='7',
                                  page_index='',
                                  page_size='')
        pprint(r)
        schema = {
                    'data': {
                        'current_page': int,
                        'total_page': int,
                        'total_size': int,
                        'trades': [
                            {
                                'contract_code': linear_contract_code,
                                'create_date': int,
                                'direction': str,
                                'fee_asset': 'USDT',
                                'id': str,
                                'margin_account': str,
                                'margin_mode': 'cross',
                                'match_id': int,
                                'offset': str,
                                'offset_profitloss': float,
                                'order_id': int,
                                'order_id_str': str,
                                'order_source': str,
                                'real_profit': float,
                                'role': str,
                                'symbol': symbol,
                                'trade_fee': float,
                                'trade_price': float,
                                'trade_turnover': float,
                                'trade_volume': float
                            }
                        ]
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('组合查询用户历史成交记录（全仓）')
    def test_linear_cross_matchresults_exact(self,linear_contract_code,symbol):
        r = t.linear_cross_matchresults_exact(contract_code=linear_contract_code,
                                        trade_type='0',
                                        start_time='',
                                        end_time='',
                                        from_id='',
                                        size='',
                                        direct='')
        pprint(r)
        schema = {
                    'data': {
                        'next_id': Or(int,None),
                        'remain_size': int,
                        'trades': [
                            {
                                'contract_code': linear_contract_code,
                                'create_date': int,
                                'direction': str,
                                'fee_asset': 'USDT',
                                'id': str,
                                'margin_account': str,
                                'margin_mode': 'cross',
                                'match_id': int,
                                'offset': str,
                                'offset_profitloss': float,
                                'order_id': int,
                                'order_id_str': str,
                                'order_source': str,
                                'real_profit': float,
                                'role': str,
                                'symbol': symbol,
                                'trade_fee': float,
                                'trade_price': float,
                                'trade_turnover': float,
                                'trade_volume': float,
                                'query_id': int
                            }
                        ]
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('获取用户的合约当前未成交委托(全仓)')
    def test_linear_cross_openorders(self,linear_contract_code,symbol):
        t.linear_cross_order(contract_code=linear_contract_code,
                       client_order_id='',
                       price=self.buy_price-1,
                       volume='1',
                       direction='buy',
                       offset='open',
                       lever_rate=self.lever_rate,
                       order_price_type='limit')
        time.sleep(1)
        r = t.linear_cross_openorders(contract_code=linear_contract_code,
                                page_index='',
                                page_size='')
        pprint(r)
        schema = {
                    'data': {
                        'current_page': int,
                        'orders': [
                            {
                                'canceled_at': Or(int,str,None),
                                'client_order_id':  Or(int,str,None),
                                'contract_code': linear_contract_code,
                                'created_at': int,
                                'direction': str,
                                'fee': Or(int,float),
                                'fee_asset': 'USDT',
                                'is_tpsl': Or(0,1),
                                'lever_rate': int,
                                'liquidation_type': Or(str,None),
                                'margin_account': str,
                                'margin_asset': 'USDT',
                                'margin_frozen': Or(int,float,None),
                                'margin_mode': 'cross',
                                'offset': str,
                                'order_id': int,
                                'order_id_str': str,
                                'order_price_type': str,
                                'order_source': str,
                                'order_type': int,
                                'price': Or(int,float),
                                'profit': Or(int,float),
                                'real_profit':  Or(int,float),
                                'status': int,
                                'symbol': symbol,
                                'trade_avg_price': Or(int,float,None),
                                'trade_turnover': Or(int,float,None),
                                'trade_volume': int,
                                'update_time': int,
                                'volume': int
                            }
                        ],
                        'total_page': int,
                        'total_size': int
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)


    @allure.title('合约下单(全仓)')
    def test_linear_cross_order1(self,linear_contract_code):
        r = t.linear_cross_order(contract_code=linear_contract_code,
                           client_order_id='',
                           price=self.buy_price-1,
                           volume='1',
                           direction='buy',
                           offset='open',
                           lever_rate=self.lever_rate,
                           order_price_type='limit')
        pprint(r)
        schema = {
                    'data': {
                        'order_id': int,
                        'order_id_str': str
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('合约下单(全仓)(client_order_id)')
    def test_linear_cross_order2(self,linear_contract_code):
        r = t.linear_cross_order(contract_code=linear_contract_code,
                           client_order_id=random.randint(1, 999999),
                           price=self.buy_price-1,
                           volume='1',
                           direction='buy',
                           offset='open',
                           lever_rate=self.lever_rate,
                           order_price_type='limit')
        pprint(r)
        schema = {
                    'data': {
                        'order_id': int,
                        'order_id_str': str,
                        'client_order_id': int
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('获取用户的合约订单明细信息(全仓)')
    def test_linear_cross_order_detail(self,linear_contract_code,symbol):
        a = t.linear_cross_order(contract_code=linear_contract_code,
                       client_order_id='',
                       price=self.sell_price,
                       volume='1',
                       direction='buy',
                       offset='open',
                       lever_rate=self.lever_rate,
                       order_price_type='limit')
        time.sleep(3)
        order_id = a['data']['order_id']
        created_at = a['ts']
        r = t.linear_cross_order_detail(contract_code=linear_contract_code,
                                  order_id=order_id,
                                  created_at=created_at,
                                  order_type='1',
                                  page_index='1',
                                  page_size='20')
        pprint(r)
        schema1 = {
                    'data': {
                        'adjust_value': Or(int,float),
                        'canceled_at': int,
                        'client_order_id': Or(str,None),
                        'contract_code': linear_contract_code,
                        'created_at': int,
                        'current_page': int,
                        'direction': str,
                        'fee': Or(int,float),
                        'fee_asset': 'USDT',
                        'final_interest': int,
                        'instrument_price': Or(int,float),
                        'is_tpsl': Or(0,1),
                        'lever_rate': int,
                        'liquidation_type': str,
                        'margin_account': str,
                        'margin_asset': 'USDT',
                        'margin_frozen': Or(float,int),
                        'margin_mode': 'cross',
                        'offset': str,
                        'order_id': int,
                        'order_id_str': str,
                        'order_price_type': str,
                        'order_source': str,
                        'order_type': str,
                        'price': Or(int,float),
                        'profit': float,
                        'real_profit': Or(int,float),
                        'status': int,
                        'symbol': symbol,
                        'total_page': int,
                        'total_size': int,
                        'trade_avg_price': Or(int,float,None),
                        'trade_turnover': float,
                        'trade_volume': float,
                        'trades': [
                            {'created_at': int,
                             'fee_asset': 'USDT',
                             'id': str,
                             'profit': float,
                             'real_profit': float,
                             'role': str,
                             'trade_fee': float,
                             'trade_id': int,
                             'trade_price': float,
                             'trade_turnover': float,
                             'trade_volume': float}
                        ],
                        'volume': float
                    },
                    'status': 'ok',
                    'ts': int
                }

        schema2 = {'created_at': int,
                 'fee_asset': 'USDT',
                 'id': str,
                 'profit': float,
                 'real_profit': float,
                 'role': str,
                 'trade_fee': float,
                 'trade_id': int,
                 'trade_price': float,
                 'trade_turnover': float,
                 'trade_volume': float}

        Schema(schema1).validate(r)
        Schema(schema2).validate(r['data']['trades'][0])

    @allure.title('获取用户资产和持仓信息（全仓）')
    def test_linear_cross_position_info(self,linear_contract_code,symbol):
        r = t.linear_cross_position_info(contract_code=linear_contract_code)
        pprint(r)
        schema = {
            'data': [
                {
                    'symbol': symbol,
                    'contract_code': linear_contract_code,
                    'volume': float,
                    'available': float,
                    'frozen': Or(float,None),
                    'cost_open': float,
                    'cost_hold': float,
                    'profit_unreal': float,
                    'profit_rate': float,
                    'profit': float,
                    'margin_asset': 'USDT',
                    'position_margin': float,
                    'lever_rate': int,
                    'margin_account': str,
                    'margin_mode': 'cross',
                    'direction': str,
                    'last_price': Or(float,int)
                }
            ],
            'status': 'ok',
            'ts': int
        }

        Schema(schema).validate(r)

    @allure.title('获取用户的合约持仓量限制（全仓）')
    def test_linear_cross_position_limit(self,linear_contract_code,symbol):
        r = t.linear_cross_position_limit(contract_code=linear_contract_code)
        pprint(r)
        schema = {
                    'data': [
                        {
                            'buy_limit': Or(float,None),
                            'contract_code': linear_contract_code,
                            'margin_mode': 'cross',
                            'sell_limit': Or(float,None),
                            'symbol': symbol
                        }
                    ],
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('查询开仓单关联的止盈止损订单详情（全仓）')
    def test_linear_cross_relation_tpsl_order(self,linear_contract_code):
        a = t.linear_cross_order(contract_code=linear_contract_code,
                           client_order_id='',
                           price=self.sell_price,
                           volume='1',
                           direction='buy',
                           offset='open',
                           lever_rate=self.lever_rate,
                           order_price_type='limit',
                           tp_trigger_price=self.sell_price+100,
                           tp_order_price=self.sell_price+100,
                           tp_order_price_type='limit',
                           sl_order_price=self.sell_price-100,
                           sl_order_price_type='limit',
                           sl_trigger_price=self.sell_price-100)
        time.sleep(1)
        pprint(a)
        order_id = a['data']['order_id']
        r = t.linear_cross_relation_tpsl_order(contract_code=linear_contract_code,
                                         order_id=order_id)

        pprint(r)
        schema1 = {'data': {'canceled_at': int,
                          'client_order_id': Or(int,str,None),
                          'contract_code': linear_contract_code,
                          'created_at': int,
                          'direction': str,
                          'fee': Or(float,int),
                          'fee_asset': 'USDT',
                          'lever_rate': int,
                          'margin_account': 'USDT',
                          'margin_frozen': float,
                          'margin_mode': 'cross',
                          'offset': str,
                          'order_id': int,
                          'order_id_str': str,
                          'order_price_type': str,
                          'order_source': str,
                          'order_type': int,
                          'price': Or(int,float),
                          'profit': Or(int,float),
                          'status': int,
                          'symbol': str,
                          'tpsl_order_info': [{'canceled_at': int,
                                               'created_at': int,
                                               'direction': str,
                                               'fail_code': Or(None,str),
                                               'fail_reason': Or(None,str),
                                               'order_id': int,
                                               'order_id_str': str,
                                               'order_price': float,
                                               'order_price_type': str,
                                               'relation_order_id': str,
                                               'relation_tpsl_order_id': str,
                                               'status': int,
                                               'tpsl_order_type': str,
                                               'trigger_price': float,
                                               'trigger_type': str,
                                               'triggered_price': Or(int,float,None),
                                               'volume': float},],
                          'trade_avg_price': Or(float,None),
                          'trade_turnover': Or(float,int),
                          'trade_volume': int,
                          'volume': int},
                 'status': 'ok',
                 'ts': int}

        schema2 = {'canceled_at': int,
                   'created_at': int,
                   'direction': str,
                   'fail_code': Or(None,str),
                   'fail_reason': Or(None,str),
                   'order_id': int,
                   'order_id_str': str,
                   'order_price': float,
                   'order_price_type': str,
                   'relation_order_id': str,
                   'relation_tpsl_order_id': str,
                   'status': int,
                   'tpsl_order_type': str,
                   'trigger_price': float,
                   'trigger_type': str,
                   'triggered_price': Or(int,float,None),
                   'volume': float}


        Schema(schema1).validate(r)
        Schema(schema2).validate(r['data']['tpsl_order_info'][0])

    @allure.title('查询母账户下的单个子账户资产信息')
    def test_linear_cross_sub_account_info(self,sub_uid):
        r = t.linear_cross_sub_account_info(margin_account='USDT',sub_uid=sub_uid)
        pprint(r)
        schema = {'data': [{'contract_detail': [{'adjust_factor': float,
                                                'contract_code': str,
                                                'lever_rate': int,
                                                'liquidation_price': Or(float,int,str,None),
                                                'margin_available': Or(int,float),
                                                'margin_frozen': Or(int,float),
                                                'margin_position': Or(int,float),
                                                'profit_unreal': Or(int,float),
                                                'symbol': str},],
                           'margin_account': 'USDT',
                           'margin_asset': 'USDT',
                           'margin_balance': Or(int,float),
                           'margin_frozen': Or(int,float),
                           'margin_mode': 'cross',
                           'margin_position': Or(int,float),
                           'margin_static': Or(int,float),
                           'profit_real': Or(int,float),
                           'profit_unreal': Or(int,float),
                           'risk_rate': Or(int,None,float),
                           'withdraw_available': Or(int,None,float)}],
                 'status': 'ok',
                 'ts': int}
        Schema(schema).validate(r)

    @allure.title('批量获取子账户资产信息（全仓）')
    def test_linear_cross_sub_account_info_list(self,symbol):
        r = t.linear_cross_sub_account_info_list(margin_account='USDT',page_index='',page_size='')
        pprint(r)
        schema = {'data': {'current_page': int,
          'sub_list': [{'account_info_list': [{'margin_account': 'USDT',
                                               'margin_asset': 'USDT',
                                               'margin_balance': Or(float,int),
                                               'margin_mode': 'cross',
                                               'risk_rate': Or(float,None)}],
                                                'sub_uid': int}],
                                  'total_page': int,
                                  'total_size': int},
                         'status': 'ok',
                         'ts': int}

        Schema(schema).validate(r)

    @allure.title('查询母账户下所有子账户资产信息（全仓）')
    def test_linear_cross_sub_account_list(self):
        r = t.linear_cross_sub_account_list(margin_account='USDT')
        pprint(r)
        schema = {
                    'data': [
                        {
                            'list': [
                                {
                                    'margin_account': str,
                                    'margin_asset': 'USDT',
                                    'margin_balance': Or(int,float,None),
                                    'margin_mode': 'cross',
                                    'risk_rate': Or(int,float,None)
                                }
                            ],
                            'sub_uid': int
                        }
                    ],
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('查询母账户下的单个子账户持仓信息（全仓）')
    def test_linear_cross_sub_position_info(self,linear_contract_code,sub_uid,symbol):
        r = t.linear_cross_sub_position_info(contract_code=linear_contract_code,sub_uid=sub_uid)
        pprint(r)
        schema = {
                    'data': [
                        {
                            'available': float,
                            'contract_code': linear_contract_code,
                            "margin_mode": "cross",
                            "margin_account": "USDT",
                            'cost_hold': float,
                            'cost_open': float,
                            'direction': str,
                            'frozen': float,
                            'last_price': Or(float,int),
                            'lever_rate': int,
                            'margin_asset': 'USDT',
                            'position_margin': float,
                            'profit': float,
                            'profit_rate': float,
                            'profit_unreal': float,
                            'symbol': symbol,
                            'volume': float
                        }
                    ],
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('切换杠杆倍数（全仓）')
    def test_linear_cross_switch_lever_rate(self,linear_contract_code,symbol):
        r = t.linear_cross_switch_lever_rate(contract_code=linear_contract_code,lever_rate=self.lever_rate)
        pprint(r)
        schema = {'data': {'contract_code': linear_contract_code,
                          'lever_rate': int,
                          'margin_mode': 'cross'},
                 'status': 'ok',
                 'ts': int}

        Schema(schema).validate(r)



    @allure.title('止盈止损订单撤单（全仓）')
    def test_linear_cross_tpsl_cancel(self,linear_contract_code):
        t.linear_cross_order(contract_code=linear_contract_code,
                           client_order_id='',
                           price=self.sell_price,
                           volume='1',
                           direction='buy',
                           offset='open',
                           lever_rate=self.lever_rate,
                           order_price_type='limit')

        a = t.linear_cross_tpsl_order(contract_code=linear_contract_code,
                                direction='sell',
                                volume='1',
                                tp_trigger_price=self.sell_price+100,
                                tp_order_price=self.sell_price+100,
                                tp_order_price_type='limit',
                                sl_order_price=self.sell_price-100,
                                sl_order_price_type='limit',
                                sl_trigger_price=self.sell_price-100)
        time.sleep(1)
        order_id = a['data']['tp_order']['order_id']
        r = t.linear_cross_tpsl_cancel(contract_code=linear_contract_code,
                                 order_id=order_id)
        pprint(r)
        schema = {'data': {'errors': list,
                           'successes': str},
                             'status': 'ok',
                             'ts': int}

        Schema(schema).validate(r)

    @allure.title('止盈止损订单全部撤单（全仓）')
    def test_linear_cross_tpsl_cancelall(self,linear_contract_code):
        t.linear_cross_order(contract_code=linear_contract_code,
                           client_order_id='',
                           price=self.sell_price-1,
                           volume='1',
                           direction='buy',
                           offset='open',
                           lever_rate=self.lever_rate,
                           order_price_type='limit')

        t.linear_cross_tpsl_order(contract_code=linear_contract_code,
                                direction='sell',
                                volume='1',
                                tp_trigger_price=self.sell_price+100,
                                tp_order_price=self.sell_price+100,
                                tp_order_price_type='limit',
                                sl_order_price=self.sell_price-100,
                                sl_order_price_type='limit',
                                sl_trigger_price=self.sell_price-100)
        time.sleep(2)

        r = t.linear_cross_tpsl_cancelall(contract_code=linear_contract_code)
        pprint(r)
        schema = {'data': {'errors': list,
                           'successes': str},
                             'status': 'ok',
                             'ts': int}

        Schema(schema).validate(r)

    @allure.title('查询止盈止损订单历史委托（全仓）')
    def test_linear_cross_tpsl_hisorders(self,linear_contract_code,symbol):
        r = t.linear_cross_tpsl_hisorders(contract_code=linear_contract_code,
                                    status='0',
                                    create_date='7',
                                    page_size='',
                                    page_index='',
                                    sort_by='')
        pprint(r)
        schema = {'data': {'current_page': int,
                          'orders': [{'canceled_at': int,
                                      'contract_code': linear_contract_code,
                                      'created_at': int,
                                      'direction': str,
                                      'fail_code': Or(str,None),
                                      'fail_reason': Or(str,None),
                                      'margin_account': 'USDT',
                                      'margin_mode': 'cross',
                                      'order_id': int,
                                      'order_id_str': str,
                                      'order_price': float,
                                      'order_price_type': str,
                                      'order_source': str,
                                      'order_type': int,
                                      'relation_order_id': str,
                                      'relation_tpsl_order_id': str,
                                      'source_order_id': Or(int,None,str),
                                      'status': int,
                                      'symbol': str,
                                      'tpsl_order_type': str,
                                      'trigger_price': float,
                                      'trigger_type': str,
                                      'triggered_price': Or(str,None),
                                      'update_time': int,
                                      'volume': float},],
                          'total_page': int,
                          'total_size': int},
                 'status': 'ok',
                 'ts': int}

        Schema(schema).validate(r)

    @allure.title('查询止盈止损订单当前委托（全仓）')
    def test_linear_cross_tpsl_openorders(self,linear_contract_code,symbol):
        t.linear_cross_order(contract_code=linear_contract_code,
                           client_order_id='',
                           price=self.sell_price,
                           volume='1',
                           direction='buy',
                           offset='open',
                           lever_rate=self.lever_rate,
                           order_price_type='limit')
        t.linear_cross_tpsl_order(contract_code=linear_contract_code,
                                direction='sell',
                                volume='1',
                                tp_trigger_price=self.sell_price+100,
                                tp_order_price=self.sell_price+100,
                                tp_order_price_type='limit',
                                sl_order_price=self.sell_price-100,
                                sl_order_price_type='limit',
                                sl_trigger_price=self.sell_price-100)
        time.sleep(1)
        r = t.linear_cross_tpsl_openorders(contract_code=linear_contract_code,
                                     page_index='',
                                     page_size='')
        pprint(r)
        schema = {'data': {'current_page': int,
                          'orders': [{'contract_code': linear_contract_code,
                                      'created_at': int,
                                      'direction': str,
                                      'margin_account': 'USDT',
                                      'margin_mode': 'cross',
                                      'order_id': int,
                                      'order_id_str': str,
                                      'order_price': float,
                                      'order_price_type': str,
                                      'order_source': str,
                                      'order_type': int,
                                      'relation_tpsl_order_id': str,
                                      'source_order_id': Or(str,None),
                                      'status': int,
                                      'symbol': symbol,
                                      'tpsl_order_type': str,
                                      'trigger_price': float,
                                      'trigger_type': str,
                                      'volume': float},],
                          'total_page': int,
                          'total_size': int},
                 'status': 'ok',
                 'ts': int}

        Schema(schema).validate(r)

    @allure.title('对仓位设置止盈止损订单（全仓）')
    def test_linear_cross_tpsl_order(self,linear_contract_code):
        t.linear_cross_order(contract_code=linear_contract_code,
                           client_order_id='',
                           price=self.sell_price,
                           volume='1',
                           direction='buy',
                           offset='open',
                           lever_rate=self.lever_rate,
                           order_price_type='limit')

        r = t.linear_cross_tpsl_order(contract_code=linear_contract_code,
                                direction='sell',
                                volume='1',
                                tp_trigger_price=self.sell_price+100,
                                tp_order_price=self.sell_price+100,
                                tp_order_price_type='limit',
                                sl_order_price=self.sell_price-100,
                                sl_order_price_type='limit',
                                sl_trigger_price=self.sell_price-100)
        pprint(r)
        schema = {'data': {'sl_order': {'order_id': int,
                            'order_id_str': str},
                          'tp_order': {'order_id': int,
                                       'order_id_str': str}},
                         'status': 'ok',
                         'ts': int}

        Schema(schema).validate(r)

    @allure.title('跟踪委托撤单(全仓)')
    def test_linear_cross_track_cancel(self,linear_contract_code):
        a = t.linear_cross_track_order(contract_code=linear_contract_code,
                                 direction='buy',
                                 offset='open',
                                 lever_rate=self.lever_rate,
                                 volume='1',
                                 callback_rate='0.01',
                                 active_price=self.last_price-100,
                                 order_price_type='formula_price')
        time.sleep(1)
        order_id = a['data']['order_id']
        r = t.linear_cross_track_cancel(contract_code=linear_contract_code,
                                  order_id=order_id)
        pprint(r)
        schema = {'data': {'errors': list,
                           'successes': str},
                         'status': 'ok',
                         'ts': int}

        Schema(schema).validate(r)

    @allure.title('跟踪委托全部撤单(全仓)')
    def test_linear_cross_track_cancelall(self,linear_contract_code):
        a = t.linear_cross_track_order(contract_code=linear_contract_code,
                                 direction='buy',
                                 offset='open',
                                 lever_rate=self.lever_rate,
                                 volume='1',
                                 callback_rate='0.01',
                                 active_price=self.last_price-100,
                                 order_price_type='formula_price')
        time.sleep(1)
        r = t.linear_cross_track_cancelall(contract_code=linear_contract_code)
        pprint(r)
        schema = {'data': {'errors': list,
                           'successes': str},
                         'status': 'ok',
                         'ts': int}

        Schema(schema).validate(r)

    @allure.title('获取跟踪委托历史委托(全仓)')
    def test_linear_cross_track_hisorders(self,linear_contract_code,symbol):
        r = t.linear_cross_track_hisorders(contract_code=linear_contract_code,
                                     status='0',
                                     trade_type='0',
                                     create_date='7',
                                     page_size='',
                                     page_index='',
                                     sort_by='')

        pprint(r)
        schema = {'data': {'current_page': int,
                          'orders': [{'active_price': float,
                                      'callback_rate': float,
                                      'canceled_at': int,
                                      'contract_code': linear_contract_code,
                                      'created_at': int,
                                      'direction': str,
                                      'fail_code': Or(None,str),
                                      'fail_reason': Or(None,str),
                                      'formula_price': Or(None,str,int,float),
                                      'is_active': int,
                                      'lever_rate': int,
                                      'margin_account': 'USDT',
                                      'margin_mode': 'cross',
                                      'market_limit_price': Or(None,int,float,str),
                                      'offset': str,
                                      'order_id': int,
                                      'order_id_str': str,
                                      'order_price_type': str,
                                      'order_source': str,
                                      'order_type': int,
                                      'real_volume': Or(int,float),
                                      'relation_order_id': str,
                                      'status': int,
                                      'symbol': symbol,
                                      'triggered_price': Or(None,int,str,float),
                                      'update_time': int,
                                      'volume': float},],
                          'total_page': int,
                          'total_size': int},
                 'status': 'ok',
                 'ts': int}

        Schema(schema).validate(r)

    @allure.title('获取跟踪委托当前委托(全仓)')
    def test_linear_cross_track_openorders(self,linear_contract_code,symbol):
        t.linear_cross_track_order(contract_code=linear_contract_code,
                                 direction='buy',
                                 offset='open',
                                 lever_rate=self.lever_rate,
                                 volume='1',
                                 callback_rate='0.01',
                                 active_price=self.last_price-100,
                                 order_price_type='formula_price')
        time.sleep(1)
        r = t.linear_cross_track_openorders(contract_code=linear_contract_code,
                                      page_index='',
                                      page_size='')
        pprint(r)
        schema = {'data': {'current_page': int,
                          'orders': [{'active_price': float,
                                      'callback_rate': float,
                                      'contract_code': linear_contract_code,
                                      'created_at': int,
                                      'direction': str,
                                      'is_active': int,
                                      'lever_rate': int,
                                      'margin_account': 'USDT',
                                      'margin_mode': 'cross',
                                      'offset': str,
                                      'order_id': int,
                                      'order_id_str': str,
                                      'order_price_type': str,
                                      'order_source': str,
                                      'order_type': int,
                                      'status': int,
                                      'symbol': symbol,
                                      'volume': float}],
                          'total_page': int,
                          'total_size': int},
                 'status': 'ok',
                 'ts': int}

        Schema(schema).validate(r)

    @allure.title('跟踪委托下单(全仓)')
    def test_linear_cross_track_order(self, linear_contract_code):
        r = t.linear_cross_track_order(contract_code=linear_contract_code,
                                       direction='buy',
                                       offset='open',
                                       lever_rate=self.lever_rate,
                                       volume='1',
                                       callback_rate='0.01',
                                       active_price=self.last_price-100,
                                       order_price_type='formula_price')
        pprint(r)
        schema = {'data': {'order_id': int,
                           'order_id_str': str},
                  'status': 'ok',
                  'ts': int}

        Schema(schema).validate(r)

    @allure.title('查询系统交易权限（全仓）')
    def test_linear_cross_trade_state(self,linear_contract_code,symbol):
        r = t.linear_cross_trade_state(contract_code=linear_contract_code)
        pprint(r)
        schema = {'data': [{'cancel': int,
                           'close': int,
                           'contract_code': linear_contract_code,
                           'margin_account': 'USDT',
                           'margin_mode': 'cross',
                           'open': int,
                           'symbol': symbol}],
                 'status': 'ok',
                 'ts': int}
        Schema(schema).validate(r)

    @allure.title('获取用户的合约划转限制（全仓）')
    def test_linear_cross_transfer_limit(self):
        r = t.linear_cross_transfer_limit(margin_account='USDT')
        pprint(r)
        schema = {
                    'data': [
                        {
                            'margin_account': str,
                            'margin_mode': 'cross',
                            'net_transfer_in_max_daily': float,
                            'net_transfer_out_max_daily': float,
                            'transfer_in_max_daily': float,
                            'transfer_in_max_each': float,
                            'transfer_in_min_each': float,
                            'transfer_out_max_daily': float,
                            'transfer_out_max_each': float,
                            'transfer_out_min_each': float
                        }
                    ],
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('查询系统划转权限--全仓')
    def test_linear_cross_transfer_state(self):
        r = t.linear_cross_transfer_state()
        pprint(r)
        schema = {
                    "status": str,
                    "data": [
                        {
                            "margin_mode": str,
                            "margin_account": str,
                            "transfer_in": Or(None,int),
                            "transfer_out": Or(None,int),
                            "master_transfer_sub": Or(None,int),
                            "sub_transfer_master": Or(None,int),
                            "master_transfer_sub_inner_in": Or(None,int),
                            "master_transfer_sub_inner_out": Or(None,int),
                            "sub_transfer_master_inner_in": Or(None,int),
                            "sub_transfer_master_inner_out": Or(None,int),
                            "transfer_inner_in": Or(None,int),
                            "transfer_inner_out": Or(None,int),

                        }
                    ],
                    "ts": int
                }

        Schema(schema).validate(r)

    @allure.title('合约计划委托撤单(全仓)')
    def test_linear_cross_trigger_cancel(self,linear_contract_code):
        a = t.linear_cross_trigger_order(contract_code=linear_contract_code,
                                   trigger_type='le',
                                   trigger_price=self.last_price-100,
                                   order_price=self.last_price-100,
                                   order_price_type='limit',
                                   volume='1',
                                   direction='buy',
                                   offset='open',
                                   lever_rate=self.lever_rate)
        time.sleep(1)
        order_id = a['data']['order_id']
        r = t.linear_cross_trigger_cancel(contract_code=linear_contract_code,
                                    order_id=order_id)
        pprint(r)
        schema = {
                    'data': {
                        'errors': [

                        ],
                        'successes': str
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('合约计划委托全部撤单(全仓)')
    def test_linear_cross_trigger_cancelall(self,linear_contract_code):
        t.linear_cross_trigger_order(contract_code=linear_contract_code,
                                   trigger_type='le',
                                   trigger_price=self.last_price-100,
                                   order_price=self.last_price-100,
                                   order_price_type='limit',
                                   volume='1',
                                   direction='buy',
                                   offset='open',
                                   lever_rate=self.lever_rate)
        time.sleep(3)

        r = t.linear_cross_trigger_cancelall(contract_code=linear_contract_code)
        pprint(r)
        schema = {
                    'data': {
                        'errors': [

                        ],
                        'successes': str
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('获取计划委托历史委托(全仓)')
    def test_linear_cross_trigger_hisorders(self,linear_contract_code,symbol):
        r = t.linear_cross_trigger_hisorders(contract_code=linear_contract_code,
                                       trade_type='1',
                                       status='0',
                                       create_date='7',
                                       page_index='',
                                       page_size='')
        pprint(r)
        schema = {
                    'data': {
                        'current_page': int,
                        'orders': [
                            {
                                'canceled_at': Or(int,None),
                                'contract_code': linear_contract_code,
                                'created_at': int,
                                'direction': 'buy',
                                'fail_code': Or(int,None),
                                'fail_reason': Or(str,None),
                                'lever_rate': int,
                                'margin_account': str,
                                'margin_mode': 'cross',
                                'offset': str,
                                'order_id': int,
                                'order_id_str': str,
                                'order_insert_at': int,
                                'order_price': float,
                                'order_price_type': str,
                                'order_source': str,
                                'order_type': int,
                                'relation_order_id': str,
                                'status': int,
                                'symbol': symbol,
                                'trigger_price': float,
                                'trigger_type': Or('ge','le'),
                                'triggered_at': Or(int,None),
                                'triggered_price': Or(int,float,None),
                                'update_time': int,
                                'volume': float
                            }
                        ],
                        'total_page': int,
                        'total_size': int
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('获取计划委托当前委托(全仓)')
    def test_linear_cross_trigger_openorders(self,linear_contract_code,symbol):
        a = t.linear_cross_trigger_order(contract_code=linear_contract_code,
                                   trigger_type='le',
                                   trigger_price=self.last_price-100,
                                   order_price=self.last_price-100,
                                   order_price_type='limit',
                                   volume='1',
                                   direction='buy',
                                   offset='open',
                                   lever_rate=self.lever_rate)
        time.sleep(1)
        r = t.linear_cross_trigger_openorders(contract_code=linear_contract_code,
                                       page_index='',
                                       page_size='')
        pprint(r)
        schema = {
                    'data': {
                        'current_page': int,
                        'orders': [
                            {
                                'contract_code': linear_contract_code,
                                'created_at': int,
                                'direction': str,
                                'lever_rate': int,
                                'margin_account': str,
                                'margin_mode': 'cross',
                                'offset': str,
                                'order_id': int,
                                'order_id_str': str,
                                'order_price': float,
                                'order_price_type': str,
                                'order_source': str,
                                'order_type': int,
                                'status': int,
                                'symbol': symbol,
                                'trigger_price': float,
                                'trigger_type': str,
                                'volume': float
                            }
                        ],
                        'total_page': int,
                        'total_size': int
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('合约计划委托下单(全仓)')
    def test_linear_cross_trigger_order(self,linear_contract_code):
        r = t.linear_cross_trigger_order(contract_code=linear_contract_code,
                                   trigger_type='le',
                                   trigger_price=self.last_price-100,
                                   order_price=self.last_price-100,
                                   order_price_type='limit',
                                   volume='1',
                                   direction='buy',
                                   offset='open',
                                   lever_rate=self.lever_rate)
        pprint(r)
        schema = {
                    'data': {
                        'order_id': int,
                        'order_id_str': str
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('查询用户结算记录（全仓）')
    def test_linear_cross_user_settlement_records(self,linear_contract_code,symbol):
        r = t.linear_cross_user_settlement_records(margin_account='USDT',
                                             start_time='',
                                             end_time='',
                                             page_size='',
                                             page_index='')
        pprint(r)
        schema = {'data': {'current_page': int,
                          'settlement_records': [{'clawback': float,
                                                  'contract_detail': [{'contract_code': str,
                                                                       'fee': float,
                                                                       'fee_asset': 'USDT',
                                                                       'offset_profitloss': float,
                                                                       'positions': [{'contract_code': str,
                                                                                      'cost_hold': float,
                                                                                      'cost_hold_pre': float,
                                                                                      'cost_open': float,
                                                                                      'direction': str,
                                                                                      'settlement_price': float,
                                                                                      'settlement_profit_unreal': float,
                                                                                      'settlement_type': 'settlement',
                                                                                      'symbol': str,
                                                                                      'volume': float},],
                                                                       'symbol': str},],
                                                  'fee': float,
                                                  'fee_asset': 'USDT',
                                                  'funding_fee': float,
                                                  'margin_account': 'USDT',
                                                  'margin_balance': Or(float,None),
                                                  'margin_balance_init': Or(float,None),
                                                  'margin_mode': 'cross',
                                                  'offset_profitloss': float,
                                                  'settlement_profit_real': float,
                                                  'settlement_time': int}],
                          'total_page': int,
                          'total_size': int},
                 'status': 'ok',
                 'ts': int}

        Schema(schema).validate(r)

    @allure.title('获取行情深度数据')
    def test_linear_depth(self,linear_contract_code):
        r = t.linear_depth(contract_code=linear_contract_code,type='setp0')
        pprint(r)
        schema = {'ch': 'market.{}.depth.setp0'.format(linear_contract_code),
                     'status': 'ok',
                     'tick': Or(None,dict),
                     'ts': int}
        Schema(schema).validate(r)

    @allure.title('批量获取聚合行情')
    def test_linear_detail_batch_merged(self,linear_contract_code):
        r = t.linear_detail_batch_merged(contract_code=linear_contract_code)
        pprint(r)
        schema = {
                     'status': 'ok',
                     'ticks': [{  'contract_code': linear_contract_code,
                                  'amount': str,
                                  'ask': list,
                                  'bid': list,
                                  'close': str,
                                  'count': int,
                                  'high': str,
                                  'id': int,
                                  'low': str,
                                  'open': str,
                                  'trade_turnover': str,
                                  'ts': int,
                                  'vol': str}],
                     'ts': int}
        Schema(schema).validate(r)

    @allure.title('获取聚合行情')
    def test_linear_detail_merged(self,linear_contract_code):
        r = t.linear_detail_merged(contract_code=linear_contract_code)
        pprint(r)
        schema = {'ch': 'market.{}.detail.merged'.format(linear_contract_code),
                     'status': 'ok',
                     'tick': {'amount': str,
                          'ask': list,
                          'bid': list,
                          'close': str,
                          'count': int,
                          'high': str,
                          'id': int,
                          'low': str,
                          'open': str,
                          'trade_turnover': str,
                          'ts': int,
                          'vol': str},
                     'ts': int}
        Schema(schema).validate(r)

    @allure.title('精英账户多空持仓对比-账户数')
    def test_linear_elite_account_ratio1(self,linear_contract_code,symbol):
        r = t.linear_elite_account_ratio(contract_code=linear_contract_code,
                                         period='60min')
        pprint(r)
        schema = {
                    'data': {
                        'contract_code': linear_contract_code,
                        'list': [
                            {
                                'buy_ratio': float,
                                'locked_ratio': float,
                                'sell_ratio': float,
                                'ts': int
                            }
                        ],
                        'symbol': symbol
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('精英账户多空持仓对比-持仓量')
    def test_linear_elite_position_ratio1(self,linear_contract_code,symbol):
        r = t.linear_elite_position_ratio(contract_code=linear_contract_code,
                                         period='60min')
        pprint(r)
        schema = {
                    'data': {
                        'contract_code': linear_contract_code,
                        'list': [
                            {
                                'buy_ratio': float,
                                'sell_ratio': float,
                                'ts': int
                            }
                        ],
                        'symbol': symbol
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('获取预测资金费率的K线数据')
    def test_linear_estimated_rate_kline(self,linear_contract_code):
        r = t.linear_estimated_rate_kline(contract_code=linear_contract_code,period='1min',size='200')
        pprint(r)
        schema = {'ch': 'market.{}.estimated_rate.{}'.format(linear_contract_code,'1min'),
                  'status': 'ok',
                  'data': [{'amount': str,
                           'close': str,
                           'count': str,
                           'high': str,
                           'id': int,
                           'low': str,
                           'open': str,
                           'vol': str}],
                  'ts': int}
        Schema(schema).validate(r)

    @allure.title('获取预估结算价（全逐通用）')
    def test_linear_estimated_settlement_price(self,linear_contract_code,symbol):
        r = t.linear_estimated_settlement_price(contract_code=linear_contract_code)
        pprint(r)
        schema = {'data': [{'contract_code': linear_contract_code,
                               'estimated_settlement_price': Or(float,int,None),
                               'settlement_type': 'settlement'}],
                     'status': 'ok',
                     'ts': int}

        Schema(schema).validate(r)

    @allure.title('获取用户的合约手续费费率')
    def test_linear_fee(self,linear_contract_code,symbol):
        r = t.linear_fee(contract_code=linear_contract_code)
        pprint(r)
        schema = {
                    'data': [
                        {
                            'close_maker_fee': str,
                            'close_taker_fee': str,
                            'contract_code': linear_contract_code,
                            'fee_asset': 'USDT',
                            'open_maker_fee': str,
                            'open_taker_fee': str,
                            'symbol': symbol
                        }
                    ],
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('查询用户财务记录')
    def test_linear_financial_record(self,linear_contract_code):
        r = t.linear_financial_record(margin_account=linear_contract_code,type='',create_date='7',page_index='',page_size='')
        pprint(r)
        schema = {
            'data': {
                'financial_record': [
                    {
                        'id':int,
                        'ts':int,
                        'asset': 'USDT',
                        'contract_code': linear_contract_code,
                        'margin_account': linear_contract_code,
                        'face_margin_account': Or(str,None),
                        'type':int,
                        'amount':float
                    }
                ],
                'total_page':int,
                'current_page':int,
                'total_size':int
            },
            'status': 'ok',
            'ts': int
        }

        Schema(schema).validate(r)

    @allure.title('组合查询用户财务记录（全逐通用）')
    def test_linear_financial_record_exact(self,linear_contract_code):
        r = t.linear_financial_record_exact(margin_account=linear_contract_code,
                                            contract_code=linear_contract_code,
                                            type='',
                                            start_time='',
                                            end_time='',
                                            from_id='',
                                            size='',
                                            direct='')
        pprint(r)
        schema = {'data': {'financial_record': [{'amount': Or(float,int),
                                                'asset': 'USDT',
                                                'contract_code': linear_contract_code,
                                                'face_margin_account': str,
                                                'id': int,
                                                'margin_account': linear_contract_code,
                                                'ts': int,
                                                'type': int},],
                                              'next_id': int,
                                              'remain_size': int},
                                     'status': 'ok',
                                     'ts': int}

        Schema(schema).validate(r)

    @allure.title('获取合约的资金费率')
    def test_linear_funding_rate1(self,linear_contract_code,symbol):
        r = t.linear_funding_rate(contract_code=linear_contract_code)
        pprint(r)
        schema = {
                    'data': {
                        'contract_code': linear_contract_code,
                        'estimated_rate': str,
                        'fee_asset': 'USDT',
                        'funding_rate': str,
                        'funding_time': str,
                        'next_funding_time': str,
                        'symbol': symbol
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('获取平台持仓量（全逐通用）')
    def test_linear_his_open_interest(self,linear_contract_code,symbol):
        r = t.linear_his_open_interest(contract_code=linear_contract_code,period='60min',size='48',amount_type='1')
        pprint(r)
        schema = {
            'data':
                {
                    'symbol': symbol,
                    'contract_code': linear_contract_code,
                    'tick': [
                        {'volume': float,
                        'amount_type' : int,
                         'value' : float,
                         'ts' : int
                         }
                    ]
                },

            'status': 'ok',
            'ts': int
        }
        Schema(schema).validate(r)


    @allure.title('获取用户的合约历史委托')
    def test_linear_hisorders(self,linear_contract_code,symbol):
        r = t.linear_hisorders(contract_code=linear_contract_code,
                               trade_type='0',
                               type='1',
                               status='0',
                               create_date='7',
                               page_index='',
                               page_size='')
        pprint(r)
        schema = {
                    'data': {
                        'current_page': int,
                        'orders': [Or(
                            {
                                'contract_code': linear_contract_code,
                                'create_date': int,
                                'direction': str,
                                'fee': float,
                                'fee_asset': 'USDT',
                                'is_tpsl': Or(0,1),
                                'lever_rate': int,
                                'liquidation_type': str,
                                'margin_account': str,
                                'margin_asset': 'USDT',
                                'margin_frozen': Or(float,None),
                                'margin_mode': 'isolated',
                                'offset': str,
                                'order_id': int,
                                'order_id_str': str,
                                'order_price_type': int,
                                'order_source': str,
                                'order_type': int,
                                'price': float,
                                'profit': float,
                                'real_profit':Or(float,int),
                                'status': int,
                                'symbol': symbol,
                                'trade_avg_price': Or(float,int),
                                'trade_turnover': float,
                                'trade_volume': float,
                                'update_time': int,
                                'volume': float
                            },None)
                        ],
                        'total_page': int,
                        'total_size': int
                    },
                    'status': 'ok',
                    'ts': int
                }
        Schema(schema).validate(r)

    @allure.title('组合查询合约历史委托（逐仓）')
    def test_linear_hisorders_exact(self,linear_contract_code,symbol):
        r = t.linear_hisorders_exact(contract_code=linear_contract_code,
                                       trade_type='0',
                                       type='1',
                                       status='0',
                                       order_price_type='limit',
                                       start_time='',
                                       end_time='',
                                       from_id='',
                                        size='',
                                     direct='')
        pprint(r)
        schema = {'data': {'next_id': Or(int,None),
                              'orders': [{'contract_code': linear_contract_code,
                                          'create_date': int,
                                          'direction': str,
                                          'fee': float,
                                          'fee_asset': 'USDT',
                                          'is_tpsl': int,
                                          'lever_rate': int,
                                          'liquidation_type': str,
                                          'margin_account': linear_contract_code,
                                          'margin_frozen': float,
                                          'margin_mode': 'isolated',
                                          'offset': str,
                                          'order_id': int,
                                          'order_id_str': str,
                                          'order_price_type': str,
                                          'order_source': str,
                                          'order_type': int,
                                          'price': float,
                                          'profit': float,
                                          'query_id': int,
                                          'real_profit': Or(int,float),
                                          'status': int,
                                          'symbol': symbol,
                                          'trade_avg_price': Or(int,float),
                                          'trade_turnover': float,
                                          'trade_volume':float,
                                          'volume': float},],
                              'remain_size': int},
                     'status': 'ok',
                     'ts': int}
        Schema(schema).validate(r)


    @allure.title('获取合约的历史资金费率')
    def test_linear_historical_funding_rate(self,linear_contract_code,symbol):
        r = t.linear_historical_funding_rate(contract_code=linear_contract_code,
                                             page_index='',
                                             page_size='')
        pprint(r)
        schema = {
                    'data': {
                        'current_page': int,
                        'data': [
                            {
                                'avg_premium_index': str,
                                'contract_code': linear_contract_code,
                                'fee_asset': 'USDT',
                                'funding_rate': str,
                                'funding_time': str,
                                'realized_rate': str,
                                'symbol': symbol
                            }
                        ],
                        'total_page': int,
                        'total_size': int
                    },
                    'status': 'ok',
                    'ts': int
                }


        Schema(schema).validate(r)

    @allure.title('获取指数的K线数据（全逐通用）')
    def test_linear_history_index(self,linear_contract_code):
        r = t.linear_history_index(symbol=linear_contract_code,period='1min',size='10')
        pprint(r)
        schema = {'ch': 'market.{}.index.{}'.format(linear_contract_code,'1min'),
                    'data':[
                        {'amount': Or(float,int),
                         'close': Or(int,float),
                         'count': int,
                         'high': Or(int,float),
                         'id':int,
                         'low': Or(int,float),
                         'open': Or(int,float),
                         'vol':Or(int,float)}],
                     'status': 'ok',
                     'ts': int}
        Schema(schema).validate(r)


    @allure.title('批量获取最近的交易记录')
    def test_linear_history_trade(self,linear_contract_code):
        r = t.linear_history_trade(contract_code=linear_contract_code,size='10')
        pprint(r)
        schema = {'ch': 'market.{}.trade.detail'.format(linear_contract_code),
                  'data':[{'data': [{'amount': Or(float,int),
                                     'direction': str,
                                     'id': int,
                                     'price': Or(int,float),
                                     'quantity':Or(float,int),
                                     'trade_turnover': Or(int,float),
                                     'ts': int}],
                               'id': int,
                               'ts': int}],
                     'status': 'ok',
                     'ts': int}
        Schema(schema).validate(r)

    @allure.title('获取合约指数信息')
    def test_linear_index(self,linear_contract_code):
        r = t.linear_index(contract_code=linear_contract_code)
        pprint(r)
        schema = {
                    'data': [
                        {
                            'contract_code': linear_contract_code,
                            'index_price': float,
                            'index_ts': int
                        }
                    ],
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('获取风险准备金历史数据')
    def test_linear_insurance_fund(self,linear_contract_code,symbol):
        r = t.linear_insurance_fund(contract_code=linear_contract_code,page_size='',page_index='')
        pprint(r)
        schema = {
                    'data': {
                        'contract_code': linear_contract_code,
                        'current_page': int,
                        'symbol': symbol,
                        'tick': [
                            {
                                'insurance_fund': Or(float,0),
                                'ts': int
                            }
                        ],
                        'total_page': int,
                        'total_size': int
                    },
                    'status': 'ok',
                    'ts': int
                }


        Schema(schema).validate(r)

    @allure.title('获取K线数据')
    def test_linear_kline(self,linear_contract_code):
        r = t.linear_kline(contract_code=linear_contract_code,period='1min',size='200',FROM='1',to='2')
        pprint(r)
        schema = {'ch': 'market.{}.kline.{}'.format(linear_contract_code,'1min'),
                  'data': [{'amount': Or(float, int),
                             'close': Or(float, int),
                             'count': Or(float, int),
                             'high': Or(float, int),
                             'id': Or(float, int),
                             'low': Or(float, int),
                             'open': Or(float, int),
                             'trade_turnover': Or(float, int),
                             'vol': Or(float, int)}],
                  'status': 'ok',
                  'ts': int}
        Schema(schema).validate(r)

    @allure.title('获取平台阶梯保证金（逐仓）')
    def test_linear_ladder_margin(self,linear_contract_code,symbol):
        r = t.linear_ladder_margin(contract_code=linear_contract_code)
        pprint(r)
        schema = {'data': [{'contract_code': linear_contract_code,
                           'list': [{'ladders': [{'max_margin_available': Or(int,float,None),
                                                  'max_margin_balance': Or(int,float,None),
                                                  'min_margin_available': Or(int,float,None),
                                                  'min_margin_balance': Or(int,float)},None],
                                     'lever_rate': int},],
                                   'margin_account': linear_contract_code,
                                   'margin_mode': 'isolated',
                                   'symbol': symbol}],
                         'status': 'ok',
                         'ts': int}
        Schema(schema).validate(r)

    @allure.title('合约闪电平仓下单')
    def test_linear_lightning_close_position(self,linear_contract_code):
        a = t.linear_order(contract_code=linear_contract_code,
                       client_order_id='',
                       price=self.sell_price,
                       volume='1',
                       direction='buy',
                       offset='open',
                       lever_rate=self.lever_rate,
                       order_price_type='limit')
        time.sleep(1)

        r = t.linear_lightning_close_position(contract_code=linear_contract_code,
                                              volume='1',
                                              direction='sell',
                                              client_order_id='',
                                              order_price_type='lightning')
        pprint(r)
        schema = {
                    'data': {
                        'order_id': int,
                        'order_id_str': str
                    },
                    'status': 'ok',
                    'ts': int
                }
        Schema(schema).validate(r)

    @allure.title('获取强平订单')
    def test_linear_liquidation_orders(self,linear_contract_code,symbol):
        r = t.linear_liquidation_orders(contract_code=linear_contract_code,
                                        trade_type='0',
                                        create_date='7',
                                        page_index='',
                                        page_size='50')
        pprint(r)
        schema = {
                    'data': {
                        'current_page': int,
                        'orders': [
                            {
                                'contract_code': linear_contract_code,
                                'amount': float,
                                'trade_turnover': float,
                                'created_at': int,
                                'direction': str,
                                'offset': str,
                                'price': float,
                                'symbol': symbol,
                                'volume': Or(float,int,None)
                            }
                        ],
                        'total_page': int,
                        'total_size': int
                    },
                    'status': 'ok',
                    'ts': int
                }
        Schema(schema).validate(r)

    @allure.title('母子账户划转')
    def test_linear_master_sub_transfer(self,sub_uid,linear_contract_code):
        r = t.linear_master_sub_transfer(sub_uid=sub_uid,
                                         asset='usdt',
                                         from_margin_account=linear_contract_code,
                                         to_margin_account='eth-usdt',
                                         amount='1',
                                         type='master_to_sub')
        pprint(r)
        schema = {
                    'data': {
                        'order_id': str
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('获取母账户下的所有母子账户划转记录')
    def test_linear_master_sub_transfer_record(self,linear_contract_code):
        r = t.linear_master_sub_transfer_record(margin_account=linear_contract_code,
                                                transfer_type='34',
                                                create_date='7',
                                                page_index='',
                                                page_size='')
        pprint(r)
        schema = {
                    'data': {
                        'current_page': int,
                        'total_page': int,
                        'total_size': int,
                        'transfer_record': [
                            {
                                'amount': float,
                                'asset': 'USDT',
                                'from_margin_account': str,
                                'id': int,
                                'margin_account': str,
                                'sub_account_name': str,
                                'sub_uid': str,
                                'to_margin_account': str,
                                'transfer_type': int,
                                'ts': int
                            }
                        ]
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('获取用户的合约历史成交记录')
    def test_linear_matchresults(self,linear_contract_code,symbol):
        r = t.linear_matchresults(contract_code=linear_contract_code,
                                  trade_type='0',
                                  create_date='7',
                                  page_index='',
                                  page_size='')
        pprint(r)
        schema = {
                    'data': {
                        'current_page': int,
                        'total_page': int,
                        'total_size': int,
                        'trades': [
                            {
                                'contract_code': linear_contract_code,
                                'create_date': int,
                                'direction': str,
                                'fee_asset': 'USDT',
                                'id': str,
                                'margin_account': str,
                                'margin_mode': 'isolated',
                                'match_id': int,
                                'offset': str,
                                'offset_profitloss': float,
                                'order_id': int,
                                'order_id_str': str,
                                'order_source': str,
                                'real_profit': float,
                                'role': str,
                                'symbol': symbol,
                                'trade_fee': float,
                                'trade_price': float,
                                'trade_turnover': float,
                                'trade_volume': float
                            }
                        ]
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('组合查询用户历史成交记录（逐仓）')
    def test_linear_matchresults_exact(self,linear_contract_code,symbol):
        r = t.linear_matchresults_exact(contract_code=linear_contract_code,
                                        trade_type='0',
                                        start_time='',
                                        end_time='',
                                        from_id='',
                                        size='',
                                        direct='')
        pprint(r)
        schema = {
                    'data': {
                        'next_id': int,
                        'remain_size': int,
                        'trades': [
                            {
                                'contract_code': linear_contract_code,
                                'create_date': int,
                                'direction': str,
                                'fee_asset': 'USDT',
                                'id': str,
                                'margin_account': str,
                                'margin_mode': 'isolated',
                                'match_id': int,
                                'offset': str,
                                'offset_profitloss': float,
                                'order_id': int,
                                'order_id_str': str,
                                'order_source': str,
                                'real_profit': float,
                                'role': str,
                                'symbol': symbol,
                                'trade_fee': float,
                                'trade_price': float,
                                'trade_turnover': float,
                                'trade_volume': float,
                                'query_id': int
                            }
                        ]
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('获取当前可用合约总持仓量')
    def test_linear_open_interest(self,linear_contract_code,symbol):
        r = t.linear_open_interest(contract_code=linear_contract_code)
        pprint(r)
        schema = {
            'data': [
                {
                    'symbol': symbol,
                    'contract_code': linear_contract_code,
                    'trade_amount': float,
                    'trade_turnover': float,
                    'trade_volume': int,
                    'volume': float,
                    'value': float,
                    'amount': float
                    }
                ],
            'status': 'ok',
            'ts': int
        }
        Schema(schema).validate(r)

    @allure.title('获取用户的合约当前未成交委托')
    def test_linear_openorders(self,linear_contract_code,symbol):
        t.linear_order(contract_code=linear_contract_code,
                       client_order_id='',
                       price=self.sell_price-1,
                       volume='1',
                       direction='buy',
                       offset='open',
                       lever_rate=self.lever_rate,
                       order_price_type='limit')
        time.sleep(1)
        r = t.linear_openorders(contract_code=linear_contract_code,
                                page_index='',
                                page_size='')
        pprint(r)
        schema = {
                    'data': {
                        'current_page': int,
                        'orders': [
                            {
                                'canceled_at': Or(int,str,None),
                                'client_order_id':  Or(int,str,None),
                                'contract_code': linear_contract_code,
                                'created_at': int,
                                'direction': str,
                                'fee': Or(int,float),
                                'fee_asset': 'USDT',
                                'is_tpsl': Or(0,1),
                                'lever_rate': int,
                                'liquidation_type': Or(str,None),
                                'margin_account': str,
                                'margin_asset': 'USDT',
                                'margin_frozen': Or(int,float,None),
                                'margin_mode': 'isolated',
                                'offset': str,
                                'order_id': int,
                                'order_id_str': str,
                                'order_price_type': str,
                                'order_source': str,
                                'order_type': int,
                                'price': Or(int,float),
                                'profit': Or(int,float),
                                'real_profit':  Or(int,float),
                                'status': int,
                                'symbol': symbol,
                                'trade_avg_price': Or(int,float,None),
                                'trade_turnover': Or(int,float,None),
                                'trade_volume': int,
                                'update_time': int,
                                'volume': int
                            }
                        ],
                        'total_page': int,
                        'total_size': int
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)



    @allure.title('合约下单(逐仓)')
    def test_linear_order1(self,linear_contract_code):
        r = t.linear_order(contract_code=linear_contract_code,
                           client_order_id='',
                           price=self.buy_price-1,
                           volume='1',
                           direction='buy',
                           offset='open',
                           lever_rate=self.lever_rate,
                           order_price_type='limit')
        pprint(r)
        schema = {
                    'data': {
                        'order_id': int,
                        'order_id_str': str
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('合约下单(逐仓)(client_order_id)')
    def test_linear_order2(self,linear_contract_code):
        r = t.linear_order(contract_code=linear_contract_code,
                           client_order_id=random.randint(1, 999999),
                           price=self.buy_price-1,
                           volume='1',
                           direction='buy',
                           offset='open',
                           lever_rate=self.lever_rate,
                           order_price_type='limit')
        pprint(r)
        schema = {
                    'data': {
                        'order_id': int,
                        'order_id_str': str,
                        'client_order_id': int
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('获取用户的合约订单明细信息')
    def test_linear_order_detail(self,linear_contract_code,symbol):
        a = t.linear_order(contract_code=linear_contract_code,
                       client_order_id='',
                       price=self.sell_price,
                       volume='1',
                       direction='buy',
                       offset='open',
                       lever_rate=self.lever_rate,
                       order_price_type='limit')
        time.sleep(3)
        order_id = a['data']['order_id']
        created_at = a['ts']
        r = t.linear_order_detail(contract_code=linear_contract_code,
                                  order_id=order_id,
                                  created_at=created_at,
                                  order_type='1',
                                  page_index='1',
                                  page_size='20')
        pprint(r)
        schema1 = {
                    'data': {
                        'adjust_value': Or(int,float),
                        'canceled_at': int,
                        'client_order_id': Or(str,None),
                        'contract_code': linear_contract_code,
                        'created_at': int,
                        'current_page': int,
                        'direction': str,
                        'fee': Or(int,float),
                        'fee_asset': 'USDT',
                        'final_interest': int,
                        'instrument_price': Or(int,float),
                        'is_tpsl': Or(0,1),
                        'lever_rate': int,
                        'liquidation_type': str,
                        'margin_account': str,
                        'margin_asset': 'USDT',
                        'margin_frozen': Or(float,int),
                        'margin_mode': 'isolated',
                        'offset': str,
                        'order_id': int,
                        'order_id_str': str,
                        'order_price_type': str,
                        'order_source': str,
                        'order_type': str,
                        'price': Or(int,float),
                        'profit': float,
                        'real_profit': Or(int,float),
                        'status': int,
                        'symbol': symbol,
                        'total_page': int,
                        'total_size': int,
                        'trade_avg_price': Or(int,float,None),
                        'trade_turnover': float,
                        'trade_volume': float,
                        'trades': [
                            {'created_at': int,
                             'fee_asset': 'USDT',
                             'id': str,
                             'profit': float,
                             'real_profit': float,
                             'role': str,
                             'trade_fee': float,
                             'trade_id': int,
                             'trade_price': float,
                             'trade_turnover': float,
                             'trade_volume': float}
                        ],
                        'volume': float
                    },
                    'status': 'ok',
                    'ts': int
                }

        schema2 = {'created_at': int,
                 'fee_asset': 'USDT',
                 'id': str,
                 'profit': float,
                 'real_profit': float,
                 'role': str,
                 'trade_fee': float,
                 'trade_id': int,
                 'trade_price': float,
                 'trade_turnover': float,
                 'trade_volume': float}

        Schema(schema1).validate(r)
        Schema(schema2).validate(r['data']['trades'][0])

    @allure.title('获取用户的合约订单信息')
    def test_linear_order_info(self,linear_contract_code,symbol):
        a = t.linear_order(contract_code=linear_contract_code,
                       client_order_id='',
                       price=self.sell_price,
                       volume='1',
                       direction='buy',
                       offset='open',
                       lever_rate=self.lever_rate,
                       order_price_type='limit')
        time.sleep(1)
        order_id = a['data']['order_id']
        r = t.linear_order_info(contract_code=linear_contract_code,
                                order_id=order_id)
        pprint(r)
        schema = {
                    'data': [
                        {
                            'canceled_at': int,
                            'client_order_id': Or(None,int),
                            'contract_code': linear_contract_code,
                            'created_at': int,
                            'direction': str,
                            'fee': Or(int,float),
                            'fee_asset': 'USDT',
                            'is_tpsl': Or(0,1),
                            'lever_rate': int,
                            'liquidation_type': str,
                            'margin_account': str,
                            'margin_asset': 'USDT',
                            'margin_frozen': Or(float,None),
                            'margin_mode': 'isolated',
                            'offset': str,
                            'order_id': int,
                            'order_id_str': str,
                            'order_price_type': str,
                            'order_source': str,
                            'order_type': int,
                            'price': Or(int,float),
                            'profit': Or(int,float),
                            'real_profit': Or(int,float),
                            'status': int,
                            'symbol': symbol,
                            'trade_avg_price': Or(int,float,None),
                            'trade_turnover': Or(float,int),
                            'trade_volume': int,
                            'update_time': Or(int,None),
                            'volume': int
                        }
                    ],
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('获取用户的合约下单量限制')
    def test_linear_order_limit(self,linear_contract_code,symbol):
        r = t.linear_order_limit(contract_code=linear_contract_code,order_price_type='limit')
        pprint(r)
        schema = {
                    'data': {
                        'list': [
                            {
                                'close_limit': Or(float,None),
                                'contract_code': linear_contract_code,
                                'open_limit': Or(float,None),
                                'symbol': symbol
                            }
                        ],
                        'order_price_type': str
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('获取溢价指数K线数据')
    def test_linear_premium_index_kline(self,linear_contract_code,symbol):
        r = t.linear_premium_index_kline(contract_code=linear_contract_code,period='1min',size='200')
        pprint(r)
        schema = {'ch': 'market.{}.premium_index.{}'.format(linear_contract_code,'1min'),
                  'data': [{'amount': str,
                             'close': str,
                             'count': str,
                             'high': str,
                             'id': int,
                             'low': str,
                             'open': str,
                             'vol': str}],
                  'status': 'ok',
                  'ts': int}
        Schema(schema).validate(r)

    @allure.title('获取合约最高限价和最低限价')
    def test_linear_price_limit(self,linear_contract_code,symbol):
        r = t.linear_price_limit(contract_code=linear_contract_code)
        pprint(r)
        schema = {
                    'data': [
                        {
                            'high_limit': Or(float,None),
                            'contract_code': linear_contract_code,
                            'low_limit': Or(float,None),
                            'symbol': symbol
                        }
                    ],
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('查询开仓单关联的止盈止损订单详情（逐仓）')
    def test_linear_relation_tpsl_order(self,linear_contract_code):
        a = t.linear_order(contract_code=linear_contract_code,
                           client_order_id='',
                           price=self.sell_price,
                           volume='1',
                           direction='buy',
                           offset='open',
                           lever_rate=self.lever_rate,
                           order_price_type='limit',
                           tp_trigger_price=self.sell_price+100,
                           tp_order_price=self.sell_price+100,
                           tp_order_price_type='limit',
                           sl_order_price=self.sell_price-100,
                           sl_order_price_type='limit',
                           sl_trigger_price=self.sell_price-100)
        time.sleep(1)
        order_id = a['data']['order_id']
        r = t.linear_relation_tpsl_order(contract_code=linear_contract_code,
                                         order_id=order_id)
        pprint(r)
        schema = {'data': {'canceled_at': int,
                          'client_order_id': Or(int,str,None),
                          'contract_code': linear_contract_code,
                          'created_at': int,
                          'direction': str,
                          'fee': float,
                          'fee_asset': 'USDT',
                          'lever_rate': int,
                          'margin_account': linear_contract_code,
                          'margin_frozen': float,
                          'margin_mode': 'isolated',
                          'offset': str,
                          'order_id': int,
                          'order_id_str': str,
                          'order_price_type': str,
                          'order_source': str,
                          'order_type': int,
                          'price': Or(int,float),
                          'profit': Or(int,float),
                          'status': int,
                          'symbol': str,
                          'tpsl_order_info': [{'canceled_at': int,
                                               'created_at': int,
                                               'direction': str,
                                               'fail_code': Or(None,str),
                                               'fail_reason': Or(None,str),
                                               'order_id': int,
                                               'order_id_str': str,
                                               'order_price': float,
                                               'order_price_type': str,
                                               'relation_order_id': str,
                                               'relation_tpsl_order_id': str,
                                               'status': int,
                                               'tpsl_order_type': str,
                                               'trigger_price': float,
                                               'trigger_type': str,
                                               'triggered_price': Or(int,float,None),
                                               'volume': float},],
                          'trade_avg_price': float,
                          'trade_turnover': float,
                          'trade_volume': int,
                          'volume': int},
                 'status': 'ok',
                 'ts': int}

        Schema(schema).validate(r)

    @allure.title('查询合约风险准备金和预估分摊比例')
    def test_linear_risk_info(self,linear_contract_code):
        r = t.linear_risk_info(contract_code=linear_contract_code)
        pprint(r)
        schema = {
                    'data': [
                        {
                            'contract_code': linear_contract_code,
                            'estimated_clawback': float,
                            'insurance_fund': float
                        }
                    ],
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('查询平台历史结算记录（全逐通用）')
    def test_linear_settlement_records(self,linear_contract_code,symbol):
        r = t.linear_settlement_records(contract_code=linear_contract_code,
                                        start_time='',
                                        end_time='',
                                        page_size='',
                                        page_index='')
        pprint(r)
        schema = {'data': {'current_page': int,
                          'settlement_record': [{'clawback_ratio': float,
                                                 'contract_code': linear_contract_code,
                                                 'settlement_price': float,
                                                 'settlement_time': int,
                                                 'settlement_type': 'settlement',
                                                 'symbol': symbol},],
                          'total_page': int,
                          'total_size': int},
                 'status': 'ok',
                 'ts': int}

        Schema(schema).validate(r)

    @allure.title('查询母账户下的单个子账户资产信息')
    def test_linear_sub_account_info(self,linear_contract_code,sub_uid,symbol):
        r = t.linear_sub_account_info(contract_code=linear_contract_code,sub_uid=sub_uid)
        pprint(r)
        schema = {
                    'data': [
                        {
                            'adjust_factor': float,
                            'contract_code': linear_contract_code,
                            'lever_rate': int,
                            'liquidation_price': Or(int,float,None),
                            'margin_account': str,
                            'margin_asset': 'USDT',
                            'margin_available': float,
                            'margin_balance': float,
                            'margin_frozen': Or(int,float),
                            'margin_mode': 'isolated',
                            'margin_position': Or(int,float),
                            'margin_static': Or(int,float),
                            'profit_real': float,
                            'profit_unreal': Or(int,float),
                            'risk_rate': Or(float,None),
                            'symbol': symbol,
                            'withdraw_available': Or(int,float)
                        }
                    ],
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)




    @allure.title('批量获取子账户资产信息（逐仓）')
    def test_linear_sub_account_info_list(self,linear_contract_code,symbol):
        r = t.linear_sub_account_info_list(contract_code=linear_contract_code,page_index='',page_size='')
        pprint(r)
        schema = {'data': {'current_page': int,
          'sub_list': [{'account_info_list': [{'contract_code': linear_contract_code,
                                               'liquidation_price': Or(float,None),
                                               'margin_account': linear_contract_code,
                                               'margin_asset': 'USDT',
                                               'margin_balance': Or(float,0),
                                               'margin_mode': 'isolated',
                                               'risk_rate': Or(float,None),
                                               'symbol': symbol}],
                                                'sub_uid': int}],
                                  'total_page': int,
                                  'total_size': int},
                         'status': 'ok',
                         'ts': int}

        Schema(schema).validate(r)

    @allure.title('查询母账户下所有子账户资产信息')
    def test_linear_sub_account_list(self,linear_contract_code,symbol):
        r = t.linear_sub_account_list(contract_code=linear_contract_code)
        pprint(r)
        schema = {
                    'data': [
                        {
                            'list': [
                                {
                                    'contract_code': linear_contract_code,
                                    'liquidation_price': Or(int,float,None),
                                    'margin_account': str,
                                    'margin_asset': 'USDT',
                                    'margin_balance': Or(int,float,None),
                                    'margin_mode': 'isolated',
                                    'risk_rate': Or(int,float,None),
                                    'symbol': symbol
                                }
                            ],
                            'sub_uid': int
                        }
                    ],
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('批量设置子账户交易权限（全逐通用）')
    def test_linear_sub_auth(self,sub_uid):
        r = t.linear_sub_auth(sub_uid=sub_uid,sub_auth='1')
        pprint(r)
        schema = {'data': {'errors': list,
                           'successes': str},
                         'status': 'ok',
                         'ts': int}

        Schema(schema).validate(r)

    @allure.title('查询母账户下的单个子账户持仓信息')
    def test_linear_sub_position_info(self,linear_contract_code,sub_uid,symbol):
        r = t.linear_sub_position_info(contract_code=linear_contract_code,sub_uid=sub_uid)
        pprint(r)
        schema = {
                    'data': [
                        {
                            'available': float,
                            'contract_code': linear_contract_code,
                            'cost_hold': float,
                            'cost_open': float,
                            'direction': str,
                            'frozen': float,
                            'last_price': Or(float,int),
                            'lever_rate': int,
                            'margin_asset': 'USDT',
                            'margin_account': str,
                            'margin_mode': 'isolated',
                            'position_margin': float,
                            'profit': float,
                            'profit_rate': float,
                            'profit_unreal': float,
                            'symbol': symbol,
                            'volume': float
                        }
                    ],
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('获取标记价格的K线数据（全逐通用）')
    def test_linear_swap_mark_price_kline(self,linear_contract_code):
        r = t.linear_swap_mark_price_kline(contract_code=linear_contract_code,period='1min',size='200')
        pprint(r)
        schema = {'ch': 'market.{}.mark_price.{}'.format(linear_contract_code,'1min'),
                  'data': [{'amount': str,
                             'close': str,
                             'count': str,
                             'high': str,
                             'id': int,
                             'low': str,
                             'open': str,
                             'trade_turnover': str,
                             'vol': str}],
                  'status': 'ok',
                  'ts': int}
        Schema(schema).validate(r)

    @allure.title('切换杠杆倍数 （逐仓）')
    def test_linear_switch_lever_rate(self,linear_contract_code,symbol):
        r = t.linear_switch_lever_rate(contract_code=linear_contract_code,lever_rate='5')
        pprint(r)
        schema = {'data': {'contract_code': linear_contract_code,
                          'lever_rate': int,
                          'margin_mode': 'isolated'},
                 'status': 'ok',
                 'ts': int}

        Schema(schema).validate(r)

    @allure.title('止盈止损订单撤单（逐仓）')
    def test_linear_tpsl_cancel(self,linear_contract_code):
        t.linear_order(contract_code=linear_contract_code,
                           client_order_id='',
                           price=self.sell_price,
                           volume='1',
                           direction='buy',
                           offset='open',
                           lever_rate=self.lever_rate,
                           order_price_type='limit')

        a = t.linear_tpsl_order(contract_code=linear_contract_code,
                                direction='sell',
                                volume='1',
                                tp_trigger_price=self.sell_price+100,
                                tp_order_price=self.sell_price+100,
                                tp_order_price_type='limit',
                                sl_order_price=self.sell_price-100,
                                sl_order_price_type='limit',
                                sl_trigger_price=self.sell_price-100)
        time.sleep(1)
        order_id = a['data']['tp_order']['order_id']
        r = t.linear_tpsl_cancel(contract_code=linear_contract_code,
                                 order_id=order_id)
        pprint(r)
        schema = {'data': {'errors': list,
                           'successes': str},
                             'status': 'ok',
                             'ts': int}

        Schema(schema).validate(r)



    @allure.title('止盈止损订单全部撤单（逐仓）')
    def test_linear_tpsl_cancel(self,linear_contract_code):
        t.linear_order(contract_code=linear_contract_code,
                           client_order_id='',
                           price=self.sell_price,
                           volume='1',
                           direction='buy',
                           offset='open',
                           lever_rate=self.lever_rate,
                           order_price_type='limit')

        a = t.linear_tpsl_order(contract_code=linear_contract_code,
                                direction='sell',
                                volume='1',
                                tp_trigger_price=self.sell_price+100,
                                tp_order_price=self.sell_price+100,
                                tp_order_price_type='limit',
                                sl_order_price=self.sell_price-100,
                                sl_order_price_type='limit',
                                sl_trigger_price=self.sell_price-100)
        time.sleep(1)
        r = t.linear_tpsl_cancelall(contract_code=linear_contract_code)
        pprint(r)
        schema = {'data': {'errors': list,
                           'successes': str},
                  'status': 'ok',
                  'ts': int}

        Schema(schema).validate(r)

    @allure.title('查询止盈止损订单历史委托（逐仓）')
    def test_linear_tpsl_hisorders(self,linear_contract_code,symbol):
        r = t.linear_tpsl_hisorders(contract_code=linear_contract_code,
                                    status='0',
                                    create_date='7',
                                    page_size='',
                                    page_index='',
                                    sort_by='')
        pprint(r)
        schema = {'data': {'current_page': int,
                          'orders': [{'canceled_at': int,
                                      'contract_code': linear_contract_code,
                                      'created_at': int,
                                      'direction': str,
                                      'fail_code': Or(str,None),
                                      'fail_reason': Or(str,None),
                                      'margin_account': linear_contract_code,
                                      'margin_mode': 'isolated',
                                      'order_id': int,
                                      'order_id_str': str,
                                      'order_price': float,
                                      'order_price_type': str,
                                      'order_source': str,
                                      'order_type': int,
                                      'relation_order_id': str,
                                      'relation_tpsl_order_id': str,
                                      'source_order_id': Or(int,None,str),
                                      'status': int,
                                      'symbol': str,
                                      'tpsl_order_type': str,
                                      'trigger_price': float,
                                      'trigger_type': str,
                                      'triggered_price': Or(str,None),
                                      'update_time': int,
                                      'volume': float},],
                          'total_page': int,
                          'total_size': int},
                 'status': 'ok',
                 'ts': int}

        Schema(schema).validate(r)

    @allure.title('查询止盈止损订单当前委托（逐仓）')
    def test_linear_tpsl_openorders(self,linear_contract_code,symbol):
        t.linear_order(contract_code=linear_contract_code,
                           client_order_id='',
                           price=self.sell_price,
                           volume='1',
                           direction='buy',
                           offset='open',
                           lever_rate=self.lever_rate,
                           order_price_type='limit')

        a = t.linear_tpsl_order(contract_code=linear_contract_code,
                                direction='sell',
                                volume='1',
                                tp_trigger_price=self.sell_price+100,
                                tp_order_price=self.sell_price+100,
                                tp_order_price_type='limit',
                                sl_order_price=self.sell_price-100,
                                sl_order_price_type='limit',
                                sl_trigger_price=self.sell_price-100)
        time.sleep(1)

        r = t.linear_tpsl_openorders(contract_code=linear_contract_code,
                                     page_index='',
                                     page_size='')
        pprint(r)
        schema = {'data': {'current_page': int,
                          'orders': [{'contract_code': linear_contract_code,
                                      'created_at': int,
                                      'direction': str,
                                      'margin_account': linear_contract_code,
                                      'margin_mode': 'isolated',
                                      'order_id': int,
                                      'order_id_str': str,
                                      'order_price': float,
                                      'order_price_type': str,
                                      'order_source': str,
                                      'order_type': int,
                                      'relation_tpsl_order_id': str,
                                      'source_order_id': Or(int,None),
                                      'status': int,
                                      'symbol': symbol,
                                      'tpsl_order_type': str,
                                      'trigger_price': float,
                                      'trigger_type': str,
                                      'volume': float},],
                          'total_page': int,
                          'total_size': int},
                 'status': 'ok',
                 'ts': int}

        Schema(schema).validate(r)



    @allure.title('对仓位设置止盈止损订单（逐仓）')
    def test_linear_tpsl_order(self,linear_contract_code):
        t.linear_order(contract_code=linear_contract_code,
                           client_order_id='',
                           price=self.sell_price,
                           volume='1',
                           direction='buy',
                           offset='open',
                           lever_rate=self.lever_rate,
                           order_price_type='limit')

        r = t.linear_tpsl_order(contract_code=linear_contract_code,
                                direction='sell',
                                volume='1',
                                tp_trigger_price=self.sell_price+100,
                                tp_order_price=self.sell_price+100,
                                tp_order_price_type='limit',
                                sl_order_price=self.sell_price-100,
                                sl_order_price_type='limit',
                                sl_trigger_price=self.sell_price-100)
        time.sleep(1)
        pprint(r)
        schema = {'data': {'sl_order': {'order_id': int,
                            'order_id_str': str},
                          'tp_order': {'order_id': int,
                                       'order_id_str': str}},
                         'status': 'ok',
                         'ts': int}

        Schema(schema).validate(r)

    @allure.title('跟踪委托撤单')
    def test_linear_track_cancel(self,linear_contract_code):
        a = t.linear_track_order(contract_code=linear_contract_code,
                                 direction='buy',
                                 offset='open',
                                 lever_rate=self.lever_rate,
                                 volume='1',
                                 callback_rate='0.01',
                                 active_price=self.last_price-100,
                                 order_price_type='formula_price')
        time.sleep(1)
        order_id = a['data']['order_id']
        r = t.linear_track_cancel(contract_code=linear_contract_code,
                                  order_id=order_id)
        pprint(r)
        schema = {'data': {'errors': list,
                           'successes': str},
                         'status': 'ok',
                         'ts': int}

        Schema(schema).validate(r)

    @allure.title('跟踪委托全部撤单')
    def test_linear_track_cancelall(self,linear_contract_code):
        a = t.linear_track_order(contract_code=linear_contract_code,
                                 direction='buy',
                                 offset='open',
                                 lever_rate=self.lever_rate,
                                 volume='1',
                                 callback_rate='0.01',
                                 active_price=self.last_price-100,
                                 order_price_type='formula_price')
        time.sleep(1)
        r = t.linear_track_cancelall(contract_code=linear_contract_code)
        pprint(r)
        schema = {'data': {'errors': list,
                           'successes': str},
                         'status': 'ok',
                         'ts': int}

        Schema(schema).validate(r)


    @allure.title('获取跟踪委托历史委托')
    def test_linear_track_hisorders(self,linear_contract_code,symbol):
        r = t.linear_track_hisorders(contract_code=linear_contract_code,
                                     status='0',
                                     trade_type='0',
                                     create_date='7',
                                     page_size='',
                                     page_index='',
                                     sort_by='')
        pprint(r)
        schema = {'data': {'current_page': int,
                          'orders': [{'active_price': float,
                                      'callback_rate': float,
                                      'canceled_at': int,
                                      'contract_code': linear_contract_code,
                                      'created_at': int,
                                      'direction': str,
                                      'fail_code': Or(None,str),
                                      'fail_reason': Or(None,str),
                                      'formula_price': Or(None,str,int,float),
                                      'is_active': int,
                                      'lever_rate': int,
                                      'margin_account': linear_contract_code,
                                      'margin_mode': 'isolated',
                                      'market_limit_price': Or(None,int,float,str),
                                      'offset': str,
                                      'order_id': int,
                                      'order_id_str': str,
                                      'order_price_type': str,
                                      'order_source': str,
                                      'order_type': int,
                                      'real_volume': Or(int,float),
                                      'relation_order_id': str,
                                      'status': int,
                                      'symbol': symbol,
                                      'triggered_price': Or(None,int,str,float),
                                      'update_time': int,
                                      'volume': float},],
                          'total_page': int,
                          'total_size': int},
                 'status': 'ok',
                 'ts': int}

        Schema(schema).validate(r)

    @allure.title('获取跟踪委托当前委托')
    def test_linear_track_openorders(self,linear_contract_code,symbol):
        t.linear_track_order(contract_code=linear_contract_code,
                                 direction='buy',
                                 offset='open',
                                 lever_rate=self.lever_rate,
                                 volume='1',
                                 callback_rate='0.01',
                                 active_price=self.sell_price-100,
                                 order_price_type='formula_price')
        time.sleep(1)
        r = t.linear_track_openorders(contract_code=linear_contract_code,
                                      page_index='',
                                      page_size='')
        pprint(r)
        schema = {'data': {'current_page': int,
                          'orders': [{'active_price': float,
                                      'callback_rate': float,
                                      'contract_code': linear_contract_code,
                                      'created_at': int,
                                      'direction': str,
                                      'is_active': int,
                                      'lever_rate': int,
                                      'margin_account': linear_contract_code,
                                      'margin_mode': 'isolated',
                                      'offset': str,
                                      'order_id': int,
                                      'order_id_str': str,
                                      'order_price_type': str,
                                      'order_source': str,
                                      'order_type': int,
                                      'status': int,
                                      'symbol': symbol,
                                      'volume': float}],
                          'total_page': int,
                          'total_size': int},
                 'status': 'ok',
                 'ts': int}

        Schema(schema).validate(r)


    @allure.title('跟踪委托下单')
    def test_linear_track_order(self,linear_contract_code):
        r = t.linear_track_order(contract_code=linear_contract_code,
                                 direction='buy',
                                 offset='open',
                                 lever_rate=self.lever_rate,
                                 volume='1',
                                 callback_rate='0.01',
                                 active_price=self.sell_price-100,
                                 order_price_type='formula_price')
        pprint(r)
        schema = {'data': {'order_id': int,
                           'order_id_str': str},
                         'status': 'ok',
                         'ts': int}

        Schema(schema).validate(r)

    @allure.title('获取市场最近成交记录')
    def test_linear_trade(self,linear_contract_code):
        r = t.linear_trade(contract_code=linear_contract_code)
        pprint(r)
        schema = {'ch': 'market.{}.trade.detail'.format(linear_contract_code),
                  'tick': {'data': [{'amount': str,
                                     'contract_code': linear_contract_code,
                                     'direction': str,
                                     'id': int,
                                     'price': str,
                                     'quantity': str,
                                     'trade_turnover': str,
                                     'ts': int}],
                             'id':int,
                              'ts': int},
                      'status': 'ok',
                      'ts': int}
        Schema(schema).validate(r)

    @allure.title('同账号不同保证金账户的划转')
    def test_linear_transfer_inner(self,linear_contract_code):
        r = t.linear_transfer_inner(asset='usdt',from_margin_account=linear_contract_code,to_margin_account='eth-usdt',amount='1')
        pprint(r)
        schema = {
                    'data': {
                        'order_id': str
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('获取用户的合约划转限制')
    def test_linear_transfer_limit(self,linear_contract_code,symbol):
        r = t.linear_transfer_limit(contract_code=linear_contract_code)
        pprint(r)
        schema = {
                    'data': [
                        {
                            'contract_code': linear_contract_code,
                            'margin_account': str,
                            'margin_mode': 'isolated',
                            'net_transfer_in_max_daily': float,
                            'net_transfer_out_max_daily': float,
                            'symbol': symbol,
                            'transfer_in_max_daily': float,
                            'transfer_in_max_each': float,
                            'transfer_in_min_each': float,
                            'transfer_out_max_daily': float,
                            'transfer_out_max_each': float,
                            'transfer_out_min_each': float
                        }
                    ],
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('合约计划委托撤单')
    def test_linear_trigger_cancel(self,linear_contract_code):
        a = t.linear_trigger_order(contract_code=linear_contract_code,
                                   trigger_type='le',
                                   trigger_price=self.last_price-100,
                                   order_price=self.last_price-100,
                                   order_price_type='limit',
                                   volume='1',
                                   direction='buy',
                                   offset='open',
                                   lever_rate=self.lever_rate)
        time.sleep(1)
        order_id = a['data']['order_id']
        r = t.linear_trigger_cancel(contract_code=linear_contract_code,
                                    order_id=order_id)
        pprint(r)
        schema = {
                    'data': {
                        'errors': [

                        ],
                        'successes': str
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('合约计划委托全部撤单')
    def test_linear_trigger_cancelall(self,linear_contract_code):
        t.linear_trigger_order(contract_code=linear_contract_code,
                                   trigger_type='le',
                                   trigger_price=self.last_price-100,
                                   order_price=self.last_price-100,
                                   order_price_type='limit',
                                   volume='1',
                                   direction='buy',
                                   offset='open',
                                   lever_rate=self.lever_rate)
        time.sleep(1)

        r = t.linear_trigger_cancelall(contract_code=linear_contract_code)
        pprint(r)
        schema = {
                    'data': {
                        'errors': [

                        ],
                        'successes': str
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('获取计划委托历史委托')
    def test_linear_trigger_hisorders(self,linear_contract_code,symbol):
        r = t.linear_trigger_hisorders(contract_code=linear_contract_code,
                                       trade_type='1',
                                       status='0',
                                       create_date='7',
                                       page_index='',
                                       page_size='')
        pprint(r)
        schema = {
                    'data': {
                        'current_page': int,
                        'orders': [
                            {
                                'canceled_at': Or(int,None),
                                'contract_code': linear_contract_code,
                                'created_at': int,
                                'direction': 'buy',
                                'fail_code': Or(int,None),
                                'fail_reason': Or(str,None),
                                'lever_rate': int,
                                'margin_account': str,
                                'margin_mode': 'isolated',
                                'offset': str,
                                'order_id': int,
                                'order_id_str': str,
                                'order_insert_at': int,
                                'order_price': float,
                                'order_price_type': str,
                                'order_source': str,
                                'order_type': int,
                                'relation_order_id': str,
                                'status': int,
                                'symbol': symbol,
                                'trigger_price': float,
                                'trigger_type': Or('ge','le'),
                                'triggered_at': Or(int,None),
                                'triggered_price': Or(int,float,None),
                                'update_time': int,
                                'volume': float
                            }
                        ],
                        'total_page': int,
                        'total_size': int
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('获取计划委托当前委托')
    def test_linear_trigger_openorders(self,linear_contract_code,symbol):
        a = t.linear_trigger_order(contract_code=linear_contract_code,
                                   trigger_type='le',
                                   trigger_price=self.last_price-100,
                                   order_price=self.last_price-100,
                                   order_price_type='limit',
                                   volume='1',
                                   direction='buy',
                                   offset='open',
                                   lever_rate=self.lever_rate)
        time.sleep(1)
        r = t.linear_trigger_openorders(contract_code=linear_contract_code,
                                       page_index='',
                                       page_size='')
        pprint(r)
        schema = {
                    'data': {
                        'current_page': int,
                        'orders': [
                            {
                                'contract_code': linear_contract_code,
                                'created_at': int,
                                'direction': str,
                                'lever_rate': int,
                                'margin_account': str,
                                'margin_mode': 'isolated',
                                'offset': str,
                                'order_id': int,
                                'order_id_str': str,
                                'order_price': float,
                                'order_price_type': str,
                                'order_source': str,
                                'order_type': int,
                                'status': int,
                                'symbol': symbol,
                                'trigger_price': float,
                                'trigger_type': str,
                                'volume': float
                            }
                        ],
                        'total_page': int,
                        'total_size': int
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('合约计划委托下单')
    def test_linear_trigger_order(self,linear_contract_code):
        r = t.linear_trigger_order(contract_code=linear_contract_code,
                                   trigger_type='le',
                                   trigger_price=self.last_price-100,
                                   order_price=self.last_price-100,
                                   order_price_type='limit',
                                   volume='1',
                                   direction='buy',
                                   offset='open',
                                   lever_rate=self.lever_rate)
        pprint(r)
        schema = {
                    'data': {
                        'order_id': int,
                        'order_id_str': str
                    },
                    'status': 'ok',
                    'ts': int
                }

        Schema(schema).validate(r)

    @allure.title('查询用户结算记录（逐仓）')
    def test_linear_user_settlement_records(self,linear_contract_code,symbol):
        r = t.linear_user_settlement_records(contract_code=linear_contract_code,
                                             start_time='',
                                             end_time='',
                                             page_size='',
                                             page_index='')
        pprint(r)
        schema = {'data': {'current_page': int,
                  'settlement_records': [{'clawback': float,
                                          'contract_code': linear_contract_code,
                                          'fee': float,
                                          'fee_asset': 'USDT',
                                          'funding_fee': float,
                                          'margin_account': linear_contract_code,
                                          'margin_balance': Or(float,int),
                                          'margin_balance_init': Or(float,int),
                                          'margin_mode': 'isolated',
                                          'offset_profitloss': float,
                                          'positions': [{'contract_code': linear_contract_code,
                                                         'cost_hold': float,
                                                         'cost_hold_pre': float,
                                                         'cost_open': float,
                                                         'direction': str,
                                                         'settlement_price': float,
                                                         'settlement_profit_unreal': float,
                                                         'settlement_type': 'settlement',
                                                         'symbol': symbol,
                                                         'volume': float},],
                                          'settlement_profit_real': float,
                                          'settlement_time': int,
                                          'symbol': symbol},],
                                          'total_page': int,
                                          'total_size': int},
                                 'status': 'ok',
                                 'ts': int}

        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()




