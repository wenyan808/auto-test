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
@allure.feature('查询母账户下所有子账户资产信息')
class TestLinearSubaccountList:

    def test_linear_sub_account_list(self,contract_code,symbol):
        r = t.linear_sub_account_list(contract_code=contract_code)
        pprint(r)
        schema = {
                    'data': [
                        {
                            'list': [
                                {
                                    'contract_code': contract_code,
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




if __name__ == '__main__':
    pytest.main()
