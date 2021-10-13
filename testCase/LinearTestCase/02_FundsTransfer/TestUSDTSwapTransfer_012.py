#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : 张广南


from common.LinearServiceAPI import t as linear_api
from common.ContractServiceOrder import t as contranct_order

from schema import Schema, And, Or, Regex, SchemaError
from pprint import pprint
import pytest, allure, random, time
from tool.get_test_data import case_data


@allure.epic('反向交割')
@allure.feature('获取用户的合约账户和持仓信息')
@pytest.mark.stable
class TestUSDTSwapTransfer_012:

    def setUp(self):
        print('\n前置条件')


    def test_contract_account_position_info(self, symbol):
        subuid = ""
        amount = "1.6"
        asset = "USDT"
        from_margin_account = 'BTC-USDT'
        to_margin_account = 'ETH-USDT'
        expectedresult = (asset, float(amount))

        self.setUp()
        r = linear_api.linear_cross_sub_account_info_list(margin_account=asset)
        #pprint(r)
        sublist = r['data']['sub_list']
        if sublist != []:
            subuid = sublist[0]['sub_uid']
        pprint(subuid)
        r = linear_api.linear_master_sub_transfer(sub_uid=subuid,
                                         asset=asset,
                                         from_margin_account=from_margin_account,
                                         to_margin_account=to_margin_account,
                                         amount=amount,
                                         type='sub_to_master')
        pprint(r)
        time.sleep(2)
        r2 = linear_api.linear_financial_record(margin_account=to_margin_account,
                                                     type='35',
                                                     create_date='',
                                                     page_index='',
                                                     page_size='')
        pprint(r2)
        financial_record_lastest = r2['data']['financial_record'][0]

        actual = (financial_record_lastest['asset'], financial_record_lastest['amount'])

        pprint(financial_record_lastest)

        assert actual == expectedresult


if __name__ == '__main__':
    pytest.main()
