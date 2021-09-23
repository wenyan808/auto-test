#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : zhangranghan


from common.ContractServiceAPI import t as contranct_api
from common.ContractServiceOrder import t as contranct_order

from schema import Schema, And, Or, Regex, SchemaError
from pprint import pprint
import pytest, allure, random, time
from tool.get_test_data import case_data


@allure.epic('反向交割')
@allure.feature('')
class TestContractLever_001:

    def setUp(self, symbol):
        print('\n全部撤单')
        r = contranct_api.contract_cancelall(symbol=symbol)
        pprint(r)
    @allure.title('title')
    def test_contract_account_position_info(self, symbol):

        self.setUp(symbol)

        r = contranct_api.contract_available_level_rate(symbol=symbol)
        availableleverlist = r['data'][0]['available_level_rate'].split(',')

        i = random.choice(availableleverlist)
        r = contranct_api.contract_switch_lever_rate(symbol=symbol, lever_rate=i)
        pprint(r)

        assert r['status'] == 'ok'


if __name__ == '__main__':
    pytest.main()
