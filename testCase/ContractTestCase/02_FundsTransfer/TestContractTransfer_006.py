#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : 张广南


from common.ContractServiceAPI import t as contranct_api
from common.ContractServiceOrder import t as contranct_order

from schema import Schema, And, Or, Regex, SchemaError
from pprint import pprint
import pytest, allure, random, time
from tool.get_test_data import case_data


@allure.epic('反向交割')
@allure.feature('获取用户的合约账户和持仓信息')
@pytest.mark.stable
class TestContractTransfer_006:

    def setUp(self):
        print('\n前置条件')


    def test_contract_account_position_info(self, symbol):
        subuid = ""
        amount = "0.20"

        expectedresult = (symbol, float(amount))

        self.setUp()
        r = contranct_api.contract_sub_account_info_list(symbol=symbol)
        pprint(r)
        sublist = r['data']['sub_list']
        if sublist != []:
            subuid = sublist[0]['sub_uid']

        r = contranct_api.contract_master_sub_transfer(symbol=symbol,
                                                       amount=amount,
                                                       sub_uid=subuid,
                                                       type='sub_to_master')
        pprint(r)
        time.sleep(2)
        r2 = contranct_api.contract_financial_record(symbol=symbol,
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
