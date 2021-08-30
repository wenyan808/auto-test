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
@allure.feature('获取母账户下的所有母子账户划转记录')
class TestLinearMasterSubTransferRecord:


    def test_linear_master_sub_transfer_record(self,contract_code):
        r = t.linear_master_sub_transfer_record(margin_account=contract_code,
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




if __name__ == '__main__':
    pytest.main()
