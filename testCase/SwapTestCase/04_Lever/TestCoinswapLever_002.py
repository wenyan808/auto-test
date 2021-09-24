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

    @allure.title('title')
    def test_contract_account_position_info(self, contract_code):
        self.setUp(contract_code)
        time.sleep(0.1)
        '''查询支持的全部杠杆率，取随机一种下单，再切换另一种，预期失败'''
        r = swap_api.swap_available_level_rate(contract_code=contract_code)
        availableleverlist = r['data'][0]['available_level_rate'].split(',')

        i = random.choice(availableleverlist)
        availableleverlist.remove(i)
        j = random.choice(availableleverlist)
        '''下单任意一种杠杆'''
        r = swap_api.swap_order(contract_code=contract_code,
                                     client_order_id='',
                                     price='40001',
                                     volume='1',
                                     direction='buy',
                                     offset='open',
                                     lever_rate='5',
                                     order_price_type='limit')
        pprint(r)
        time.sleep(0.5)
        '''调整杠杆率'''
        r = swap_api.swap_switch_lever_rate(contract_code=contract_code, lever_rate=j)
        pprint(r)

        assert r['err_msg'] == '当前有挂单,无法切换倍数'


if __name__ == '__main__':
    pytest.main()
