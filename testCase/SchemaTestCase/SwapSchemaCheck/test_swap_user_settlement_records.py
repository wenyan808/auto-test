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
@allure.feature('查询用户结算记录')
class TestSwapUserSettlementRecords:

    def test_swap_user_settlement_records(self, contract_code):
        r = t.swap_user_settlement_records(contract_code=contract_code, start_time='', end_time='', page_index='1',
                                           page_size='10')



if __name__ == '__main__':
    pytest.main()
