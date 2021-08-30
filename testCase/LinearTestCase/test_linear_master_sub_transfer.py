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
@allure.feature('母子账户划转')
class TestLinearMasterSubTransfer:


    def test_linear_master_sub_transfer(self,sub_uid,contract_code):
        r = t.linear_master_sub_transfer(sub_uid=sub_uid,
                                         asset='usdt',
                                         from_margin_account=contract_code,
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


if __name__ == '__main__':
    pytest.main()
