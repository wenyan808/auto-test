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
@allure.feature('批量获取子账户资产信息（全仓）')
class TestLinearCrossSubAccountInfoList:

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



if __name__ == '__main__':
    pytest.main()
