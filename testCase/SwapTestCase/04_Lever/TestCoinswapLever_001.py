#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : zhangranghan


from common.SwapServiceAPI import t as swap_api


from schema import Schema, And, Or, Regex, SchemaError
from pprint import pprint
import pytest, allure, random, time
from tool.get_test_data import case_data


@allure.epic('反向交割')
@allure.feature('')
class TestContractLever_001:

    def setUp(self, contract_code):
        print('\n全部撤单')
        r = swap_api.swap_cancelall(contract_code=contract_code)
        pprint(r)
    # @allure.title('{title}')
    def test_contract_account_position_info(self, contract_code):

        self.setUp(contract_code)

        r = swap_api.swap_available_level_rate(contract_code=contract_code)
        availableleverlist = r['data'][0]['available_level_rate'].split(',')
        time.sleep(0.1)
        i = random.choice(availableleverlist)
        r = swap_api.swap_switch_lever_rate(contract_code=contract_code, lever_rate=i)
        pprint(r)

        assert r['status'] == 'ok'


if __name__ == '__main__':
    pytest.main()
