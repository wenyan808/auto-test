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
@allure.feature('获取用户的合约账户和持仓信息')
class TestCoinSwapTransfer_006:

    def setUp(self):
        print('\n前置条件')

    @allure.title('{title}')
    def test_contract_account_position_info(self, symbol, contract_code):
        subuid = ""
        amount = "0.19"

        expectedresult = (symbol, float(amount))

        self.setUp()
        r = swap_api.swap_sub_account_info_list(contract_code=contract_code)
        pprint(r)
        sublist = r['data']['sub_list']
        if sublist != []:
            subuid = sublist[0]['sub_uid']

        r = swap_api.swap_master_sub_transfer(contract_code=contract_code,
                                              amount=amount,
                                              sub_uid=subuid,
                                              type='sub_to_master')
        pprint(r)
        time.sleep(0.8)
        r2 = swap_api.swap_financial_record(contract_code=contract_code,
                                            type='35',
                                            create_date='',
                                            page_index='',
                                            page_size='')
        pprint(r2)
        financial_record_lastest = r2['data']['financial_record'][0]

        actual = (financial_record_lastest['symbol'], financial_record_lastest['amount'])

        pprint(financial_record_lastest)

        assert actual == expectedresult


if __name__ == '__main__':
    pytest.main()
