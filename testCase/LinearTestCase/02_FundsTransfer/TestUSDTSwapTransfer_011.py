#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/1
# @Author  : 张广南


from pprint import pprint

import allure
import pytest
import time

from common.LinearServiceAPI import t as linear_api


@allure.epic('正向永续')
@allure.feature('资金划转（含母子划转，借贷币划转）')  # 这里填功能
@allure.story('跨账户划转')  # 这里填子功能，没有的话就把本行注释掉
@allure.tag('Script owner : 张广南', 'Case owner : 张广南')
@pytest.mark.stable
class TestUSDTSwapTransfer_011:

    def setup(self):
        print('\n前置条件')

    def test_execute(self, symbol, contract_code):
        asset = linear_api.get_trade_partition(contract_code)
        subuid = ""
        amount = "3"
        symbollist = ["BTC", "ETH"]
        to_symbol = symbollist[1] if symbol == symbollist[0] else symbollist[0]
        to_margin_account = to_symbol + "-" + asset
        from_margin_account = contract_code

        expectedresult = (asset, -float(amount))

        r = linear_api.linear_cross_sub_account_info_list(margin_account=asset)
        # pprint(r)
        sublist = r['data']['sub_list']
        if sublist != []:
            subuid = sublist[0]['sub_uid']
        pprint(subuid)
        r = linear_api.linear_master_sub_transfer(sub_uid=subuid,
                                                  asset=asset,
                                                  from_margin_account=from_margin_account,
                                                  to_margin_account=to_margin_account,
                                                  amount=amount,
                                                  type='master_to_sub')
        pprint(r)
        time.sleep(2)
        r2 = linear_api.linear_financial_record(margin_account=from_margin_account,
                                                type='34',
                                                create_date='',
                                                page_index='',
                                                page_size='')
        pprint(r2)
        financial_record_lastest = r2['data']['financial_record'][0]

        actual = (financial_record_lastest['asset'], financial_record_lastest['amount'])

        pprint(financial_record_lastest)

        assert actual == expectedresult

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')

if __name__ == '__main__':
    pytest.main()
