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
class TestUSDTSwapTransfer_006:

    def setup(self):
        print('\n前置条件')

    def test_execute(self, symbol, contract_code):
        asset = linear_api.get_trade_partition(contract_code)
        from_margin_account = contract_code
        to_margin_account = asset
        amount = '2.1'

        expectedresult = (to_margin_account, float(amount))

        r = linear_api.linear_transfer_inner(asset=asset, from_margin_account=from_margin_account,
                                             to_margin_account=to_margin_account, amount=amount)
        pprint(r)
        time.sleep(3)

        r2 = linear_api.linear_financial_record(margin_account=to_margin_account,
                                                type='38',
                                                create_date='',
                                                page_index='',
                                                page_size='')
        #        pprint(r2)
        financial_record_lastest = r2['data']['financial_record'][0]

        actual = (financial_record_lastest['margin_account'], financial_record_lastest['amount'])

        pprint(financial_record_lastest)

        assert actual == expectedresult

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
