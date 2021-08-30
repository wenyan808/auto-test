#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/10/13
# @Author  : zhangranghan




from common.SwapServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError

from pprint import pprint
import pytest,allure,random,time


@allure.epic('反向永续')
@allure.feature('获取合约的历史资金费率')
class TestSwapHistoricalFundingRate:


    def test_swap_historical_funding_rate(self,contract_code):

        r = t.swap_historical_funding_rate(contract_code=contract_code,page_index='',page_size='')
        pprint(r)
        assert r['status'] == 'ok'



if __name__ == '__main__':
    pytest.main()