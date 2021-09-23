#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : zhangranghan


from common.LinearServiceAPI import t as linear_api

from schema import Schema, And, Or, Regex, SchemaError
from pprint import pprint
import pytest, allure, random, time
from tool.get_test_data import case_data


@allure.epic('反向交割')
@allure.feature('')
class TestUSDTSwapLever_001:

    def setUp(self, contract_code):
        print('\n全部撤单')
        r = linear_api.linear_cross_cancelall(contract_code=contract_code)
        pprint(r)
    # @allure.title('{title}')
    def test_contract_account_position_info(self, contract_code):

        self.setUp(contract_code)
        time.sleep(0.2)
        r = linear_api.linear_cross_available_level_rate(contract_code=contract_code)
        pprint(r)
        availableleverlist = r['data'][0]['available_level_rate'].split(',')

        i = random.choice(availableleverlist)
        r = linear_api.linear_cross_switch_lever_rate(contract_code=contract_code, lever_rate=i)
        pprint(r)

        assert r['status'] == 'ok'


if __name__ == '__main__':
    pytest.main()
