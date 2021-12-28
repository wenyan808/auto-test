#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/9
# @Author  : Alex Li

from common.ContractServiceAPI import t as contranct_api
from pprint import pprint
import pytest
import allure
import time
from tool.get_test_data import case_data


@allure.epic('反向交割')
@allure.feature('获取用户的合约账户和持仓信息')
@allure.tag('Script owner : Alex Li', 'Case owner : 曾超群')
@pytest.mark.stable
class TestContractTransfer_005:

    def setUp(self):
        print('\n前置条件')

    @allure.step('测试执行')
    def test_execute(self, symbol):
        subuid = ""
        amount = "0.14"

        expectedresult = (symbol, -float(amount))

        self.setUp()
        r = contranct_api.contract_sub_account_info_list(symbol=symbol)
        pprint(r)
        sublist = r['data']['sub_list']
        if sublist != []:
            subuid = sublist[0]['sub_uid']

        r = contranct_api.contract_master_sub_transfer(symbol=symbol,
                                                       amount=amount,
                                                       sub_uid=subuid,
                                                       type='master_to_sub')
        pprint(r)
        time.sleep(2)
        r2 = contranct_api.contract_financial_record(symbol=symbol,
                                                     type='34',
                                                     create_date='',
                                                     page_index='',
                                                     page_size='')
        pprint(r2)
        flag = False
        for k, v in enumerate(r2['data']['financial_record']):
            actual = (v['symbol'], v['amount'])
            if actual == expectedresult:
                flag = True
                print("第{}次命中。".format(k))
                break
        assert flag == True


if __name__ == '__main__':
    pytest.main()
