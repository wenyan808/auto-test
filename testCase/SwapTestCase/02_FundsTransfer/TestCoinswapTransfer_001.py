#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : zhangranghan


from common.SwapServiceAPI import t as swap_api
from common.SwapServiceOrder import t as swap_order

from schema import Schema, And, Or, Regex, SchemaError
from pprint import pprint
import pytest, allure, random, time
from tool.get_test_data import case_data


@allure.epic('反向交割')
@allure.feature('获取用户的合约账户和持仓信息')
class TestCoinswapTransfer_001:

    def setUp(self):
        print('\n前置条件')


    def test_contract_account_position_info(self, symbol, contract_code):
        amount = 0.14

        expectedresult = (symbol, float(amount))

        self.setUp()

        r = swap_order.coinswap_transfer(currency=symbol, amount=amount, _from="spot", _to="swap")
        pprint(r)
        time.sleep(0.1)

        r2 = swap_api.swap_financial_record(contract_code=contract_code,
                                                type='14',
                                                create_date='',
                                                page_index='',
                                                page_size='')

        financial_record_lastest = r2['data']['financial_record'][0]

        actual = (financial_record_lastest['symbol'], financial_record_lastest['amount'])

        pprint(financial_record_lastest)

        assert actual == expectedresult


if __name__ == '__main__':
    pytest.main()
