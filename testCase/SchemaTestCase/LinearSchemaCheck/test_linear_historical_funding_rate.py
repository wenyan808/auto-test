#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/8/7
# @Author  : zhangranghan



from common.LinearServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema,And,Or,Regex,SchemaError

from pprint import pprint
import pytest,allure,random,time



@allure.epic('正向永续')
@allure.feature('获取合约的历史资金费率')
class TestLinearHistoricalFundingRate:


    @allure.title('{title}')
    @pytest.mark.parametrize(*case_data())
    def test_linear_historical_funding_rate(self,title,contract_code,page_index,page_size,status):
        r = t.linear_historical_funding_rate(contract_code=contract_code,
                                             page_index=page_index,
                                             page_size=page_size)
        pprint(r)
        assert r['status'] == status


if __name__ == '__main__':
    pytest.main()
