#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/8/7
# @Author  : zhangranghan



from common.LinearServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError

from pprint import pprint
import pytest,allure,random,time




@allure.epic('正向永续')
@allure.feature('获取用户的合约历史成交记录')
class TestLinearMatchresults:


    def test_linear_matchresults(self,contract_code,symbol):
        r = t.linear_matchresults(contract_code=contract_code,
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
                                'contract_code': contract_code,
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




if __name__ == '__main__':
    pytest.main()
