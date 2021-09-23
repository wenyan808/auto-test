#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : zhangranghan


from common.LinearServiceAPI import t as linear_api
from common.LinearServiceOrder import t as linear_order

from schema import Schema, And, Or, Regex, SchemaError
from pprint import pprint
import pytest, allure, random, time
from tool.get_test_data import case_data


@allure.epic('反向交割')
@allure.feature('获取用户的合约账户和持仓信息')
class TestUSDTSwapTransfer_003:

    def setUp(self):
        print('\n前置条件')

    # @allure.title('{title}')
    def test_contract_account_position_info(self, symbol, contract_code):
        from_margin_account = 'USDT'
        to_margin_account = contract_code
        amount = '6'

        expectedresult = (from_margin_account, -float(amount))

        self.setUp()

        r = linear_api.linear_transfer_inner(asset='usdt', from_margin_account=from_margin_account,
                                             to_margin_account=to_margin_account, amount=amount)
        pprint(r)
        time.sleep(3)

        r2 = linear_api.linear_financial_record(margin_account=from_margin_account,
                                                type='39',
                                                create_date='',
                                                page_index='',
                                                page_size='')
        #        pprint(r2)
        financial_record_lastest = r2['data']['financial_record'][0]

        actual = (financial_record_lastest['margin_account'], financial_record_lastest['amount'])

        pprint(financial_record_lastest)

        assert actual == expectedresult


if __name__ == '__main__':
    pytest.main()
