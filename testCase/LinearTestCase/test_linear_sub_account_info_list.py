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
@allure.feature('批量获取子账户资产信息（逐仓）')
class TestLinearSubAccountInfoList:

    def test_linear_sub_account_info_list(self,contract_code,symbol):
        r = t.linear_sub_account_info_list(contract_code=contract_code,page_index='',page_size='')
        pprint(r)
        schema = {'data': {'current_page': int,
          'sub_list': [{'account_info_list': [{'contract_code': contract_code,
                                               'liquidation_price': Or(float,None),
                                               'margin_account': contract_code,
                                               'margin_asset': 'USDT',
                                               'margin_balance': Or(float,None),
                                               'margin_mode': 'isolated',
                                               'risk_rate': Or(float,None),
                                               'symbol': symbol}],
                                                'sub_uid': int}],
                                  'total_page': int,
                                  'total_size': int},
                         'status': 'ok',
                         'ts': int}

        Schema(schema).validate(r)



if __name__ == '__main__':
    pytest.main()
