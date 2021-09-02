#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/10/13
# @Author  : zhangranghan


from common.SwapServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema, And, Or, Regex, SchemaError

from pprint import pprint
import pytest, allure, random, time


@allure.epic('反向永续')
@allure.feature('母子账户划转')
class TestSwapMasterSubTransfer:

    def test_swap_master_sub_transfer(self, sub_uid, contract_code):
        r = t.swap_master_sub_transfer(sub_uid=sub_uid, contract_code=contract_code, amount='1', type='master_to_sub')
        schema = {'data': {'order_id': str},
                  'status': 'ok',
                  'ts': int}
        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
